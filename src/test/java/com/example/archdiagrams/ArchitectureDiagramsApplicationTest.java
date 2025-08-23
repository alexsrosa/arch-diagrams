package com.example.archdiagrams;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Testes unitários para a classe ArchitectureDiagramsApplication.
 */
class ArchitectureDiagramsApplicationTest {
    
    @Test
    void testValidateDiagram() {
        ArchitectureDiagramsApplication app = new ArchitectureDiagramsApplication();
        
        // Teste com arquivo válido
        assertTrue(app.validateDiagram("example.puml"));
        
        // Teste com arquivo inválido
        assertFalse(app.validateDiagram("example.txt"));
        
        // Teste com null
        assertFalse(app.validateDiagram(null));
    }
    
    @Test
    void testMainMethod() {
        // Teste simples para verificar se o método main executa sem erros
        assertDoesNotThrow(() -> {
            ArchitectureDiagramsApplication.main(new String[]{});
        });
    }
}