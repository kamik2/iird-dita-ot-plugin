# Rebuild and inventory

Build and run unit tests:

```powershell
mvn -B -f org.iirds.dita.ot.plugin/pom.xml clean package
```

To refresh the distribution inventory after dependency changes:

```powershell
mvn -B -f org.iirds.dita.ot.plugin/pom.xml org.cyclonedx:cyclonedx-maven-plugin:2.9.1:makeBom '-DoutputFormat=all' '-DoutputName=SOFTWARE_BILL_OF_MATERIALS.cdx' '-DincludeProvidedScope=false' '-DincludeTestScope=false' '-DschemaVersion=1.6'
python scripts/update_sbom.py
mvn -B -f org.iirds.dita.ot.plugin/pom.xml package
```

The enrichment script inspects the built archive and shaded Jena JAR, adds the
five unchanged RDF assets and embedded Guava components, and writes matching
JSON/XML inventories. Python `lxml` is needed for enrichment. It is a build aid,
not a plug-in runtime dependency. Recheck both files against the official
CycloneDX 1.6 JSON Schema and XSD after an inventory change. Rebuilding packages
the committed documentation and both inventories under `docs/`.

Language precedence checks: `python scripts/verify_language.py PATH_TO_TOOLKIT`.
The launcher also recognizes Oxygen's `lib/saxon` and DOST patch libraries.

Use the isolated installation and integration commands in the repository README
before delivering a rebuilt ZIP. Read the validation limits in `VALIDATION.md`.

If an IDE is compiling into the same `target` directory, use a separate Maven output:

```powershell
mvn -B -f org.iirds.dita.ot.plugin/pom.xml package '-Diirds.build.directory=C:/absolute/path/to/isolated-output'
```

The output directory must be absolute. This avoids sharing class and test-resource
files with an IDE background compiler.
