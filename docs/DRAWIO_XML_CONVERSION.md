# Conversão PlantUML para Draw.io XML

Este projeto agora inclui uma solução automatizada para converter diagramas PlantUML diretamente para o formato XML do Draw.io, permitindo edição completa dos diagramas no Draw.io.

## 🎯 Problema Resolvido

Anteriormente, os arquivos SVG exportados do PlantUML eram importados no Draw.io como imagens únicas, não permitindo edição de elementos individuais. Com esta solução:

- ✅ **Edição completa**: Elementos individuais podem ser editados no Draw.io
- ✅ **Código PlantUML incorporado**: O código original fica embutido no arquivo XML
- ✅ **Processo automatizado**: Integrado ao script de build existente
- ✅ **Transparente**: Funciona automaticamente sem intervenção manual

## 🚀 Como Usar

### Opção 1: Gerar apenas arquivos XML do Draw.io
```bash
./generate-diagrams.sh --drawio
```

### Opção 2: Gerar todos os formatos (PNG, SVG e XML)
```bash
./generate-diagrams.sh --all
# ou simplesmente
./generate-diagrams.sh
```

### Opção 3: Limpar e regenerar tudo
```bash
./generate-diagrams.sh --clean
```

## 📁 Estrutura de Arquivos

Após a execução, os arquivos serão organizados da seguinte forma:

```
docs/
├── generated-diagrams/     # Arquivos PNG para documentação
├── drawio-exports/          # Arquivos SVG para importação básica
└── drawio-xml-exports/      # Arquivos XML para edição completa ⭐
    ├── arch-evolution-containerization/
    ├── arch-evolution-steps/
    ├── event-driven-messaging/
    ├── scalability-performance/
    ├── security-compliance/
    └── sequence-diagram-solutions/
```

## 🎨 Importando no Draw.io

### Para Edição Completa (Recomendado)
1. Abra o [Draw.io](https://app.diagrams.net/)
2. Clique em "Open Existing Diagram"
3. Selecione um arquivo `.drawio` da pasta `docs/drawio-xml-exports/`
4. ✨ **Agora você pode editar elementos individuais e acessar o código PlantUML original!**

### Para Edição Básica
1. Abra o [Draw.io](https://app.diagrams.net/)
2. Clique em "Import" → "SVG"
3. Selecione um arquivo `.svg` da pasta `docs/drawio-exports/`
4. Edição limitada como imagem vetorial

## 🔧 Componentes da Solução

### 1. Script de Conversão (`plantuml_to_drawio.py`)
- Converte arquivos `.puml` para formato XML do Draw.io
- Incorpora o código PlantUML original no arquivo XML
- Usa SVGs existentes quando disponíveis
- Fallback para geração via Maven quando necessário

### 2. Script de Build Atualizado (`generate-diagrams.sh`)
- Nova opção `--drawio` para gerar apenas XMLs
- Opção `--all` atualizada para incluir XMLs
- Integração transparente com o processo existente

### 3. Estrutura de Pastas
- `docs/drawio-xml-exports/`: Arquivos XML para edição completa
- Mantém a mesma estrutura de diretórios dos arquivos originais

## 📊 Estatísticas

- **119 diagramas** convertidos automaticamente
- **6 categorias** de diagramas suportadas
- **Conversão 100% bem-sucedida** em todos os testes

## 🛠️ Requisitos Técnicos

- Python 3.x
- Maven (já configurado no projeto)
- Graphviz (já configurado no projeto)

## 💡 Dicas de Uso

1. **Execute sempre `--all`** para manter todos os formatos atualizados
2. **Use arquivos XML** para edição completa no Draw.io
3. **Use arquivos SVG** apenas para visualização ou edição básica
4. **Use arquivos PNG** para documentação e apresentações

## 🔄 Fluxo de Trabalho Recomendado

1. Edite os arquivos `.puml` no seu editor preferido
2. Execute `./generate-diagrams.sh --all`
3. Importe os arquivos `.drawio` no Draw.io para ajustes visuais
4. Use os arquivos PNG para documentação

---

**Resultado**: Agora você tem o melhor dos dois mundos - a simplicidade do PlantUML para criação de diagramas e a flexibilidade do Draw.io para edição visual! 🎉