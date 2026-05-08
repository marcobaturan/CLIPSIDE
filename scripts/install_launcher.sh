#!/bin/bash
# CLIPSIDE Launcher Installer
# This script installs the .desktop file to the Desktop and Applications menu.

# Get the absolute path of the project root (the parent directory of this script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_PATH="$PROJECT_ROOT/src/assets/clipside.desktop"
TEMP_DESKTOP="/tmp/clipside.desktop"

echo "📦 Installing CLIPSIDE launcher..."
echo "📍 Project Root: $PROJECT_ROOT"

if [ ! -f "$TEMPLATE_PATH" ]; then
    echo "❌ Error: Template not found at $TEMPLATE_PATH"
    exit 1
fi

# Replace PROJECT_DIR with the actual path
sed "s|PROJECT_DIR|$PROJECT_ROOT|g" "$TEMPLATE_PATH" > "$TEMP_DESKTOP"

# 1. Install to Desktop
DESKTOP_DIR="$HOME/Desktop"
[ ! -d "$DESKTOP_DIR" ] && DESKTOP_DIR="$HOME/Escritorio"

if [ -d "$DESKTOP_DIR" ]; then

    cp "$TEMP_DESKTOP" "$DESKTOP_DIR/"
    chmod +x "$DESKTOP_DIR/clipside.desktop"
    echo "✅ Launcher added to Desktop"
else
    echo "⚠️ Desktop directory not found, skipping..."
fi

# 2. Install to Applications Menu
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
cp "$TEMP_DESKTOP" "$APPS_DIR/"
chmod +x "$APPS_DIR/clipside.desktop"
echo "✅ Launcher added to Applications menu (Development)"

# Clean up
rm "$TEMP_DESKTOP"

# Ensure start.sh is executable
chmod +x "$PROJECT_ROOT/start.sh"

echo "🚀 Done! You can now launch CLIPSIDE from your menu or desktop."
