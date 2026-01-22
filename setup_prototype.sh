#!/bin/bash
# MetaFinder Prototype Setup Script

echo "================================================"
echo "🚀 MetaFinder Prototype Setup"
echo "================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "\n📋 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check ExifTool
echo -e "\n📋 Checking ExifTool..."
if ! command -v exiftool &> /dev/null; then
    echo -e "${YELLOW}⚠️  ExifTool not found${NC}"
    echo -e "Install it:"
    echo -e "  macOS:   brew install exiftool"
    echo -e "  Linux:   sudo apt install libimage-exiftool-perl"
    echo -e "  Windows: Download from https://exiftool.org/"
    exit 1
fi
EXIFTOOL_VERSION=$(exiftool -ver)
echo -e "${GREEN}✅ ExifTool $EXIFTOOL_VERSION${NC}"

# Install Python dependencies
echo -e "\n📦 Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Create directories
echo -e "\n📁 Creating directories..."
mkdir -p data
mkdir -p tests
echo -e "${GREEN}✅ Directories created${NC}"

# Create test data
echo -e "\n🧪 Creating test data..."
mkdir -p data/test-files

# Create a simple test text file with metadata
cat > data/test-files/test-document.txt << EOF
This is a test document for MetaFinder.
Created: $(date)
Author: MetaFinder Setup Script
EOF

echo -e "${GREEN}✅ Test files created in data/test-files/${NC}"

# Test the installation
echo -e "\n🧪 Testing installation..."
if python3 -c "import exiftool; print('PyExifTool OK')" 2>/dev/null; then
    echo -e "${GREEN}✅ PyExifTool working${NC}"
else
    echo -e "${RED}❌ PyExifTool not working${NC}"
    exit 1
fi

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\n📚 Quick Start:"
echo -e "  1. Scan test files:    python3 metafinder_cli.py scan data/test-files"
echo -e "  2. View statistics:    python3 metafinder_cli.py stats"
echo -e "  3. Search files:       python3 metafinder_cli.py search"
echo -e "  4. Get help:           python3 metafinder_cli.py --help"

echo -e "\n🎯 Ready to scan your files!"
