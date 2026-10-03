package dev.learning.fundamentals.lesson02_git;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class GitWorkspaceMarkerTest {

    @Test
    void keepsThePracticeMarkerAvailable() {
        assertEquals("Prática de Git pronta para versionar.", GitWorkspaceMarker.practiceStatus());
    }
}
