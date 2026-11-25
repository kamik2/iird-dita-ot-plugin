/* Local additions, 2026. Apache-2.0. */
package org.iirds.rdf;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.RDFS;
import org.junit.jupiter.api.Test;
class SchemaCoverageTest {
 @Test void loadsAllFiveOfficialSchemas() {
  Model m = RDFConstants.getRDFSModel();
  assertTrue(m.contains(m.getResource(IirdsConstants.iiRDS_URI + "Topic"), RDF.type, RDFS.Class));
  assertTrue(m.containsResource(m.getResource(IirdsConstants.iiRDS_Mch_URI + "HardwareTool")));
  assertTrue(m.containsResource(m.getResource(IirdsConstants.iiRDS_Sft_URI + "Deployment")));
  assertTrue(m.containsResource(m.getResource(IirdsConstants.iiRDS_Hov_URI + "DocumentCategory")));
  assertTrue(m.contains(null, m.getProperty("http://www.w3.org/2004/02/skos/core#prefLabel")));
  assertEquals("1.3", IirdsConstants.IIRDS_VERSION);
 }
 @Test void bindsStructuredOverlaySubjectsAndObjects() {
  Model target = ModelFactory.createDefaultModel(), extra = ModelFactory.createDefaultModel();
  Resource input = target.createResource("urn:test:document"), pkg = target.createResource("urn:test:package");
  Resource placeholder = extra.createResource("urn:iirds:input");
  placeholder.addProperty(extra.createProperty(IirdsConstants.iiRDS_URI + "revision"), "Überarbeitung A");
  placeholder.addProperty(extra.createProperty(IirdsConstants.iiRDS_URI + "is-part-of-package"), extra.createResource("urn:iirds:package"));
  Resource identity = extra.createResource().addProperty(extra.createProperty(IirdsConstants.iiRDS_URI + "identifier"), "ID-42");
  placeholder.addProperty(extra.createProperty(IirdsConstants.iiRDS_URI + "has-identity"), identity);
  MetadataOverlay.merge(target, extra, input, pkg);
  assertTrue(target.contains(input, target.createProperty(IirdsConstants.iiRDS_URI + "revision"), "Überarbeitung A"));
  assertTrue(target.contains(input, target.createProperty(IirdsConstants.iiRDS_URI + "is-part-of-package"), pkg));
  assertTrue(target.contains(identity, target.createProperty(IirdsConstants.iiRDS_URI + "identifier"), "ID-42"));
  assertFalse(target.containsResource(target.createResource("urn:iirds:input")));
 }
}
