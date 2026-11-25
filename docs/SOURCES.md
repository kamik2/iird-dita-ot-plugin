# Sources and resource access

Checked 25 November 2026. iiRDS content is pinned to **1.3**.

## Normative reference

[Official iiRDS 1.3 specification, released 3 November 2025](https://www.iirds.org/fileadmin/iiRDS_specification/20251103-1.3-release/index.html).
The full document was fetched successfully; the user's offline copy is in
`_extern_resources/website/tekom iiRDS Standard.html`.
The web-search reader could not open the large HTML page, but direct HTTP retrieval
worked, so this is not an outstanding access blocker.

The specification's schema reference exposes these working, direct versioned downloads:

| File | Direct source | SHA-256 |
| --- | --- | --- |
| iirds-core.rdf | [Download](https://iirds.org/fileadmin/downloads/documents/rdfs/1.3/iirds-core.rdf) | `caa384a8b7cc44041b12c4b80e606edc865d4808fa67bd181653f0055f2a3d7a` |
| iirds-machinery.rdf | [Download](https://iirds.org/fileadmin/downloads/documents/rdfs/1.3/iirds-machinery.rdf) | `6301d5c461fac5b520bcb3932cc2200b8411a85715f0fbda402129702599d993` |
| iirds-software.rdf | [Download](https://iirds.org/fileadmin/downloads/documents/rdfs/1.3/iirds-software.rdf) | `9c8a556a622e637f445954ac4629d5af2ac0fafbd85419cba8c300b82ad5a039` |
| iirds-handover.rdf | [Download](https://iirds.org/fileadmin/downloads/documents/rdfs/1.3/iirds-handover.rdf) | `21af671432473816a74bffbdee79e8435aa6bf5d397158f848688785f57cf93f` |
| iirds-skos.rdf | [Download](https://iirds.org/fileadmin/downloads/documents/rdfs/1.3/iirds-skos.rdf) | `8b1f5369ebe9e2ac524da0939acca290feed1067ac28ee21e3ab705fd654b711` |

These files are preserved byte for byte in `src/main/resources`, inside the code
JAR and as readable `schemas/*.rdf` assets in the distribution. Git attributes
prevent newline conversion. The consortium plug-in's original files are content-equivalent
after line-ending normalization; no vocabulary rewrite was needed.

## Consortium repositories

* [dita-ot-plugin](https://github.com/iirds-consortium/dita-ot-plugin): local source
  matched the current upstream HEAD `969eb4e1d3459b1cb3e7d2a6210b458c53109935` before edits.
* [models](https://github.com/iirds-consortium/models): inspected the four public
  RDF files and branches. Its main branch does not include Handover. Use the
  versioned 1.3 downloads above as this build's authority.
* [specification](https://github.com/iirds-consortium/specification): inspected
  the repository structure and source sections on domains, archive rules,
  schema definitions and class constraints. The versioned published HTML is the
  release reference.
* [dita-ot-plugin-registry](https://github.com/iirds-consortium/dita-ot-plugin-registry):
  a registry fork, not an additional RDF vocabulary or transformation engine.
  This local 1.2.0 build is not published there.

## Other supplied materials

The supplied files in `_rdf/` match the corresponding exact versioned downloads.
The upstream 1.1.0 package and `iirds_plugin.pdf` are available in
`_extern_resources`; the PDF's text was extracted for review. No rendered PDF
layout review or PDF modification was performed. The supplied 2019 sample packages
are historical examples, not 1.3 schema authority or 1.3 conformance fixtures.
The repository's existing metadata handlers, subject scheme conventions, and SPI
extension boundaries informed the implementation.

The website's [1.3 download landing page](https://www.iirds.org/materials/version-13)
and [sample content landing page](https://www.iirds.org/materials/sample-content)
hide download controls behind login. The direct schema URLs and user-supplied
sample files resolve the required access gaps. No required resource is currently
blocked. Other member-only or unrelated site material was not exhaustively audited.

## Toolkit reference

[DITA-OT 4.4.2 release](https://github.com/dita-ot/dita-ot/releases/tag/4.4.2),
released 14 November 2026, was the current stable release when checked.
The official distribution was installed only under `.work/` for isolated testing.
Maven Central currently exposes DOST 4.3.0 as its latest API artifact; this is why
the compile dependency differs from the verified runtime version.
