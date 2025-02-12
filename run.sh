#!/bin/bash

set -euo pipefail

eval "$(spack env activate --sh -d .)"
spack concretize --fresh --deprecated --force
spack graph --dot > spack.dot
if command -v dot >& /dev/null; then
    dot -Tpng -o spack.{png,dot}
fi
spack install --deprecated -y --fail-fast
