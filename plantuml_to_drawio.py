#!/usr/bin/env python3
"""
Script para converter diagramas PlantUML para formato XML do Draw.io
Permite edição completa dos diagramas no Draw.io, incluindo elementos individuais
"""

import os
import sys
import subprocess
import base64
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse

def run_plantuml_via_maven(puml_file, output_format='svg'):
    """
    Executa PlantUML via Maven para gerar o diagrama no formato especificado
    """
    try:
        # Cria um arquivo temporário para o diagrama
        import tempfile
        import shutil
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copia o arquivo para o diretório temporário
            temp_puml = os.path.join(temp_dir, 'temp.puml')
            shutil.copy2(puml_file, temp_puml)
            
            # Executa PlantUML via Maven
            if output_format == 'svg':
                cmd = ['mvn', 'com.github.jeluard:plantuml-maven-plugin:generate', 
                       f'-Dplantuml.sourceFiles={temp_puml}', 
                       f'-Dplantuml.outputDirectory={temp_dir}', 
                       '-Dplantuml.format=svg', '-q']
            else:
                cmd = ['mvn', 'com.github.jeluard:plantuml-maven-plugin:generate', 
                       f'-Dplantuml.sourceFiles={temp_puml}', 
                       f'-Dplantuml.outputDirectory={temp_dir}', 
                       f'-Dplantuml.format={output_format}', '-q']
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Lê o arquivo gerado
            output_file = os.path.join(temp_dir, f'temp.{output_format}')
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f"Arquivo de saída não encontrado: {output_file}")
                return None
                
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Maven PlantUML: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def run_plantuml_direct(puml_file, output_format='svg'):
    """
    Executa PlantUML diretamente (se disponível no PATH)
    """
    try:
        cmd = ['plantuml', f'-t{output_format}', '-pipe']
        with open(puml_file, 'r', encoding='utf-8') as f:
            puml_content = f.read()
        
        result = subprocess.run(cmd, input=puml_content, text=True, 
                              capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar PlantUML: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        return None

def run_plantuml(puml_file, output_format='svg'):
    """
    Executa PlantUML usando o método disponível (direto ou via Maven)
    """
    # Tenta primeiro o PlantUML direto
    result = run_plantuml_direct(puml_file, output_format)
    if result is not None:
        return result
    
    # Se não funcionar, tenta via Maven
    print("PlantUML não encontrado no PATH, tentando via Maven...")
    return run_plantuml_via_maven(puml_file, output_format)

def create_drawio_xml(puml_content, svg_content, diagram_name):
    """
    Cria o XML do Draw.io incorporando o código PlantUML e o SVG renderizado
    """
    # Codifica o conteúdo PlantUML em base64
    puml_b64 = base64.b64encode(puml_content.encode('utf-8')).decode('utf-8')
    
    # Codifica o SVG em base64
    svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
    
    # Template XML do Draw.io com PlantUML incorporado
    xml_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="{diagram_name}" agent="PlantUML Converter" version="1.0" etag="plantuml-diagram" type="device">
  <diagram id="plantuml-{diagram_name}" name="{diagram_name}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="plantuml-container" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;imageAspect=0;aspect=fixed;image=data:image/svg+xml,{svg_b64};plantuml={puml_b64};" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="400" height="300" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    
    return xml_template



def convert_puml_to_drawio(puml_file, output_file):
    """
    Converte um arquivo PlantUML para formato XML do Draw.io
    """
    print(f"Convertendo {puml_file} para {output_file}...")
    
    # Lê o conteúdo do arquivo PlantUML
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            puml_content = f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo {puml_file}: {e}")
        return False
    
    # Gera SVG via PlantUML
    print(f"  Gerando SVG para {puml_file}...")
    svg_content = run_plantuml(puml_file, 'svg')
    if not svg_content:
        print(f"  Falha ao gerar SVG para {puml_file}")
        # Cria um SVG placeholder simples
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <rect width="400" height="300" fill="#f8f9fa" stroke="#dee2e6"/>
  <text x="200" y="150" text-anchor="middle" font-family="Arial" font-size="14" fill="#6c757d">
    Diagrama PlantUML: {Path(puml_file).stem}
  </text>
  <text x="200" y="170" text-anchor="middle" font-family="Arial" font-size="12" fill="#6c757d">
    (SVG não disponível - use o código PlantUML incorporado)
  </text>
</svg>'''
    
    # Extrai o nome do diagrama
    diagram_name = Path(puml_file).stem
    
    # Cria o XML do Draw.io
    drawio_xml = create_drawio_xml(puml_content, svg_content, diagram_name)
    
    # Salva o arquivo XML
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(drawio_xml)
        print(f"✓ Convertido com sucesso: {output_file}")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo {output_file}: {e}")
        return False

def convert_directory(input_dir, output_dir):
    """
    Converte todos os arquivos .puml de um diretório
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Diretório de entrada não existe: {input_dir}")
        return False
    
    puml_files = list(input_path.rglob('*.puml'))
    if not puml_files:
        print(f"Nenhum arquivo .puml encontrado em {input_dir}")
        return False
    
    print(f"Encontrados {len(puml_files)} arquivos .puml")
    
    success_count = 0
    for puml_file in puml_files:
        # Mantém a estrutura de diretórios
        relative_path = puml_file.relative_to(input_path)
        output_file = output_path / relative_path.with_suffix('.drawio')
        
        if convert_puml_to_drawio(str(puml_file), str(output_file)):
            success_count += 1
    
    print(f"\nConversão concluída: {success_count}/{len(puml_files)} arquivos convertidos com sucesso")
    return success_count == len(puml_files)

def main():
    parser = argparse.ArgumentParser(description='Converte diagramas PlantUML para formato XML do Draw.io')
    parser.add_argument('input', help='Arquivo .puml ou diretório de entrada')
    parser.add_argument('output', help='Arquivo .drawio ou diretório de saída')
    parser.add_argument('--verbose', '-v', action='store_true', help='Saída detalhada')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if input_path.is_file():
        # Conversão de arquivo único
        if not input_path.suffix == '.puml':
            print("Erro: O arquivo de entrada deve ter extensão .puml")
            sys.exit(1)
        
        output_file = output_path if output_path.suffix == '.drawio' else output_path.with_suffix('.drawio')
        success = convert_puml_to_drawio(str(input_path), str(output_file))
        sys.exit(0 if success else 1)
    
    elif input_path.is_dir():
        # Conversão de diretório
        success = convert_directory(str(input_path), str(output_path))
        sys.exit(0 if success else 1)
    
    else:
        print(f"Erro: Caminho de entrada não existe: {input_path}")
        sys.exit(1)

if __name__ == '__main__':
    main()