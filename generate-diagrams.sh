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
    echo "  -a, --all       Generate PNG and SVG (default)"
    echo "  -p, --png       Generate PNG only"
    echo "  -s, --svg       Generate SVG only for draw.io"
    echo "  -c, --clean     Clean generated files first"
    echo "  -h, --help      Display this help"
    echo ""
    echo "Examples:"
    echo "  $0              # Generate PNG and SVG"
    echo "  $0 --png       # Generate PNG only"
    echo "  $0 --clean     # Clean and generate all"
}

# Function to generate PNG
generate_png() {
    echo "📊 Generating PNG diagrams..."
    mvn com.github.jeluard:plantuml-maven-plugin:generate@generate-png-diagrams -q
    echo "✅ PNG generated in: docs/generated-diagrams/"
}

# Function to generate SVG
generate_svg() {
    echo "🎨 Generating SVG diagrams for draw.io..."
    mvn com.github.jeluard:plantuml-maven-plugin:generate@generate-svg-diagrams -q
    echo "✅ SVG generated in: docs/drawio-exports/"
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
    ls -lh docs/drawio-exports/ 2>/dev/null || true
}

# Simple argument parsing
ACTION="all"
while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--png)
      ACTION="png"; shift ;;
    -s|--svg)
      ACTION="svg"; shift ;;
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
  svg)
    generate_svg
    ;;
  clean)
    clean_files
    generate_png
    generate_svg
    ;;
  all)
    generate_png
    generate_svg
    ;;
  *)
    show_help; exit 1 ;;
esac

list_generated

echo -e "\n✅ Completed successfully. Tip: import SVG files from docs/drawio-exports/ into draw.io for visual editing."