# Third-party material

The plug-in code retains the upstream Apache-2.0 licence and contributor notices.
Local modifications for version 1.2.0 add native RDF transformations, runtime SKOS
loading, structured RDF metadata merging, refreshed taxonomies, and DITA-OT 4.4.2
build and verification support. This local build is not an official consortium release.

The five RDF schema files are unchanged official iiRDS 1.3 downloads. Their embedded
copyright statements identify Gesellschaft für Technische Kommunikation – tekom
Deutschland e.V. and the Creative Commons Attribution-NoDerivatives 4.0 International
licence. See their original notices, [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/)
and [source URLs](SOURCES.md). Generated vocabulary views preserve the published
terms and identifiers; the RDF sources remain available in the distribution.

The distributed Java libraries and their declared licences are inventoried in both
CycloneDX files. The package contains ten third-party JARs: Apache Jena 3.17.0
(iri, core, base, shaded-guava), Commons CLI 1.4, Codec 1.15, Compress 1.20, CSV 1.8,
Lang 3.11, and Dexx Collection 0.7. Jena's shaded JAR includes Guava 30.0-jre,
failureaccess 1.0.1, and listenablefuture compatibility metadata. Their upstream
licence and notice files remain inside the JARs. The original upstream versions
are retained; this work is not a dependency vulnerability audit.

DITA-OT/DOST, Saxon, Commons IO, Guava from the host toolkit, SLF4J, and toolkit
rendering dependencies are supplied by DITA-OT and are not bundled as plug-in
libraries. Maven, JUnit, test logging, and the CycloneDX generator are build/test
tools. Their presence on the build machine does not make them shipped plug-in
components.

The old upstream PDF remains in the source tree as historical 1.1.0 documentation;
it is excluded from the 1.2.0 archive. The current README and DITA sources describe
the local changes. User-provided `_extern_resources` files are research inputs and
are not included in the plug-in archive.
