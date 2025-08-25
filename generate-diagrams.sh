#!/bin/bash

# Script for PlantUML diagram generation
# Author: Architecture Diagrams Project
# Version: 1.1

set -e

echo "🚀 Starting diagram generation..."

# Check Graphviz (dot) dependency
DOT_PATH=$(command -v dot || true)
if [ -z "$DOT_PATH" ]; then
    echo "❌ Graphviz (dot) not found in PATH."
    echo "👉 Install Graphviz to enable proper PlantUML diagram rendering:"
    echo "   - macOS (Homebrew): brew install graphviz"
    echo "   - macOS (MacPorts): sudo port install graphviz"
    echo "   - Ubuntu/Debian:    sudo apt-get update && sudo apt-get install -y graphviz"
    echo "   - Fedora:           sudo dnf install graphviz"
    echo "\nAfter installation, run this script again."
    exit 1
else
    export GRAPHVIZ_DOT="$DOT_PATH"
    export PLANTUML_GRAPHVIZ_DOT="$DOT_PATH"
    echo "✅ Graphviz found: $PLANTUML_GRAPHVIZ_DOT"
fi

# Function to display help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -p, --png       Generate PNG only (default)"
    echo "  -d, --drawio    Generate Draw.io XML only"
    echo "  -a, --all       Generate PNG and Draw.io XML"
    echo "  -c, --clean     Clean generated files first"
    echo "  -h, --help      Display this help"
    echo ""
    echo "Examples:"
    echo "  $0              # Generate PNG only"
    echo "  $0 --png       # Generate PNG only"
    echo "  $0 --drawio    # Generate Draw.io XML only"
    echo "  $0 --all       # Generate PNG and Draw.io XML"
    echo "  $0 --clean     # Clean and generate all"
}

# Function to generate PNG
generate_png() {
    echo "📊 Generating PNG diagrams..."
    mvn com.github.jeluard:plantuml-maven-plugin:generate@generate-png-diagrams -q
    echo "✅ PNG generated in: docs/generated-diagrams/"
}



# Function to generate Draw.io XML files
generate_drawio_xml() {
    echo "📐 Generating Draw.io XML files..."
    
    # Check if Python converter script exists
    if [ ! -f "plantuml_to_drawio.py" ]; then
        echo "❌ plantuml_to_drawio.py not found. Cannot generate Draw.io XML files."
        return 1
    fi
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Cannot generate Draw.io XML files."
        return 1
    fi
    
    # Create output directory
    mkdir -p docs/drawio-xml-exports
    
    # Convert all PlantUML files to Draw.io XML
    python3 plantuml_to_drawio.py diagrams/ docs/drawio-xml-exports/
    
    echo "✅ Draw.io XML files generated in: docs/drawio-xml-exports/"
}

# Function to clean
clean_files() {
    echo "🧹 Cleaning generated files..."
    mvn clean -q
    echo "✅ Files cleaned"
}

# Function to list generated files
list_generated() {
    echo ""
    echo "📁 Generated files:"
    ls -lh docs/generated-diagrams/ 2>/dev/null || true

    ls -lh docs/drawio-xml-exports/ 2>/dev/null || true
}

# Simple argument parsing
ACTION="png"
while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--png)
      ACTION="png"; shift ;;

    -d|--drawio)
      ACTION="drawio"; shift ;;
    -c|--clean)
      ACTION="clean"; shift ;;
    -h|--help)
      show_help; exit 0 ;;
    -a|--all)
      ACTION="all"; shift ;;
    *)
      echo "Unknown option: $1"; show_help; exit 1 ;;
  esac
done

# Execute selected action
case "$ACTION" in
  png)
    generate_png
    ;;

  drawio)
    generate_drawio_xml
    ;;
  clean)
    clean_files
    generate_png
    generate_drawio_xml
    ;;
  all)
    generate_png
    generate_drawio_xml
    ;;
  *)
    show_help; exit 1 ;;
esac

list_generated

echo -e "\n✅ Completed successfully."
echo "💡 Tips:"
echo "   • Import XML files from docs/drawio-xml-exports/ into draw.io for full editing with PlantUML code embedded"