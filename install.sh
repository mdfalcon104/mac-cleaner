#!/bin/bash

echo "========================================"
echo "Mac Cleaner - Installation Script"
echo "========================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is designed for macOS."
    echo "   The app may not work properly on other systems."
    echo ""
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "   Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 is installed: $(python3 --version)"
echo ""

# Optional: Convert icon to .icns format (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Would you like to convert the icon to .icns format? (recommended)"
    read -p "This requires macOS tools (sips and iconutil) [y/N]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Check if required tools are available
        if ! command -v sips &> /dev/null; then
            echo "❌ Error: 'sips' command not found. This tool is required for icon conversion."
            echo "   Skipping icon conversion..."
        elif ! command -v iconutil &> /dev/null; then
            echo "❌ Error: 'iconutil' command not found. This tool is required for icon conversion."
            echo "   Skipping icon conversion..."
        else
            echo "Converting icon to .icns format..."
            
            mkdir -p AppIcon.iconset
        sips -z 16 16     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_16x16.png > /dev/null 2>&1
        sips -z 32 32     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_16x16@2x.png > /dev/null 2>&1
        sips -z 32 32     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_32x32.png > /dev/null 2>&1
        sips -z 64 64     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_32x32@2x.png > /dev/null 2>&1
        sips -z 128 128   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_128x128.png > /dev/null 2>&1
        sips -z 256 256   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_128x128@2x.png > /dev/null 2>&1
        sips -z 256 256   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_256x256.png > /dev/null 2>&1
        sips -z 512 512   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_256x256@2x.png > /dev/null 2>&1
        sips -z 512 512   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_512x512.png > /dev/null 2>&1
        sips -z 1024 1024 "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_512x512@2x.png > /dev/null 2>&1
        
            if iconutil -c icns AppIcon.iconset -o "Mac Cleaner.app/Contents/Resources/AppIcon.icns" 2> /dev/null; then
                echo "✓ Icon converted to .icns format"
                rm -rf AppIcon.iconset
            else
                echo "⚠️  Could not convert icon (this is optional)"
                rm -rf AppIcon.iconset
            fi
        fi
    fi
fi

echo ""
echo "Would you like to copy Mac Cleaner to /Applications/?"
read -p "This will make it easily accessible [y/N]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "/Applications" ]; then
        cp -r "Mac Cleaner.app" /Applications/
        echo "✓ Mac Cleaner.app copied to /Applications/"
        echo ""
        echo "========================================"
        echo "✨ Installation Complete!"
        echo "========================================"
        echo ""
        echo "You can now:"
        echo "  • Open Finder → Applications"
        echo "  • Double-click 'Mac Cleaner' to run"
        echo ""
        echo "Or run directly from terminal:"
        echo "  python3 clean_mac.py"
    else
        echo "❌ /Applications directory not found"
        exit 1
    fi
else
    echo ""
    echo "========================================"
    echo "✨ Setup Complete!"
    echo "========================================"
    echo ""
    echo "You can run Mac Cleaner by:"
    echo "  • Double-clicking 'Mac Cleaner.app' in this folder"
    echo "  • Running: python3 clean_mac.py"
fi

echo ""
