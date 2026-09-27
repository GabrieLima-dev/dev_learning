package dev.learning;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class InfrastructureTest {

    @Test
    void executesTestsWithTheConfiguredJavaLevel() {
        assertTrue(Runtime.version().feature() >= 25);
    }
}
