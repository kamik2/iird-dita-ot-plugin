/* Local additions, 2026. Apache-2.0. */
package org.iirds.dita.ot.plugin;

import static org.junit.jupiter.api.Assertions.*;
import org.dita.dost.pipeline.PipelineHashIO;
import org.iirds.dita.ot.plugin.model.ToCNode;
import org.iirds.dita.ot.plugin.test.TestUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class LanguageExtractorTest {
    @BeforeEach void reset() { Configuration.create(null, null); }

    @Test void missingTopicLanguageInheritsParent() {
        ToCNode parent = new ToCNode(), child = new ToCNode();
        parent.setLanguage("de"); parent.addChild(child);
        new LanguageExtractor().extractLanguage(child, TestUtils.createElement("<concept/>"));
        assertEquals("de", child.getLanguage());
    }

    @Test void authoredLanguageWinsOverParentAndEnglishIsFinalFallback() {
        ToCNode parent = new ToCNode(), child = new ToCNode();
        parent.setLanguage("de"); parent.addChild(child);
        new LanguageExtractor().extractLanguage(child, TestUtils.createElement("<concept xml:lang='es'/>"));
        assertEquals("es", child.getLanguage());
        new LanguageExtractor().extractLanguage(parent, TestUtils.createElement("<map/>"));
        assertEquals("en", parent.getLanguage());
    }

    @Test void exportOverrideWinsOverAuthoredLanguage() {
        PipelineHashIO input = new PipelineHashIO();
        input.setAttribute("LANGUAGEOVERRIDE", "fr");
        Configuration.create(null, input);
        ToCNode node = new ToCNode();
        new LanguageExtractor().extractLanguage(node, TestUtils.createElement("<map xml:lang='de'/>"));
        assertEquals("fr", node.getLanguage());
    }
}
