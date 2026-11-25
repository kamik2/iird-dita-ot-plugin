# Transformation and parameter reference

This README describes local plug-in **1.2.0**, **iiRDS 1.3**, and the inspected
**DITA-OT 4.4.2** parameter definitions (also deployed on Oxygen's DITA-OT 4.4.1). Names and enumerated values are case-sensitive.
It covers every transformation declared by this plug-in, every plug-in parameter,
and all parameters declared by its HTML5 and common DITA-OT base descriptors.
Other toolkit transformations such as `pdf` and `html5` are supplied by the host;
they are not additional transformations implemented by this project.

## Transformations

| Transformation (`-f`) | Accepted input (`-i`) | Files written to the output directory (`-o`) | Purpose |
| --- | --- | --- | --- |
| `iirds` | DITA map/bookmap or individual DITA topic, with dependencies resolvable by the toolkit | `<input-stem>.iirds`, containing HTML5 content and `META-INF/metadata.rdf` | Publish an unrestricted iiRDS 1.3 delivery package. |
| `iirds-subjectscheme` | RDF/XML schema with an `rdf:RDF` root, or an XML `schemas` manifest | `subjectscheme.ditamap` | Generate DITA subject definitions for vocabulary authoring. Runs directly on RDF, without DITA preprocessing. |
| `iirds-schema-html` | Same native RDF/XML or manifest input | `index.html` and the default `schema.css` | Generate a readable vocabulary reference. Runs directly on RDF, without DITA preprocessing. |

All five official schema files are bundled in `schemas/`: `iirds-core.rdf`,
`iirds-machinery.rdf`, `iirds-software.rdf`, `iirds-handover.rdf`, and `iirds-skos.rdf`.
Use `schemas/iirds-1.3.xml` to transform them together. They do not require separate
domain-specific transformation names. The optional `org.iirds.dita.ot.mdext` sample
extension declares no additional transformation.

The `iirds` package has a fixed standard version of **1.3**. No parameter selects a
different iiRDS version, PDF delivery, iiRDS/A, or iiRDS/H. Handover vocabulary is
available, but its use alone does not establish iiRDS/H conformance.

## Command-line notation and common options

```powershell
dita -i INPUT -f TRANSFORMATION -o OUTPUT --parameter.name=VALUE
```

Quote the complete `--name=value` argument when it contains spaces. Use `yes/no`,
`true/false`, or uppercase values exactly as listed; these spellings are not
interchangeable across parameters. Paths in examples are placeholders to replace.

| Option | Allowed values / format | Default | Description |
| --- | --- | --- | --- |
| `-i`, `--input` | Readable input file path of the type shown in the transformation table | Required | Selects the source file. |
| `-f`, `--format` | One of the three transformation names above | Required | Selects the transformation. |
| `-o`, `--output` | Output directory path | Normally `<DITA-OT>/out` | Sets the destination. Native transformations use fixed output filenames, so separate destinations avoid overwriting previous results. |
| `--temp` | Absolute temporary directory path | Toolkit-generated temporary directory | Sets the build working directory (`dita.temp.dir`). |
| `--verbose` | Switch; no value | Off | Includes more build messages. |
| `--debug` | Switch; no value | Off | Includes debug logging. |
| `--filter` | Readable DITAVAL path; repeatable | None | Filters DITA content for `iirds`; native RDF transformations do not process DITAVAL. |
| `--resource` | Readable DITA resource path; repeatable | None | Adds resource documents for `iirds`; native RDF transformations do not perform DITA key resolution. |

## Language selection

Language selection uses this order:

1. A non-empty export parameter: `default.language` for `iirds`, or `iirds.language`
   for the two native RDF transformations.
2. The root `xml:lang` of the input topic, map, bookmap, RDF file, or schema manifest.
3. `en` when that attribute is absent or blank.

Without an explicit DITA export override, topics keep their own `xml:lang` and
otherwise inherit the map/bookmap language. An explicit `default.language` overrides
the generated document roots and iiRDS language metadata. It changes generated
language settings; it does not translate authored text. Authored files are never
rewritten. A native manifest supplies its own language context; the first referenced
RDF file does not determine the manifest's language.

For example, export a map with `xml:lang="de"` without any language parameter to
select German automatically. Add `--default.language=fr` to explicitly select
French language settings for its generated publication. In an Oxygen export
scenario, leave the applicable language parameter unset for detection; a saved
`en` value is an explicit override.

## `iirds`: publishing and metadata parameters

All parameters in this table are optional.

| Parameter | Allowed values / value format | Default | Description |
| --- | --- | --- | --- |
| `iirds.contentpath` | Relative archive directory such as `content`, `files`, or `delivery/html`; use forward slashes and no absolute path or `..` segments | `content` | Sets the directory prefix for packaged content and the rendition source references in RDF. Use a non-empty directory name. This is an archive path, not an output directory on disk. |
| `iirds.metadatahandler` | `all`, or one or more registered handler names separated by `+`; built-in names are listed below | `all` | Selects which optional metadata extractions run. It does not disable basic topic/document/package generation, title, language, or type mapping. |
| `iirds.irihandler` | `default`, or a `+`-separated ordered list of registered IRI handler names | `default` | Selects the identifier strategies. Each request uses the first handler that supplies an IRI; unresolved requests use the UUID fallback. |
| `iirds.metadata.file` | Absolute path to an existing, readable RDF/XML file | None; no additional graph | Merges an explicit metadata graph after normal model construction and before metadata post-processing. Supports nested structures, literals, and properties beyond taxonomy tags. Existing triples are retained; this is a merge, not a replacement. |
| `args.outext` | Non-empty HTML filename extension such as `html`, `htm`, `.html`, or `.htm`; no path separators | `html` | Changes generated HTML filenames and RDF rendition source extensions. Changing the suffix does not change HTML5 into another content format. |

These path/extension recommendations describe usable input; the plug-in does not
implement a strict allowlist for every string parameter. Values that are accepted
syntactically can still create unusable archive references.

### Built-in metadata handler values

| Handler name | What it extracts |
| --- | --- |
| `shortdesc` | Topic/map short descriptions as `iirds:has-abstract`. |
| `prodname` | Product names from `prodname` as related product variants. |
| `component` | Component names from `component` as related components. |
| `product-p` | Values of the root `product` profiling attribute as related product variants. |
| `critdates` | Creation, modification, effect, and expiry information from supported `critdates` data. |
| `copyright` | Copyright information as rights metadata. |
| `audience` | Audience elements as qualification metadata. |
| `audience-p` | Root `audience` profiling attribute values as qualifications. |
| `subjectscheme` | `data` key references to subject definitions carrying iiRDS class/instance IRIs. Use the combined subject scheme for cross-domain authoring. |

Example selection: `--iirds.metadatahandler=shortdesc+prodname+subjectscheme`.
Installed extension plug-ins may register more names. The bundled sample extension
adds `admonition` and `othermeta` only when installed separately.

Current selection behavior matters: `all` is a special selector, not a registered
handler. It is removed before named handlers are looked up; if no valid named
handler remains, all registered handlers run. Thus `all+shortdesc` selects only
`shortdesc`. Unknown names are logged; if every supplied name is unknown, selection
falls back to all handlers. There is no built-in `none` selector, and `default` is
not a registered metadata handler. Omit the parameter or use `all` for the normal
behavior.

### IRI handler values and RDF graph bindings

The standalone package registers only the `default` IRI handler. It derives topic
and document IRIs from the source ID and preprocessed content hash, information
object IRIs from the ID, package IRIs from a UUID, and metadata IRIs from matching
vocabulary terms or generated identifiers. Missing source information uses UUIDs.
`all` and `fallback` are not registered selectable IRI handlers. Unknown names are
logged and do not select `default`. The separate sample extension registers `csv`;
with that extension installed, `--iirds.irihandler=csv+default` tries its mapping
before the standard handler.

Inside `iirds.metadata.file`, the following resource IRIs are bound on both the
subject and object side of RDF triples:

| Resource IRI | Bound resource |
| --- | --- |
| `urn:iirds:input` | The generated Document for a map, or Topic for a single-topic input. |
| `urn:iirds:package` | The generated Package. |

Other IRIs and blank nodes remain unchanged. These are RDF resource values, not
command-line parameters. The additional graph is not a schema-selection switch or
a conformance validator; its author must respect iiRDS 1.3 semantics and cardinalities.

```powershell
dita -i manual.ditamap -f iirds -o out/manual --iirds.contentpath=files --args.outext=htm --iirds.metadatahandler=shortdesc+subjectscheme "--iirds.metadata.file=C:/Project/metadata.rdf"
```

## `iirds-subjectscheme`: parameters

| Parameter | Allowed values / value format | Default | Description |
| --- | --- | --- | --- |
| `iirds.language` | Exact XML language-tag string present in the vocabulary, for example `en` or `de`; other strings are accepted | Input root `xml:lang`, then `en` | Overrides automatic language selection, selects preferred labels and descriptions, and sets output `xml:lang`. Matching is exact: `de-DE` does not automatically match `de`. |

Labels prefer SKOS `prefLabel` in the requested language, then RDFS `label` in that
language, then available SKOS/RDFS labels in another language, then an identifier.
Descriptions prefer matching SKOS definitions, then matching RDFS comments, then
available definitions/comments. This selects existing text; it does not translate
the source. Unknown language strings therefore fall back to available labels.

The generated DITA uses class, instance, and property keys. Instance keys support
metadata assignment; property keys are vocabulary references. The complete bundled
manifest is recommended for authoring; individual domain files can refer to Core
classes defined outside that file.

```powershell
dita -i C:/dita-ot/plugins/org.iirds.dita.package/schemas/iirds-1.3.xml -f iirds-subjectscheme -o out/taxonomy --iirds.language=de
```

## `iirds-schema-html`: parameters

| Parameter | Allowed values / value format | Default | Description |
| --- | --- | --- | --- |
| `iirds.language` | Exact XML language-tag string such as `en` or `de`; other strings are accepted | Input root `xml:lang`, then `en` | Overrides automatic detection and uses the same label/description selection as `iirds-subjectscheme` and sets the HTML `lang` value. Fixed page headings remain English. |
| `iirds.schema.css` | Stylesheet URL or relative URL, for example `schema.css`, `styles/reference.css`, or `https://example.org/reference.css` | `schema.css` | Writes the value into the HTML stylesheet link. A custom file is not copied; make it available at that URL relative to `index.html`, or use a reachable absolute URL. The default `schema.css` is still written alongside the HTML. |

`args.css`, `args.copycss`, `args.outext`, and other HTML5 publication parameters do
not configure this native HTML reference. Its output filename remains `index.html`.

```powershell
dita -i C:/dita-ot/plugins/org.iirds.dita.package/schemas/iirds-handover.rdf -f iirds-schema-html -o out/handover --iirds.language=de --iirds.schema.css=https://example.org/reference.css
```

## `iirds`: inherited HTML5 parameters

The table lists every parameter declared by DITA-OT 4.4.2's HTML5 descriptor except
`args.outext`, which is documented above. They control HTML5 inside the publication
archive, not the native RDF transformations. A default of **Not declared** means
the descriptor does not specify a value; the toolkit/XSLT or project may supply one.

| Parameter | Allowed values / value format | Default when omitted | What it does |
| --- | --- | --- | --- |
| `args.artlbl` | `yes`; `no` | `no` | Specifies whether to generate a label for each image; the label will contain the image file name. |
| `args.copycss` | `yes`; `no` | `no` | Specifies whether to copy the custom .css file to the output directory. |
| `args.css` | CSS filename, local path, or URL as supported by HTML5; use `args.cssroot` for its local source directory | No custom stylesheet | Adds a custom stylesheet reference to the published HTML5. Use `args.copycss=yes` to package a local stylesheet. |
| `args.csspath` | Relative output directory such as `css`, or an HTTP(S) stylesheet directory URL | Output root | Sets the stylesheet reference/copy location. A local relative directory is inside the content part of the iiRDS archive. |
| `args.cssroot` | Directory containing the custom CSS file | No separate CSS root | Locates the source stylesheet when `args.css` names a local file. |
| `args.dita.locale` | String; see description | Not declared | Specifies the language locale file to use for sorting index entries. |
| `args.ftr` | Path to a readable file | Not declared | Specifies an XML file that contains content for a running footer. |
| `args.gen.default.meta` | `yes`; `no` | `no` | Generate metadata for parental control scanners, meta elements with name="security" and name="Robots". |
| `args.hdf` | Path to a readable file | Not declared | Specifies an XML file that contains content to be placed in the document head. |
| `args.hdr` | Path to a readable file | Not declared | Specifies an XML file that contains content for a running header. |
| `args.hide.parent.link` | `yes`; `no` | `no` | Specifies whether to hide links to parent topics in the HTML5 output. |
| `args.html5.classattr` | `yes`; `no` | `yes` | Specifies whether to include the DITA class ancestry inside the HTML5 elements. |
| `args.html5.contenttarget` | `contentwin` | `contentwin` | Specifies the value of the @target attribute on the &lt;base&gt; element in the TOC file. |
| `html5.toc.generate` | `yes`; `no` | `yes` | Generate TOC file from the DITA map. |
| `args.html5.toc` | `index` | `index` | Specifies the base name of the TOC file. |
| `args.html5.toc.class` | String; see description | Not declared | Specifies the value of the @class attribute on the &lt;body&gt; element in the TOC file. |
| `args.html5.toc.xsl` | Path to a readable XSLT stylesheet | Bundled HTML5 TOC stylesheet | Replaces the transformation that creates the HTML5 table of contents. |
| `args.indexshow` | `yes`; `no` | `no` | Specifies whether the content of &lt;indexterm&gt; elements are rendered in the output. |
| `args.xsl` | Path to a readable XSLT stylesheet | Bundled HTML5 topic stylesheet | Replaces the HTML5 topic rendering stylesheet. The custom stylesheet must produce the files expected by iiRDS rendition metadata. |
| `nav-toc` | `none`: No TOC; `partial`: Partial TOC that shows the current topic; `full`: Full TOC | `none` | Specifies whether to generate a navigation TOC in topic pages. |

For a self-contained package, use a local custom stylesheet with `args.copycss=yes`:

```powershell
dita -i manual.ditamap -f iirds -o out/styled --args.css=project.css --args.cssroot=C:/Project/styles --args.csspath=css --args.copycss=yes --nav-toc=full
```

`args.css` and `iirds.schema.css` configure different output pipelines. Likewise,
`default.language` selects the DITA publication language and `iirds.language`
selects the native RDF vocabulary language. They are not aliases.

## `iirds`: inherited common DITA-OT parameters

This is the full non-stage parameter inventory from the 4.4.2 abstract `base`
descriptor. CLI aliases are preferred for input, output, transformation, filters,
resources, and temporary directory. These DITA preprocessing/rendering parameters
do not add DITA preprocessing to the two native RDF transformations.

| Parameter | Allowed values / value format | Default when omitted | What it does |
| --- | --- | --- | --- |
| `args.gen.task.lbl` | `YES`, `NO` (uppercase) | Not declared | Controls generated headings in task sections. Existing explicit section titles remain authored content. |
| `args.rellinks` | `none`, `all`, `noparent`, `nofamily` | Toolkit standard related-link set | Selects rendered related links: none; all; without parent/ancestor; or without family relationships. With no value, the toolkit uses its standard set, which differs from explicit `all`. |
| `args.debug` | `yes`, `no` | `no` | Deprecated logging parameter. Use the command-line `--debug` switch instead. |
| `args.draft` | `yes`; `no` | `no` | Specifies whether the content of &lt;draft-comment&gt; and &lt;required-cleanup&gt; elements is included in the output. |
| `args.figurelink.style` | `NUMBER`, `TITLE`, `NUMTITLE` | `NUMBER` | Formats generated figure references using their number, title, or number and title. |
| `args.filter` | Readable DITAVAL file path; prefer `--filter=FILE` | None | Includes, excludes, or flags DITA content using a filter file. |
| `args.grammar.cache` | `yes`; `no` | `yes` | Specifies whether the grammar-caching feature of the XML parser is used. |
| `args.input` | Readable DITA map or topic path; CLI alias `-i` | Required | Selects the publication input. Native RDF transformations use the different input types described above. |
| `args.input.dir` | Directory path | Not declared | Specifies the base directory for your documentation project. |
| `args.resources` | Readable resource file path(s), normally supplied with repeatable `--resource=FILE` | None | Adds resource documents for DITA preprocessing/key resolution. |
| `args.output.base` | Filename stem without an extension | Not declared | Supplies a base output name to toolkit processing that consumes it. This plug-in has no separate archive-name parameter; its ZIP target uses the toolkit map filename root. |
| `args.tablelink.style` | `NUMBER`, `TITLE`, `NUMTITLE` | `NUMBER` | Formats generated table references using their number, title, or number and title. |
| `link-crawl` | `map`; `topic` | `topic` | Specifies whether to crawl only those topic links found in maps, or all discovered topic links. |
| `clean.temp` | `yes`; `no` | `yes` | Specifies whether DITA-OT deletes the files in the temporary directory after it finishes a build. |
| `dita.dir` | Absolute path to the toolkit installation | The toolkit being invoked | Identifies the toolkit installation. Normally leave this launcher-managed value unchanged. |
| `dita.temp.dir` | Absolute directory path | Toolkit temporary directory with generated build identifier | Sets the working directory for intermediate build files. |
| `dita.input.valfile` | Readable DITAVAL file path | None | Deprecated filter-file parameter. Use `--filter=FILE` instead. |
| `filter-stage` | `early`; `late` | `early` | Specifies whether filtering is done before all other processing, or after key and conref processing. |
| `force-unique` | `true`; `false` | `false` | Generate copy-to attributes to duplicate topicref elements. |
| `generate.copy.outer` | `1`: Do not generate output for content that is located outside the DITA map directory.; `3`: Shift the output directory so that it contains all output for the publication. | `1` | Adjust how output is generated for content that is located outside the directory containing the input resource (DITA map or topic). |
| `onlytopic.in.map` | `true`; `false` | `false` | Specifies whether files that are linked to, or referenced with a @conref attribute, generate output. |
| `outer.control` | `fail`: Fail quickly if files are going to be generated or copied outside of the directory.; `warn`: Complete the operation if files will be generated or copied outside of the directory, but log a warning.; `quiet`: Quietly finish without generating warnings or errors. | `warn` | Specifies whether to warn or fail if content is located outside the directory containing the input resource (DITA map or topic). |
| `output.dir` | Directory path; CLI alias `-o` | Toolkit output directory, normally `<DITA-OT>/out` | Selects the output directory. Prefer a separate directory for each publication or schema transformation. |
| `root-chunk-override` | String; see description | Not declared | Override for map chunk attribute value. |
| `transtype` | `iirds`, `iirds-subjectscheme`, or `iirds-schema-html`; CLI alias `-f` | Required | Selects the transformation. The remaining entries in this inherited table apply to `iirds`, unless explicitly listed as common invocation options. |
| `validate` | `true`; `false` | `true` | Specifies whether DITA-OT validates the content. |
| `generate-debug-attributes` | `true`: Enables generation of debugging attributes; `false`: Disables generation of debugging attributes | `true` | Specifies whether the @xtrf and @xtrc debugging attributes are generated in the temporary files. |
| `processing-mode` | `strict`: When an error is encountered, DITA-OT stops processing; `lax`: When an error is encountered, DITA-OT attempts to recover from it; `skip`: When an error is encountered, DITA-OT continues processing but does not attempt error recovery | `lax` | Specifies how DITA-OT handles errors and error recovery. |
| `conserve-memory` | `true`; `false` | `false` | Conserve memory at the expense of processing speed. |
| `default.language` | Non-empty language tag such as `en`, `de`, or `en-US` | Input root `xml:lang`, then `en` | For this plug-in, an explicit value overrides generated publication root languages and iiRDS language metadata. When omitted, language is detected from the input topic/map/bookmap. This does not translate authored text or select native RDF reference labels. |
| `remove-broken-links` | `true`; `false` | `false` | Remove broken related links. |
| `result.rewrite-rule.xsl` | Path to an XSLT filename-rewriting stylesheet | None | Customizes generated filenames. Custom rewriting has not been verified against the plug-in's rendition paths; check the resulting package before relying on it. |
| `result.rewrite-rule.class` | Fully qualified Java class name available to the toolkit | None | Supplies a custom filename-rewriting class. Custom rewriting has not been verified against the plug-in's rendition paths. |
| `store-type` | `file`; `memory` | `file` | Temporary file store type. |
| `parallel` | `true`; `false` | `false` | Run processes in parallel when possible. |

### Advanced preprocessing stage switches

These are the remaining parameters declared by the base descriptor. Each accepts
the literal values shown. They enable/disable the named toolkit stage when that
stage participates in the selected pipeline. `iirds` inherits the HTML5 pipeline,
which uses `preprocess2`; a switch for an unused stage has no effect. Leave these
defaults in place for normal publishing: skipping key/conref/chunk/profile stages
can change content and metadata together.

| Parameter | Allowed values / value format | Default when omitted | What it does |
| --- | --- | --- | --- |
| `build-step.clean-temp` | `true`, `false` | `true` | Runs the toolkit temporary-file cleanup stage. |
| `build-step.branch-filter` | `true`, `false` | `true` | Applies branch-specific DITAVAL filtering from map references. |
| `build-step.chunk` | `true`, `false` | `true` | Applies map chunk instructions to combine or split topic output. |
| `build-step.clean-preprocess` | `true`, `false` | `true` | Removes preprocessing-only markup from intermediate DITA. |
| `build-step.coderef` | `true`, `false` | `true` | Resolves references to external source-code fragments. |
| `build-step.conref` | `true`, `false` | `true` | Resolves content references in intermediate DITA. |
| `build-step.copy-flag` | `true`, `false` | `true` | Copies images used for profiling/flagging to the output. |
| `build-step.copy-html` | `true`, `false` | `true` | Copies referenced HTML resources to the output. |
| `build-step.copy-image` | `true`, `false` | `true` | Copies referenced image resources to the output. |
| `build-step.keyref` | `true`, `false` | `true` | Resolves DITA key references. |
| `build-step.map-profile` | `true`, `false` | `true` | Applies filtering and flagging to map content. |
| `build-step.maplink` | `true`, `false` | `true` | Generates topic relationship links from map relationships. |
| `build-step.mapref` | `true`, `false` | `true` | Resolves referenced maps into the publication structure. |
| `build-step.move-meta-entries` | `true`, `false` | `true` | Propagates applicable map metadata during preprocessing. |
| `build-step.normalize-codeblock` | `true`, `false` | `true` | Normalizes code-block whitespace/indentation where requested. |
| `build-step.profile` | `true`, `false` | `false` | Controls the profiling stage of pipelines that invoke it. |
| `build-step.topic-profile` | `true`, `false` | `false` | Applies filtering and flagging to topic content. |
| `build-step.topicpull` | `true`, `false` | `true` | Resolves cross-reference text and other topic information pulled from targets. |

## Native manifest format

The `schemas` manifest is an alternative input file, not a command-line parameter:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<schemas version="1.3">
  <schema href="iirds-core.rdf"/>
  <schema href="iirds-machinery.rdf"/>
  <schema href="iirds-software.rdf"/>
  <schema href="iirds-handover.rdf"/>
  <schema href="iirds-skos.rdf"/>
</schemas>
```

Each `href` resolves relative to the manifest file. Use readable RDF/XML files.
Invalid XML, an unsupported root, or a cyclic selected vocabulary hierarchy causes
the native subject-scheme transformation to fail. The manifest's `version` attribute
is descriptive; it does not convert or validate a different schema version. Use
the bundled 1.3 manifest and files for iiRDS 1.3 work.

## Source and scope of this reference

Checked against `plugin.xml`, `build_dita2iirds_template.xml`, the runtime handler
providers and configuration, and `xsl/schema-*.xsl` in this project's plug-in
sources, plus the installed DITA-OT 4.4.2 `org.dita.html5` and `org.dita.base`
descriptors and build initialization. In a source checkout these plug-in files are
under `org.iirds.dita.ot.plugin/src/plugin/`; in the installed package they are at
the package root. Inherited descriptor descriptions are based on the Apache-2.0
DITA-OT sources; see the toolkit's licence and notices.

Additional host extensions can register their own parameters and handler names.
Internal Ant/module values such as `iirds.processing`, `METADATAFILE`, and
`CONTENTPATH` are implementation details, not additional documented user options.
This reference describes accepted/usable parameter values; it does not claim every
combination of toolkit customization parameters has been tested with iiRDS output.
