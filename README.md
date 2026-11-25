# iiRDS 1.3 plug-in for DITA-OT

Local development version **1.2.0**, based on the consortium's latest source revision
`969eb4e1d3459b1cb3e7d2a6210b458c53109935`. This is a local extension, not a consortium-published release.

Supports **DITA-OT 4.4.1 and 4.4.2** with Java 17 or newer. Verification uses Java 25.
iiRDS remains pinned to **1.3**.

| Transformation | Input | Output |
| --- | --- | --- |
| `iirds` | DITA map or topic | HTML5 content and RDF/XML metadata in `<input>.iirds` |
| `iirds-subjectscheme` | RDF/XML schema or bundled schema manifest | `subjectscheme.ditamap` |
| `iirds-schema-html` | RDF/XML schema or bundled schema manifest | `index.html` and `schema.css` |

All five official 1.3 RDF files are included unchanged: Core, Machinery, Software,
Handover, and SKOS annotations. The combined subject scheme covers every named term;
only instance keys assign taxonomy metadata. Class and property keys are references.
Native RDF transformations bypass DITA preprocessing.

See [all transformations, parameters, and allowed values](README_TRANSFORMATIONS.md) for the complete reference.

## Build and install

From this repository, with Maven and a JDK on PATH:

```powershell
mvn -B -f org.iirds.dita.ot.plugin/pom.xml clean package
dita install org.iirds.dita.ot.plugin/target/org.iirds.dita.package-1.2.0.zip --force
dita transtypes
```

The ZIP contains one top-level folder, `org.iirds.dita.package`. Install it into your
chosen toolkit. The `org.iirds.dita.ot.mdext` directory is the original, optional
consortium extension example; it is not needed by this plug-in.

The Java code compiles against the latest DOST API artifact available on Maven
Central, 4.3.0; the installable package is tested on the current toolkit distribution,
4.4.2. The descriptor requires DITA-OT 4.4.1 or newer, including Oxygen 29's bundled toolkit. Later releases require
fresh runtime testing.

## Publish

```powershell
dita -i manual.ditamap -f iirds -o out
# Use absolute paths for additional RDF metadata:
dita -i manual.ditamap -f iirds -o out --iirds.metadata.file=C:/project/metadata.rdf
```

The optional RDF/XML graph supports all schema classes, properties and nested
structures. Within it, `urn:iirds:input` refers to the generated input Document or
Topic, and `urn:iirds:package` refers to the generated Package. Other IRIs and blank
nodes are preserved. The graph is merged before the metadata post-processing hook.
Its semantic validity and cardinalities remain the author's responsibility.
See the [all-domain example](org.iirds.dita.ot.plugin/src/plugin/examples/all-domains/publication.ditamap).

The normal HTML5 parameters apply, for example `--args.css=project.css --args.copycss=yes`.
Use `--iirds.contentpath=files` to change the archive's content directory and
`--args.outext=htm` to change the HTML extension.

For `iirds`, omit `--default.language` to detect the language from the input topic,
map, or bookmap's root `xml:lang`, with `en` as the final fallback. An explicit
`--default.language=de` overrides generated root languages and iiRDS language
metadata. Topic-specific authored languages are preserved when no override is set.
This changes language settings without translating or modifying authored files.

## Transform the RDF schemas

Replace `DITA-OT` with your toolkit directory:

```powershell
dita -i DITA-OT/plugins/org.iirds.dita.package/schemas/iirds-1.3.xml -f iirds-subjectscheme -o taxonomy
dita -i DITA-OT/plugins/org.iirds.dita.package/schemas/iirds-1.3.xml -f iirds-schema-html -o reference
# Any of the five individual .rdf files can also be used as input.
```

Both native transformations accept `--iirds.language=de`. When omitted, they use
the input root `xml:lang`, falling back to `en`. Available labels in another language
remain a fallback when the requested vocabulary language has no matching label. The HTML reference accepts `--iirds.schema.css=https://example.org/reference.css`;
this is a stylesheet URL, while `args.css` controls the DITA HTML5 publication.
The bundled HTML reference stylesheet supplies usable light and dark defaults.

For metadata authoring, use the combined subject scheme in `subjectscheme/`, or a
project-specific scheme extending it. Software keys use `iirdsSft.`; the older
`iirdSft.` spelling remains available as an alias.

## Verify in an isolated toolkit

Unpack DITA-OT 4.4.2 into a disposable directory, then run:

```powershell
python scripts/dita.py .work/dita-ot-4.4.2 install org.iirds.dita.ot.plugin/target/org.iirds.dita.package-1.2.0.zip --force
python scripts/verify.py .work/dita-ot-4.4.2
```

The helper uses a Java argument file to avoid Windows command-line length limits.
Verification checks all five schemas individually and together, registered
transformations, generated taxonomy coverage, DITA validity, HTML assets, map and
single-topic packages, rendition paths, archive structure, and RDF metadata merging.

See [source provenance](docs/SOURCES.md), [validation evidence](docs/VALIDATION.md),
and the matching SBOMs in [JSON](docs/SOFTWARE_BILL_OF_MATERIALS.cdx.json) and
[XML](docs/SOFTWARE_BILL_OF_MATERIALS.cdx.xml).

This produces unrestricted iiRDS packages. Using Handover vocabulary does not by
itself establish iiRDS/H conformance; this implementation does not add restricted
PDF/A delivery or iiRDS/A XHTML conformance validation.

Code retains the upstream Apache-2.0 licence. The unchanged iiRDS schema files
retain their own CC BY-ND 4.0 notices. See [third-party notices](docs/THIRD_PARTY.md).
