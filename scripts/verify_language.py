"""Check language precedence on native RDF and DITA topic/map/bookmap exports."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
IIRDS = '{http://iirds.tekom.de/iirds#}'

class HtmlLanguage(HTMLParser):
    language = None
    def handle_starttag(self, tag, attrs):
        if tag == 'html': self.language = dict(attrs).get('lang')

def main():
    toolkit = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT/'.work/language-verification'
    out.mkdir(parents=True, exist_ok=True)
    results = []
    def dita(label, source, kind, expected, *options):
        destination = out/label
        proc = subprocess.run([sys.executable, str(ROOT/'scripts/dita.py'), str(toolkit), '-i', str(source), '-f', kind, '-o', str(destination), *options], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        (out/(label+'.log')).write_text(proc.stdout, encoding='utf-8')
        assert proc.returncode == 0, label+': '+proc.stdout[-4000:]
        if kind == 'iirds-subjectscheme':
            assert ET.parse(destination/'subjectscheme.ditamap').getroot().attrib[XML_LANG] == expected
        elif kind == 'iirds-schema-html':
            parser = HtmlLanguage(); parser.feed((destination/'index.html').read_text(encoding='utf-8'))
            assert parser.language == expected, (label, parser.language)
        else:
            with zipfile.ZipFile(destination/(source.stem+'.iirds')) as z:
                model = ET.fromstring(z.read('META-INF/metadata.rdf'))
                languages = {n.text for n in model.iter(IIRDS+'language')}
                assert languages == set(expected.split('+')), (label, languages)
                for entry in z.namelist():
                    if entry.endswith('.html'):
                        parser = HtmlLanguage(); parser.feed(z.read(entry).decode('utf-8'))
                        assert parser.language in expected.split('+'), (label, entry, parser.language)
        results.append(label)

    fixture = out/'fixtures'; fixture.mkdir(exist_ok=True)
    rdf_template = '''<rdf:RDF {language} xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"><rdfs:Class rdf:about="urn:example:Term"><rdfs:label xml:lang="en">Term</rdfs:label><rdfs:label xml:lang="de">Begriff</rdfs:label></rdfs:Class></rdf:RDF>'''
    schema = fixture/'vocabulary.rdf'
    for kind in ['iirds-subjectscheme', 'iirds-schema-html']:
        for case, attribute, expected, options in [('detect', 'xml:lang="de"', 'de', []), ('override', 'xml:lang="de"', 'en', ['--iirds.language=en']), ('fallback', '', 'en', [])]:
            schema.write_text(rdf_template.format(language=attribute), encoding='utf-8')
            dita(kind+'-'+case, schema, kind, expected, *options)
        schema.write_text(rdf_template.format(language='xml:lang="en"'), encoding='utf-8')
        manifest = fixture/'schemas.xml'
        manifest.write_text('<schemas xml:lang="de"><schema href="vocabulary.rdf"/></schemas>', encoding='utf-8')
        dita(kind+'-manifest-language', manifest, kind, 'de')

    concept = '''<?xml version="1.0"?><!DOCTYPE concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "concept.dtd"><concept id="language-example" {language}><title>Language example</title><conbody><p>Authored content.</p></conbody></concept>'''
    for root_name in ['topic', 'map', 'bookmap']:
        for case, attribute, expected, options in [('detect', 'xml:lang="de"', 'de', []), ('override', 'xml:lang="de"', 'fr', ['--default.language=fr']), ('fallback', '', 'en', [])]:
            case_dir = fixture/(root_name+'-'+case); case_dir.mkdir(exist_ok=True)
            topic = case_dir/'topic.dita'
            topic.write_text(concept.format(language=attribute if root_name == 'topic' else ''), encoding='utf-8')
            source = topic
            if root_name == 'map':
                source = case_dir/'publication.ditamap'
                source.write_text('<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd"><map id="language-map" '+attribute+'><title>Language example</title><topicref href="topic.dita"/></map>', encoding='utf-8')
            elif root_name == 'bookmap':
                source = case_dir/'publication.bookmap'
                source.write_text('<!DOCTYPE bookmap PUBLIC "-//OASIS//DTD DITA BookMap//EN" "bookmap.dtd"><bookmap id="language-book" '+attribute+'><booktitle><mainbooktitle>Language example</mainbooktitle></booktitle><chapter href="topic.dita"/></bookmap>', encoding='utf-8')
            original = {f:hashlib.sha256(f.read_bytes()).digest() for f in case_dir.iterdir()}
            dita(root_name+'-'+case, source, 'iirds', expected, *options)
            assert all(hashlib.sha256(f.read_bytes()).digest() == digest for f, digest in original.items()), 'Authored input changed'

    mixed_dir = fixture/'map-detect'
    (mixed_dir/'topic.dita').write_text(concept.format(language='xml:lang="es"'), encoding='utf-8')
    original = {f:hashlib.sha256(f.read_bytes()).digest() for f in mixed_dir.iterdir()}
    dita('mixed-topic-language', mixed_dir/'publication.ditamap', 'iirds', 'de+es')
    dita('mixed-topic-override', mixed_dir/'publication.ditamap', 'iirds', 'fr', '--default.language=fr')
    assert all(hashlib.sha256(f.read_bytes()).digest() == digest for f, digest in original.items())
    (out/'results.json').write_text(json.dumps({'checks':results}, indent=2), encoding='utf-8')
    print(str(len(results))+' language precedence checks passed.')

if __name__ == '__main__': main()
