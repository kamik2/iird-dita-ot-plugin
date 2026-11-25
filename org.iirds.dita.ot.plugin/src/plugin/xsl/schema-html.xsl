<?xml version="1.0" encoding="UTF-8"?>
<!-- Local additions, 2026. Apache-2.0. -->
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:f="urn:iirds:transform" exclude-result-prefixes="#all">
 <xsl:import href="schema-common.xsl"/>
 <xsl:output method="html" html-version="5" indent="yes" encoding="UTF-8"/>
 <xsl:param name="iirds.schema.css" select="'schema.css'"/>
 <xsl:template match="/"><html lang="{$iirds.language}"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>iiRDS vocabulary reference</title><link rel="stylesheet" href="{$iirds.schema.css}"/></head><body><main>
 <h1>iiRDS vocabulary reference</h1><p>Generated from the supplied RDF/XML. This reference does not validate publication conformance.</p>
 <p>Source vocabulary: Gesellschaft für Technische Kommunikation – tekom Deutschland e.V., <a href="https://www.iirds.org/materials/version-13">iiRDS 1.3</a>, <a href="https://creativecommons.org/licenses/by-nd/4.0/">CC BY-ND 4.0</a>.</p>
 <nav aria-label="Vocabulary terms"><ul><xsl:for-each select="$uris"><li><a href="#{f:key(.)}"><xsl:value-of select="f:label(.)"/></a></li></xsl:for-each></ul></nav>
 <xsl:for-each select="$uris"><section id="{f:key(.)}"><h2><xsl:value-of select="f:label(.)"/></h2><p><code><xsl:value-of select="."/></code></p><p><xsl:value-of select="f:kind(.)"/></p><p><xsl:value-of select="f:description(.)"/></p><dl>
 <xsl:for-each-group select="f:nodes(.)/*" group-by="concat(namespace-uri(.),local-name(.))"><dt><xsl:value-of select="name()"/></dt><dd><ul><xsl:for-each select="current-group()"><li><xsl:if test="@xml:lang"><span lang="{@xml:lang}"><xsl:value-of select="@xml:lang"/>: </span></xsl:if><xsl:value-of select="(@*:resource,.)[1]"/></li></xsl:for-each></ul></dd></xsl:for-each-group>
 </dl></section></xsl:for-each></main></body></html></xsl:template>
</xsl:stylesheet>
