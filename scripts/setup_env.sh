#!/bin/bash
# CLIPSIDE — Automated setup script for Debian 12 / Linux.
# Builds libclips.so from source and installs all Python dependencies.
#
# Guards added (v0.3.2):
#   check_python_version() — exits if Python < 3.10 (BUG-004)
#   check_tkinter()        — exits with install hint if tkinter missing (BUG-003)
#   install_fonts()        — installs distro-appropriate font packages (BUG-002)
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$PROJECT_DIR/.venv"
CLIPS_VERSION="6.4.1"
CLIPS_FILE_VER="${CLIPS_VERSION//./}"
CLIPS_URL="https://sourceforge.net/projects/clipsrules/files/CLIPS/${CLIPS_VERSION}/clips_core_source_${CLIPS_FILE_VER}.zip/download"
BUILD_DIR="/tmp/clips_build"

# ---------------------------------------------------------------------------
# Guard: Python version — requires Python 3.10 or higher (BUG-004)
# Linux Mint 20.3 / Ubuntu 20.04 ship Python 3.8 which is unsupported.
# ---------------------------------------------------------------------------
check_python_version() {
    local min_minor=10
    local py_major py_minor
    py_major=$(python3 -c "import sys; print(sys.version_info.major)" 2>/dev/null || echo 0)
    py_minor=$(python3 -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo 0)

    if [ "$py_major" -lt 3 ] || { [ "$py_major" -eq 3 ] && [ "$py_minor" -lt "$min_minor" ]; }; then
        echo "ERROR: Python 3.$min_minor or higher is required."
        echo "       Found: Python $py_major.$py_minor"
        echo "       Linux Mint 20.3 and Ubuntu 20.04 ship Python 3.8 — not supported."
        exit 1
    fi
    echo "  Python $py_major.$py_minor — OK"
}

# ---------------------------------------------------------------------------
# Guard: tkinter availability (BUG-003)
# On Ubuntu 22.04 python3-tk is often missing, causing a segfault on launch.
# ---------------------------------------------------------------------------
check_tkinter() {
    if ! python3 -c "import tkinter" &>/dev/null; then
        echo "ERROR: tkinter is not available for the current Python installation."
        if command -v apt-get &>/dev/null; then
            echo "Fix: sudo apt-get install python3-tk python3-dev libxcb1 libxcb-render0"
        elif command -v dnf &>/dev/null; then
            echo "Fix: sudo dnf install python3-tkinter"
        elif command -v pacman &>/dev/null; then
            echo "Fix: sudo pacman -S tk"
        fi
        exit 1
    fi
    echo "  tkinter — OK"
}

# ---------------------------------------------------------------------------
# Guard: font packages (BUG-002)
# Missing Unicode/emoji fonts cause X11 BadLength / RenderAddGlyphs crash on
# RPM-based distros (CentOS, Fedora) and sometimes on DEB-based ones too.
# ---------------------------------------------------------------------------
install_fonts() {
    echo "  Checking font dependencies..."
    if command -v dnf &>/dev/null; then
        # RPM-based: CentOS Stream, Fedora, RHEL
        sudo dnf install -y unifont gnu-free-fonts-common 2>/dev/null || true
    elif command -v apt-get &>/dev/null; then
        # DEB-based: Debian, Ubuntu, Linux Mint
        sudo apt-get install -y fonts-unifont fonts-symbola 2>/dev/null || true
    elif command -v pacman &>/dev/null; then
        # Arch-based
        sudo pacman -S --noconfirm ttf-unifont 2>/dev/null || true
    else
        echo "  WARNING: Could not detect package manager. Install fonts-unifont manually."
    fi
    echo "  Fonts — OK"
}

echo "=== CLIPSIDE Setup ==="
echo "Project: $PROJECT_DIR"

# Pre-flight checks (fail fast before any build work)
echo "[0/6] Pre-flight checks..."
check_python_version
check_tkinter
install_fonts

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
cd clips_src/*/core  # BUG-001 fix: clips.h lives in core/, not at the archive root

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
