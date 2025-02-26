#!/bin/bash

# shellcheck disable=SC2086
# https://web.archive.org/web/20230401201759/https://wiki.bash-hackers.org/scripting/debuggingtips#making_xtrace_more_useful
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
set -x

set -euo pipefail

sst_spack_version="${1}"
python_version="${2}"

git checkout -- spack.yaml
eval "$(spack env activate --sh -d .)"
python build_spack_specs.py "${sst_spack_version}" "${python_version}"
spack concretize --fresh --deprecated --force
spack graph --dot > spack.dot
if command -v dot >& /dev/null; then
    dot -Tpng -o spack.{png,dot}
fi
spack install --deprecated -y --fail-fast
