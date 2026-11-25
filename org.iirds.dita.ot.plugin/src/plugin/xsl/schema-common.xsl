<?xml version="1.0" encoding="UTF-8"?>
<!-- Local additions, 2026: native RDF/XML vocabulary transformations. Apache-2.0. -->
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:skos="http://www.w3.org/2004/02/skos/core#"
 xmlns:f="urn:iirds:transform" exclude-result-prefixes="#all">
 <xsl:param name="iirds.language" select="'en'"/>
 <xsl:variable name="graph" as="document-node()"><xsl:document><rdf:RDF>
  <xsl:choose><xsl:when test="/schemas">
   <xsl:for-each select="/schemas/schema"><xsl:copy-of select="doc(resolve-uri(@href, base-uri(.)))/rdf:RDF/*"/></xsl:for-each>
  </xsl:when><xsl:when test="/rdf:RDF"><xsl:copy-of select="/rdf:RDF/*"/></xsl:when>
  <xsl:otherwise><xsl:message terminate="yes">Expected RDF/XML or an iiRDS schema manifest.</xsl:message></xsl:otherwise></xsl:choose>
 </rdf:RDF></xsl:document></xsl:variable>
 <xsl:key name="term" match="rdf:RDF/*" use="@rdf:about"/>
 <xsl:variable name="uris" select="sort(distinct-values($graph/rdf:RDF/*/@rdf:about))"/>
 <xsl:function name="f:nodes" as="element()*"><xsl:param name="uri"/><xsl:sequence select="key('term',$uri,$graph)"/></xsl:function>
 <xsl:function name="f:kind" as="xs:string"><xsl:param name="uri"/>
  <xsl:sequence select="if (f:nodes($uri)[self::rdfs:Class or rdf:type/@rdf:resource='http://www.w3.org/2000/01/rdf-schema#Class']) then 'class-iri' else if (f:nodes($uri)[self::rdf:Property or rdf:type/@rdf:resource='http://www.w3.org/1999/02/22-rdf-syntax-ns#Property']) then 'property-iri' else 'instance-iri'"/>
 </xsl:function>
 <xsl:function name="f:key" as="xs:string"><xsl:param name="uri"/>
  <xsl:variable name="ns" select="substring-before($uri,'#')"/>
  <xsl:sequence select="if (not(contains($uri,'#'))) then concat('custom.',encode-for-uri($uri)) else concat(if ($ns='http://iirds.tekom.de/iirds') then 'iirds.' else if (ends-with($ns,'/machinery')) then 'iirdsMch.' else if (ends-with($ns,'/software')) then 'iirdsSft.' else if (ends-with($ns,'/handover')) then 'iirdsHov.' else concat('custom.',encode-for-uri($ns),'.'),substring-after($uri,'#'))"/>
 </xsl:function>
 <xsl:function name="f:label" as="xs:string"><xsl:param name="uri"/>
  <xsl:variable name="nodes" select="f:nodes($uri)"/>
  <xsl:sequence select="string(($nodes/skos:prefLabel[@xml:lang=$iirds.language],$nodes/rdfs:label[@xml:lang=$iirds.language],$nodes/skos:prefLabel,$nodes/rdfs:label,substring-after($uri,'#'),$uri)[normalize-space(.)][1])"/>
 </xsl:function>
 <xsl:function name="f:description" as="xs:string"><xsl:param name="uri"/>
  <xsl:variable name="nodes" select="f:nodes($uri)"/>
  <xsl:sequence select="normalize-space(($nodes/skos:definition[@xml:lang=$iirds.language],$nodes/rdfs:comment[@xml:lang=$iirds.language],$nodes/skos:definition,$nodes/rdfs:comment)[1])"/>
 </xsl:function>
 <xsl:function name="f:parents" as="xs:string*"><xsl:param name="uri"/>
  <xsl:variable name="nodes" select="f:nodes($uri)"/>
  <xsl:sequence select="if (f:kind($uri)='class-iri') then distinct-values($nodes/rdfs:subClassOf/@rdf:resource/string()) else if (f:kind($uri)='property-iri') then () else distinct-values(($nodes/rdf:type/@rdf:resource/string(),$nodes[not(self::rdf:Description)] ! concat(namespace-uri(.),local-name(.))))"/>
 </xsl:function>
 <xsl:function name="f:parent" as="xs:string?"><xsl:param name="uri"/>
  <xsl:variable name="parents" select="f:parents($uri)[. != $uri]"/>
  <xsl:sequence select="($parents[not(ends-with(.,'DomainEntity'))],$parents)[1]"/>
 </xsl:function>
 <xsl:function name="f:acyclic" as="xs:boolean"><xsl:param name="uri"/><xsl:param name="seen"/>
  <xsl:sequence select="if ($uri=$seen) then false() else if (not(f:parent($uri)=$uris)) then true() else f:acyclic(f:parent($uri),($seen,$uri))"/>
 </xsl:function>
</xsl:stylesheet>
