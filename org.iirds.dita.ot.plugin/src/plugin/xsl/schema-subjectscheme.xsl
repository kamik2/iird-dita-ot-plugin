<?xml version="1.0" encoding="UTF-8"?>
<!-- Local additions, 2026. Apache-2.0. -->
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:f="urn:iirds:transform" exclude-result-prefixes="#all">
 <xsl:import href="schema-common.xsl"/>
 <xsl:output method="xml" indent="yes" encoding="UTF-8" doctype-public="-//OASIS//DTD DITA Subject Scheme Map//EN" doctype-system="subjectScheme.dtd"/>
 <xsl:template match="/">
  <xsl:if test="some $uri in $uris satisfies not(f:acyclic($uri,()))"><xsl:message terminate="yes">Cyclic vocabulary hierarchy.</xsl:message></xsl:if>
  <subjectScheme xml:lang="{$iirds.language}">
   <title>iiRDS vocabulary subject scheme</title>
   <xsl:comment>Generated from RDF/XML. Schema copyright and CC BY-ND 4.0 notices remain in the source files. Properties are reference keys and are not metadata instances.</xsl:comment>
   <xsl:for-each select="distinct-values($uris ! f:parent(.))[not(.=$uris)]">
    <subjectdef keys="{f:key(.)}"><topicmeta><navtitle><xsl:value-of select="substring-after(.,'#')"/></navtitle><resourceid appid="{.}" appname="class-iri"/></topicmeta>
     <xsl:variable name="parent" select="."/><xsl:for-each select="$uris[f:parent(.)=$parent]"><xsl:call-template name="subject"><xsl:with-param name="uri" select="."/></xsl:call-template></xsl:for-each>
    </subjectdef>
   </xsl:for-each>
   <xsl:for-each select="$uris[empty(f:parent(.))]"><xsl:call-template name="subject"><xsl:with-param name="uri" select="."/></xsl:call-template></xsl:for-each>
  </subjectScheme>
 </xsl:template>
 <xsl:template name="subject"><xsl:param name="uri"/><xsl:param name="seen" select="()"/>
  <xsl:if test="$uri=$seen"><xsl:message terminate="yes">Cyclic vocabulary hierarchy.</xsl:message></xsl:if>
  <subjectdef keys="{string-join((f:key($uri), if (starts-with(f:key($uri), 'iirdsSft.')) then replace(f:key($uri), '^iirdsSft\.', 'iirdSft.') else ()), ' ')}"><topicmeta><navtitle><xsl:value-of select="f:label($uri)"/></navtitle>
   <xsl:if test="f:description($uri) != ''"><shortdesc><xsl:value-of select="f:description($uri)"/></shortdesc></xsl:if>
   <resourceid appid="{$uri}" appname="{f:kind($uri)}"/>
  </topicmeta>
  <xsl:for-each select="$uris[f:parent(.)=$uri]"><xsl:call-template name="subject"><xsl:with-param name="uri" select="."/><xsl:with-param name="seen" select="($seen,$uri)"/></xsl:call-template></xsl:for-each>
  </subjectdef>
 </xsl:template>
</xsl:stylesheet>
