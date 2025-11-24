#!/bin/bash
# Installation script for AI & Custom Search Ulauncher Extension

set -e

EXTENSION_NAME="com.github.ulauncher.ai-search"
EXTENSIONS_DIR="$HOME/.local/share/ulauncher/extensions"
EXTENSION_DIR="$EXTENSIONS_DIR/$EXTENSION_NAME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installing AI & Custom Search Extension for Ulauncher"
echo ""

# Check if Ulauncher is installed
if ! command -v ulauncher &> /dev/null; then
    echo "❌ Error: Ulauncher is not installed"
    echo "   Please install Ulauncher first:"
    echo "   sudo apt install ulauncher"
    echo "   or visit: https://ulauncher.io/"
    exit 1
fi

echo "✓ Ulauncher found"

# Create extensions directory if it doesn't exist
if [ ! -d "$EXTENSIONS_DIR" ]; then
    echo "📁 Creating extensions directory..."
    mkdir -p "$EXTENSIONS_DIR"
fi

# Remove old version if exists
if [ -d "$EXTENSION_DIR" ]; then
    echo "🗑️  Removing old version..."
    rm -rf "$EXTENSION_DIR"
fi

# Copy extension files
echo "📦 Installing extension..."
mkdir -p "$EXTENSION_DIR"

# Copy required files
cp "$SCRIPT_DIR/versions.json" "$EXTENSION_DIR/"
cp "$SCRIPT_DIR/manifest.json" "$EXTENSION_DIR/"
cp "$SCRIPT_DIR/preferences.json" "$EXTENSION_DIR/"
cp "$SCRIPT_DIR/main.py" "$EXTENSION_DIR/"

# Copy documentation (optional)
cp "$SCRIPT_DIR/README.md" "$EXTENSION_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/QUICKSTART.md" "$EXTENSION_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/TROUBLESHOOTING.md" "$EXTENSION_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/CHANGELOG.md" "$EXTENSION_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/KEYWORD_EXAMPLES.md" "$EXTENSION_DIR/" 2>/dev/null || true

# Copy images directory
if [ -d "$SCRIPT_DIR/images" ]; then
    cp -r "$SCRIPT_DIR/images" "$EXTENSION_DIR/"
else
    mkdir -p "$EXTENSION_DIR/images"
    echo "⚠️  Warning: No images directory found. Please add an icon at:"
    echo "   $EXTENSION_DIR/images/icon.png"
fi

# Clear Python cache
if [ -d "$EXTENSION_DIR/__pycache__" ]; then
    rm -rf "$EXTENSION_DIR/__pycache__"
fi

echo "✓ Extension installed successfully"
echo ""

# Restart Ulauncher
echo "🔄 Restarting Ulauncher..."
if pgrep -x "ulauncher" > /dev/null; then
    pkill ulauncher
    sleep 2
fi

ulauncher &
sleep 1

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Open Ulauncher (Alt+Space)"
echo "   2. Go to Preferences → Extensions"
echo "   3. Find 'AI & Custom Search'"
echo "   4. Configure your keyword and engines"
echo "   5. Test with: ai What is Python?"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Full documentation"
echo "   - QUICKSTART.md - Quick start guide"
echo "   - TROUBLESHOOTING.md - If you have issues"
echo "   - KEYWORD_EXAMPLES.md - Creative keyword ideas"
echo ""
echo "🎉 Enjoy searching with AI & Custom Search!"
