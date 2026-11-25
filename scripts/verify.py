"""Integration checks against an isolated, installed DITA-OT. Uses Python stdlib only."""
import argparse
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
IIRDS = '{http://iirds.tekom.de/iirds#}'
HOV = '{http://iirds.tekom.de/iirds/domain/handover#}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('toolkit', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / '.work' / 'verification')
    args = parser.parse_args()
    toolkit, out = args.toolkit.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    plugin = toolkit / 'plugins/org.iirds.dita.package'
    schemas = plugin / 'schemas'
    results = []
    def dita(label, *options, success=True):
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts/dita.py'), str(toolkit), *map(str, options)], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        (out / (label + '.log')).write_text(proc.stdout, encoding='utf-8')
        assert (proc.returncode == 0) == success, label + ': ' + proc.stdout[-5000:]
        results.append(label)
    dita('transtypes', 'transtypes')
    registered = (out / 'transtypes.log').read_text()
    assert all(t in registered.splitlines() for t in ['iirds', 'iirds-subjectscheme', 'iirds-schema-html'])
    union = set()
    schema_paths = sorted(schemas.glob('*.rdf'))
    assert len(schema_paths) == 5
    for source in [*schema_paths, schemas / 'iirds-1.3.xml']:
        expected = set()
        for f in schema_paths if source.suffix == '.xml' else [source]:
            expected.update(n.attrib[RDF+'about'] for n in ET.parse(f).getroot() if RDF+'about' in n.attrib)
        union.update(expected)
        stem = source.stem
        scheme_dir, html_dir = out / (stem+'-scheme'), out / (stem+'-html')
        dita(stem+'-scheme', '-i', source, '-f', 'iirds-subjectscheme', '-o', scheme_dir)
        generated = ET.parse(scheme_dir / 'subjectscheme.ditamap')
        uris = {n.attrib['appid'] for n in generated.iter('resourceid')}
        assert expected <= uris, (stem, expected - uris)
        keys = [k for n in generated.iter('subjectdef') for k in n.attrib.get('keys','').split()]
        assert len(keys) == len(set(keys)), 'Duplicate taxonomy key'
        dita(stem+'-html', '-i', source, '-f', 'iirds-schema-html', '-o', html_dir)
        html = (html_dir / 'index.html').read_text(encoding='utf-8')
        assert all(uri in html for uri in expected)
        assert (html_dir / 'schema.css').is_file()
    dita('schema-language-css', '-i', schemas/'iirds-core.rdf', '-f', 'iirds-schema-html', '-o', out/'custom', '--iirds.language=de', '--iirds.schema.css=https://example.org/project.css')
    custom = (out/'custom/index.html').read_text(encoding='utf-8')
    assert 'lang="de"' in custom and 'https://example.org/project.css' in custom
    dita('scheme-dita-validation', 'validate', '-i', plugin/'subjectscheme/iirds-generated-subjectscheme.ditamap')
    example = plugin / 'examples/all-domains'
    dita('all-domains-package', '-i', example/'publication.ditamap', '-f', 'iirds', '-o', out/'map', '--iirds.metadata.file='+str(example/'metadata.rdf'))
    def package(filename):
        with zipfile.ZipFile(filename) as z:
            first = z.infolist()[0]
            assert first.filename == 'mimetype' and first.compress_type == zipfile.ZIP_STORED
            assert z.read('mimetype') == b'application/iirds+zip'
            assert all(not i.flag_bits & 1 for i in z.infolist())
            rdf = ET.fromstring(z.read('META-INF/metadata.rdf'))
            assert [n.text for n in rdf.iter(IIRDS+'iiRDSVersion')] == ['1.3']
            sources = [n.text for n in rdf.iter(IIRDS+'source')]
            assert sources and all(s in z.namelist() for s in sources), sources
            return rdf, sources
    rdf, _ = package(out/'map/publication.iirds')
    def object_uri(n):
        return n.attrib.get(RDF+'resource') or next((c.attrib.get(RDF+'about') for c in n), None)
    assert any(object_uri(n) == 'http://iirds.tekom.de/iirds/domain/handover#Operation' for n in rdf.iter(HOV+'has-document-category'))
    phases = {object_uri(n) for n in rdf.iter(IIRDS+'relates-to-product-lifecycle-phase')}
    assert {'http://iirds.tekom.de/iirds#Operation', 'http://iirds.tekom.de/iirds/domain/machinery#FirstUse', 'http://iirds.tekom.de/iirds/domain/software#Deployment'} <= phases, phases
    assert 'Überarbeitung A' in [n.text for n in rdf.iter(IIRDS+'revision')]
    dita('single-topic-package', '-i', example/'operation.dita', '-f', 'iirds', '-o', out/'topic', '--args.outext=htm', '--iirds.contentpath=files')
    _, sources = package(out/'topic/operation.iirds')
    assert all(s.startswith('files/') and s.endswith('.htm') for s in sources)
    invalid = out/'invalid.rdf'
    invalid.write_text('<invalid/>', encoding='utf-8')
    dita('reject-invalid-rdf', '-i', invalid, '-f', 'iirds-subjectscheme', '-o', out/'invalid', success=False)
    cycle = out/'cycle.rdf'
    cycle.write_text('<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"><rdfs:Class rdf:about="urn:A"><rdfs:subClassOf rdf:resource="urn:B"/></rdfs:Class><rdfs:Class rdf:about="urn:B"><rdfs:subClassOf rdf:resource="urn:A"/></rdfs:Class></rdf:RDF>', encoding='utf-8')
    dita('reject-cyclic-schema', '-i', cycle, '-f', 'iirds-subjectscheme', '-o', out/'cycle', success=False)
    (out/'results.json').write_text(json.dumps({'checks':results,'unique_schema_terms':len(union)},indent=2),encoding='utf-8')
    print(str(len(results))+' integration checks passed; '+str(len(union))+' distinct schema terms covered.')

if __name__ == '__main__':
    main()
