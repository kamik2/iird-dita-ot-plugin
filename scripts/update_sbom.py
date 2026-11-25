"""Enrich Maven CycloneDX 1.6 output with verified shaded libraries and RDF assets.
Run makeBom first; this script requires lxml and writes both equivalent formats.
"""
import hashlib
import io
import json
from pathlib import Path
import zipfile
from lxml import etree as ET
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT/'org.iirds.dita.ot.plugin/target'
NS = 'http://cyclonedx.org/schema/bom/1.6'
Q = lambda name: '{'+NS+'}'+name
j = json.loads((TARGET/'SOFTWARE_BILL_OF_MATERIALS.cdx.json').read_text(encoding='utf-8'))
x = ET.parse(str(TARGET/'SOFTWARE_BILL_OF_MATERIALS.cdx.xml'))
components, dependencies = x.find(Q('components')), x.find(Q('dependencies'))
product = j['metadata']['component']['bom-ref']
extra = []
for f in sorted((ROOT/'org.iirds.dita.ot.plugin/src/main/resources').glob('*.rdf')):
    extra.append({'type':'data','bom-ref':'urn:iirds:schema:1.3:'+f.name,'name':f.name,'version':'1.3',
        'hashes':[{'alg':'SHA-256','content':hashlib.sha256(f.read_bytes()).hexdigest()}],
        'licenses':[{'license':{'id':'CC-BY-ND-4.0'}}],
        'externalReferences':[{'type':'distribution','url':'https://iirds.org/fileadmin/downloads/documents/rdfs/1.3/'+f.name}]})
with zipfile.ZipFile(TARGET/'org.iirds.dita.package-1.2.0.zip') as z:
    jar = zipfile.ZipFile(io.BytesIO(z.read('org.iirds.dita.package/lib/jena-shaded-guava.jar')))
    pom = jar.read('META-INF/maven/org.apache.jena/jena-shaded-guava/pom.xml').decode()
    assert '<version>30.0-jre</version>' in pom
    for name, version in [('guava','30.0-jre'),('failureaccess','1.0.1'),('listenablefuture','9999.0-empty-to-avoid-conflict-with-guava')]:
        if name != 'guava':
            assert ('version='+version) in jar.read('META-INF/maven/com.google.guava/'+name+'/pom.properties').decode()
        extra.append({'type':'library','bom-ref':'pkg:maven/com.google.guava/'+name+'@'+version,
            'group':'com.google.guava','name':name,'version':version,
            'description':'Embedded in jena-shaded-guava.jar; listenablefuture is an empty compatibility artifact.' if name=='listenablefuture' else 'Embedded and relocated in jena-shaded-guava.jar.',
            'licenses':[{'license':{'id':'Apache-2.0'}}],
            'purl':'pkg:maven/com.google.guava/'+name+'@'+version})

def add(parent, name, text=None, attrs=None):
    node=ET.SubElement(parent,Q(name),attrs or {})
    if text is not None: node.text=text
    return node
for c in extra:
    node=add(components,'component',attrs={'type':c['type'],'bom-ref':c['bom-ref']})
    for key in ['group','name','version','description']:
        if key in c: add(node,key,c[key])
    if 'hashes' in c:
        h=add(node,'hashes')
        for v in c['hashes']: add(h,'hash',v['content'],{'alg':v['alg']})
    licenses=add(node,'licenses')
    add(add(licenses,'license'),'id',c['licenses'][0]['license']['id'])
    if 'purl' in c: add(node,'purl',c['purl'])
    if 'externalReferences' in c:
        refs=add(node,'externalReferences')
        for ref in c['externalReferences']: add(add(refs,'reference',attrs={'type':ref['type']}),'url',ref['url'])
    j['components'].append(c)
    parent = product if c['type']=='data' else next(a['bom-ref'] for a in j['components'] if a['name']=='jena-shaded-guava')
    dep = next((d for d in j['dependencies'] if d['ref']==parent),None)
    if dep is None:
        dep={'ref':parent,'dependsOn':[]};j['dependencies'].append(dep)
    dep.setdefault('dependsOn',[]).append(c['bom-ref'])
    xdep=next((d for d in dependencies if d.attrib['ref']==parent),None)
    if xdep is None: xdep=add(dependencies,'dependency',attrs={'ref':parent})
    add(xdep,'dependency',attrs={'ref':c['bom-ref']})
    j['dependencies'].append({'ref':c['bom-ref'],'dependsOn':[]})
    add(dependencies,'dependency',attrs={'ref':c['bom-ref']})
# Maven JSON collapses POM description whitespace; keep XML text identical.
for c in j['components']:
    xc=next(v for v in components if v.attrib['bom-ref']==c['bom-ref'])
    if 'description' in c: xc.find(Q('description')).text=c['description']
j['version']=2;x.getroot().set('version','2')
out=ROOT/'docs';out.mkdir(exist_ok=True)
(out/'SOFTWARE_BILL_OF_MATERIALS.cdx.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
x.write(str(out/'SOFTWARE_BILL_OF_MATERIALS.cdx.xml'),encoding='UTF-8',xml_declaration=True,pretty_print=True)
assert {c['bom-ref'] for c in j['components']} == {c.attrib['bom-ref'] for c in components}
assert {d['ref']:set(d.get('dependsOn',[])) for d in j['dependencies']} == {d.attrib['ref']:{v.attrib['ref'] for v in d} for d in dependencies}
print('Wrote equivalent SBOMs with',len(j['components']),'components.')
