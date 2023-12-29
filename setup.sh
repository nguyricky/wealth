#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if [[ -f "$SCRIPT_DIR/requirements.txt" ]]; then
    echo -e "Installing dependencies...\n"
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    echo -e "requirements.txt not found.\n"
    exit 1
fi

echo "#!/usr/bin/env python3" > "$SCRIPT_DIR/wealth"
echo "import sys" >> "$SCRIPT_DIR/wealth"
echo "sys.path.append('$SCRIPT_DIR')" >> "$SCRIPT_DIR/wealth"
echo "from main import main_menu" >> "$SCRIPT_DIR/wealth"
echo "main_menu()" >> "$SCRIPT_DIR/wealth"

chmod +x "$SCRIPT_DIR/wealth"

echo -e "\nSetup script complete."
echo "To run the program, execute './wealth' from this directory."
echo "Or move 'wealth' to a directory in your PATH (e.g., /usr/local/bin) to run it from anywhere."
