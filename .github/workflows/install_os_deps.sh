#!/bin/bash

# install_os_deps.sh: Install dependencies at the operating system level
# needed for GitHub CI runs.

set -euo pipefail

if command -v brew; then
    brew list
    # Problems with Python overwriting files in /usr/local/bin
    # brew update
    # brew upgrade
elif command -v apt-get; then
    sudo apt-get -y --no-install-recommends update
fi
