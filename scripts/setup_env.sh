#!/bin/bash
# CLIPSIDE — Automated setup script for Debian 12 / Linux.
# Builds libclips.so from source and installs all Python dependencies.
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$PROJECT_DIR/.venv"
CLIPS_VERSION="6.41"
CLIPS_URL="https://sourceforge.net/projects/clipsrules/files/CLIPS/${CLIPS_VERSION}/clips_core_source_${CLIPS_VERSION//./_}.zip/download"
BUILD_DIR="/tmp/clips_build"

echo "=== CLIPSIDE Setup ==="
echo "Project: $PROJECT_DIR"

# 1. System dependencies
echo "[1/6] Checking system dependencies..."
MISSING=()
for tool in gcc make curl unzip python3 pip3; do
    command -v "$tool" &>/dev/null || MISSING+=("$tool")
done
if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Missing tools: ${MISSING[*]}"
    echo "Install with: sudo apt-get install -y build-essential curl unzip python3-pip"
    exit 1
fi
echo "  OK"

# 2. Build libclips.so from CLIPS source
echo "[2/6] Building libclips.so (CLIPS $CLIPS_VERSION)..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
if [ ! -f "clips_source.zip" ]; then
    curl -L -o clips_source.zip "$CLIPS_URL"
fi
unzip -o clips_source.zip -d clips_src
cd clips_src/*/

# Compile as shared library
gcc -std=c99 -O2 -fPIC -shared \
    -o /tmp/libclips.so \
    *.c \
    -lm 2>/dev/null || {
    # Fallback: compile individual files
    gcc -std=c99 -O2 -fPIC -shared -o /tmp/libclips.so *.c -lm
}
sudo cp /tmp/libclips.so /usr/local/lib/libclips.so
sudo ldconfig
echo "  libclips.so installed to /usr/local/lib/"

# 3. Python venv
echo "[3/6] Creating Python virtual environment..."
cd "$PROJECT_DIR"
python3 -m venv "$VENV"
source "$VENV/bin/activate"
pip install --upgrade pip --quiet
echo "  OK"

# 4. Python dependencies
echo "[4/6] Installing Python dependencies..."
pip install -r "$PROJECT_DIR/requirements.txt" --quiet
echo "  OK"

# 5. Ollama model
echo "[5/6] Pulling Ollama model (marcobaturan/clips-architect-final)..."
if command -v ollama &>/dev/null; then
    ollama pull marcobaturan/clips-architect-final
    echo "  Model ready."
else
    echo "  WARNING: Ollama not found. Install from https://ollama.com/download"
    echo "  Then run: ollama pull marcobaturan/clips-architect-final"
fi

# 6. Desktop launcher
echo "[6/6] Installing desktop launcher..."
DESKTOP_SRC="$PROJECT_DIR/src/assets/clipside.desktop"
DESKTOP_DEST="$HOME/.local/share/applications/clipside.desktop"
mkdir -p "$HOME/.local/share/applications"
sed "s|PROJECT_DIR|$PROJECT_DIR|g" "$DESKTOP_SRC" > "$DESKTOP_DEST"
chmod +x "$DESKTOP_DEST"
chmod +x "$PROJECT_DIR/start.sh"
echo "  Launcher installed."

echo ""
echo "=== Setup complete! ==="
echo "Run the IDE with: ./start.sh"
echo "Or via the application menu: CLIPSIDE"
