#!/bin/bash

# shellcheck disable=SC2086
# https://web.archive.org/web/20230401201759/https://wiki.bash-hackers.org/scripting/debuggingtips#making_xtrace_more_useful
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
set -x

set -eo pipefail

sst_spack_version="${1}"
python_version="${2}"
compiler_spec="${3}"

if [ -z "${sst_spack_version}" ]; then
    exit 1
fi
if [ -z "${python_version}" ]; then
    exit 1
fi
if [ -z "${compiler_spec}" ]; then
    # don't want to pass '' in the event the compiler spec isn't given
    compiler_spec_arg=
else
    compiler_spec_arg="--compiler-spec=${compiler_spec}"
fi


git checkout -- spack.yaml
eval "$(spack env activate --sh -d .)"
if command -v python 2>/dev/null; then
    PYTHON_CMD="$(command -v python)"
elif command -v python3 2>/dev/null; then
    PYTHON_CMD="$(command -v python3)"
fi
# don't want to pass '' in the event the compiler spec isn't given
"${PYTHON_CMD}" build_spack_specs.py "${sst_spack_version}" "${python_version}" ${compiler_spec_arg}
spack concretize --fresh --deprecated --force
spack graph --dot > spack.dot
if command -v dot >& /dev/null; then
    dot -Tpng -o spack.{png,dot}
fi
spack install --deprecated -y --fail-fast
