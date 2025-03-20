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
    python -m pip install pyyaml
elif command -v dnf >/dev/null 2>&1; then
    dnf upgrade -y
    dnf install -y \
        gcc-c++ \
        gcc-gfortran \
        git \
        python3.12 \
        python3.12-pip \
        python3.12-pyyaml
elif command -v apt-get; then
    apt-get update -y --no-install-recommends
    apt-get install -y --no-install-recommends \
            python3 \
            python3-yaml
elif command -v pacman >/dev/null 2>&1; then
    pacman -Syu --noconfirm
    pacman -S --noconfirm \
           git \
           python \
           python-pip \
           python-pyyaml
fi
