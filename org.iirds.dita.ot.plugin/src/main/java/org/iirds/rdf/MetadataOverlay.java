/* Local additions, 2026. Licensed under Apache-2.0. */
package org.iirds.rdf;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.Statement;

/** Explicit RDF metadata, including structured values not expressible by taxonomy tags. */
public final class MetadataOverlay {
    private MetadataOverlay() { }

    /** Merge a supplied graph, binding two reserved IRIs to the generated input and package. */
    public static void merge(Model target, Model overlay, Resource input, Resource pkg) {
        Model bound = ModelFactory.createDefaultModel();
        bound.setNsPrefixes(overlay.getNsPrefixMap());
        for (Statement stmt : overlay.listStatements().toList()) {
            Resource subject = bind(stmt.getSubject(), input, pkg);
            RDFNode object = stmt.getObject().isResource()
                    ? bind(stmt.getResource(), input, pkg) : stmt.getObject();
            bound.add(subject, stmt.getPredicate(), object);
        }
        target.add(bound);
        target.setNsPrefixes(bound.getNsPrefixMap());
    }

    private static Resource bind(Resource resource, Resource input, Resource pkg) {
        if (resource.isURIResource()) {
            if ("urn:iirds:input".equals(resource.getURI())) return input;
            if ("urn:iirds:package".equals(resource.getURI())) return pkg;
        }
        return resource;
    }
}
