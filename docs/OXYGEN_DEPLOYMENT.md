# Oxygen XML Editor 29 deployment

Installed on 25 November 2026 at the user's request.

* Toolkit: Oxygen-bundled DITA-OT **4.4.1**.
* Plug-in: local **1.2.0**, using iiRDS **1.3**.
* Destination: `C:/Users/101020/AppData/Local/Programs/Oxygen XML Editor 29/frameworks/dita/DITA-OT/plugins/org.iirds.dita.package`.
* Compatibility declaration: DITA-OT **4.4.1 or newer**, verified on 4.4.1 and 4.4.2.

The Oxygen toolkit's own `bin/dita.bat install <archive> --force` copied the archive
into the named plug-in directory and rebuilt integration files. The toolkit itself
remains version 4.4.1. The previous plug-in was backed up under
`.work/oxygen-before-language-change/org.iirds.dita.package` in the source workspace.

All three transformation types were registered: `iirds`, `iirds-subjectscheme`, and
`iirds-schema-html`. On the installed host, the 19 general integration checks and
19 language precedence checks passed. The checks invoke the installed toolkit
through `scripts/dita.py`, which includes Oxygen's patch JAR and `lib/saxon` JARs
in the launcher classpath and avoids Windows command-line length limits.

Language precedence is an explicit export parameter, then the input root's
`xml:lang`, then `en`. For DITA exports use `default.language`; for native RDF exports
use `iirds.language`. Without an export override, authored topic languages and
map/bookmap inheritance are retained. Explicit DITA overrides change generated
root language settings and iiRDS metadata; they do not translate or rewrite source
files. In an Oxygen transformation scenario, leave the language parameter unset to
enable automatic detection.

Install and export logs are in `.work/oxygen-install.log`,
`.work/oxygen-verification/`, and `.work/oxygen-language-verification/`.
These are real host-toolkit checks. Oxygen UI rendering, third-party consumer
imports, and independent iiRDS conformance validation were not performed.
