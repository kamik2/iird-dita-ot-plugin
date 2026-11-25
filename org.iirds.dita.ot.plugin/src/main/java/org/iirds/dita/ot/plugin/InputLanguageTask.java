/* Local additions, 2026. Licensed under Apache-2.0. */
package org.iirds.dita.ot.plugin;

import java.io.File;
import java.io.InputStream;
import java.nio.file.Files;
import javax.xml.XMLConstants;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamReader;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Task;

/** Select a publication language before DITA-OT initializes immutable defaults. */
public final class InputLanguageTask extends Task {
    private File file;

    public void setFile(File file) { this.file = file; }

    static String readLanguage(File file) throws Exception {
        XMLInputFactory factory = XMLInputFactory.newFactory();
        factory.setProperty(XMLInputFactory.SUPPORT_DTD, false);
        factory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);
        try (InputStream stream = Files.newInputStream(file.toPath())) {
            XMLStreamReader reader = factory.createXMLStreamReader(stream);
            try {
                while (reader.hasNext()) {
                    if (reader.next() == XMLStreamConstants.START_ELEMENT) {
                        String language = reader.getAttributeValue(XMLConstants.XML_NS_URI, "lang");
                        return language == null || language.isBlank() ? "en" : language.trim();
                    }
                }
                return "en";
            } finally { reader.close(); }
        }
    }

    @Override public void execute() {
        String explicit = getProject().getProperty("default.language");
        try {
            boolean override = explicit != null && !explicit.isBlank();
            String selected = override ? explicit.trim() : readLanguage(file);
            getProject().setNewProperty("default.language", selected);
            getProject().setNewProperty("iirds.language.selected", selected);
            if (override) getProject().setNewProperty("iirds.language.override", selected);
        } catch (Exception e) {
            throw new BuildException("Cannot determine input XML language from " + file, e, getLocation());
        }
    }
}
