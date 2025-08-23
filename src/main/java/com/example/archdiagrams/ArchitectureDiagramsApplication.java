package com.example.archdiagrams;

/**
 * Classe principal do projeto de diagramas de arquitetura.
 * Este projeto utiliza PlantUML e C4 Model para documentação de arquitetura.
 */
public class ArchitectureDiagramsApplication {
    
    public static void main(String[] args) {
        System.out.println("Architecture Diagrams Project");
        System.out.println("Utilize os diagramas na pasta /diagrams para documentar sua arquitetura.");
    }
    
    /**
     * Método utilitário para validar se um diagrama está bem formado.
     * @param diagramPath caminho para o arquivo .puml
     * @return true se o diagrama é válido
     */
    public boolean validateDiagram(String diagramPath) {
        // Implementação futura para validação de diagramas
        return diagramPath != null && diagramPath.endsWith(".puml");
    }
}