/* Local additions, 2026. Apache-2.0. */
package org.iirds.dita.ot.plugin;

import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.Files;
import java.nio.file.Path;
import org.apache.tools.ant.Project;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class InputLanguageTaskTest {
    @TempDir Path temp;

    @Test void readsTopicMapAndBookmapWithoutResolvingDtd() throws Exception {
        for (String name : new String[] {"topic", "map", "bookmap"}) {
            Path file = temp.resolve(name + ".xml");
            Files.writeString(file, "<!DOCTYPE " + name + " SYSTEM 'missing.dtd'><" + name + " xml:lang='de-AT'/>");
            assertEquals("de-AT", InputLanguageTask.readLanguage(file.toFile()));
        }
    }

    @Test void defaultsMissingAndBlankLanguageToEnglish() throws Exception {
        for (String attribute : new String[] {"", " xml:lang='  '"}) {
            Path file = temp.resolve("input.xml");
            Files.writeString(file, "<map" + attribute + "/>");
            assertEquals("en", InputLanguageTask.readLanguage(file.toFile()));
        }
    }

    @Test void explicitExportValueWinsOverInput() throws Exception {
        Path file = temp.resolve("input.xml");
        Files.writeString(file, "<map xml:lang='de'/>");
        Project project = new Project();
        project.setUserProperty("default.language", "fr");
        InputLanguageTask task = new InputLanguageTask();
        task.setProject(project); task.setFile(file.toFile()); task.execute();
        assertEquals("fr", project.getProperty("iirds.language.selected"));
        assertEquals("fr", project.getProperty("iirds.language.override"));
        assertEquals("fr", project.getProperty("default.language"));
    }

    @Test void detectedValueBecomesDefaultWithoutForcingTopicLanguages() throws Exception {
        Path file = temp.resolve("input.xml");
        Files.writeString(file, "<bookmap xml:lang='de'/>");
        Project project = new Project();
        InputLanguageTask task = new InputLanguageTask();
        task.setProject(project); task.setFile(file.toFile()); task.execute();
        assertEquals("de", project.getProperty("default.language"));
        assertNull(project.getProperty("iirds.language.override"));
    }
}
