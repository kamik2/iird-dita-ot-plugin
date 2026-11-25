# Validation of local version 1.2.0

Date: 25 November 2026. Toolkit: DITA-OT 4.4.2, isolated in `.work/dita-ot-4.4.2`.
Runtime/build JDK: Eclipse Temurin 25. Java compilation targets release 17.
No existing host toolkit was modified.

## Automated results

* Maven: **30 tests**, no failures or errors (28 inherited tests plus two schema/overlay tests).
* Installation of the standalone ZIP with `--force` succeeded; all three transformation types registered.
* **19 integration checks passed**, via `python scripts/verify.py .work/dita-ot-4.4.2`.
* Each of the five versioned RDF files and the combined manifest produced both
  a subject scheme and an HTML reference. All **327 distinct named terms** were
  covered by the combined output; generated taxonomy keys were unique.
* DITA-OT validated the combined subject scheme as DITA.
* German label selection and custom HTML reference stylesheet URL were checked.
* The all-domain DITA map produced Core, Machinery, Software, and Handover metadata.
* The additional RDF graph merged correctly, including bound input/package IRIs
  and the Unicode revision value `Ãœberarbeitung A`.
* A single-topic publication used the custom `files/` content directory and
  `.htm` extension; every rendition source resolved to an archive entry.
* Package checks confirmed an uncompressed first `mimetype` entry with the exact
  required bytes, no encryption, `META-INF/metadata.rdf`, and version `1.3`.
* Invalid native RDF input and cyclic vocabulary hierarchies failed as expected.
* The matching CycloneDX JSON and XML inventories pass the official 1.6 schemas;
  component and dependency sets match. The inventories include ten third-party
  JARs, three components embedded in the shaded Guava JAR, and five RDF assets.

The release archive contains a single top-level plug-in folder. Version identity,
registered libraries, schema hashes, main JAR contents and packaged SBOMs were
checked against the source files.

The transformation reference README was checked against all parameters and enumerated values in the local plug-in, HTML5, and common base descriptors. The rebuilt archive includes the same reference at its root.

## Limits

These are structural, unit and toolkit runtime checks. No full independent iiRDS
semantic/cardinality validator, external consumer import, production deployment,
Oxygen Author integration, PDF/A rendering or iiRDS/A/H conformance assessment was
performed. HTML output and CSS assets were checked structurally; visual browser
review has not been performed. Java 17 is the compilation target; the runtime
checks used Java 25. The iiRDS 1.3 standard's authoring and conformance requirements
remain applicable to supplied metadata and generated publications.

The Windows stock launcher exceeded command-line limits at this long workspace
path after integration. `scripts/dita.py` supplies the same installed toolkit and
plug-in libraries through a Java argument file; all reported integration checks
used this helper. Standard `dita install` also succeeded initially. The stock
launcher was not retested from a shorter installation path.

Logs and generated test artifacts are under `.work/verification/`, with
`results.json` recording the successful checks. Maven logs are under `.work/`.
