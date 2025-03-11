#!/bin/bash

# install_os_deps.sh: Install dependencies at the operating system level
# needed for GitHub CI runs.

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
if command -v brew; then
    brew list
    # Problems with Python overwriting files in /usr/local/bin
    # brew update
    # brew upgrade
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y python3.12
elif command -v apt-get; then
    apt-get update -y --no-install-recommends
    apt-get install -y --no-install-recommends python3
elif command -v pacman >/dev/null 2>&1; then
    pacman -Syu --noconfirm
    pacman -S --noconfirm \
           python \
           python-pip \
           python-pyyaml
fi
