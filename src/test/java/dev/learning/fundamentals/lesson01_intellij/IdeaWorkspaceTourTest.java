package dev.learning.fundamentals.lesson01_intellij;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class IdeaWorkspaceTourTest {

    @Test
    void returnsTheMessageShownByTheExampleProgram() {
        assertEquals("Projeto pronto para explorar no IntelliJ IDEA.", IdeaWorkspaceTour.welcomeMessage());
    }

    @Test
    void exposesASecondTestForRunningTheWholeClass() {
        assertEquals("Projeto pronto para explorar no IntelliJ IDEA.", IdeaWorkspaceTour.welcomeMessage());
    }
}
