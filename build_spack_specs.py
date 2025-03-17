#!/usr/bin/env python

"""
build_spack_specs.py: Build a set of Spack specs that can exhaustively test
the packaging of SST (core, elements, macro) via Spack.
"""

import platform
import shlex
import subprocess as sp
from typing import List, Optional, Sequence


# TODO consider building MPI independently of all other variants
_SAFE_VARIANTS_CORE = ["hdf5", "pdes_mpi", "preview", "profile", "trackevents", "trackperf", "zlib"]
# dramsim2 vs. dramsim3
# otf vs. otf2
# pin ~darwin
_SAFE_VARIANTS_ELEMENTS = [
    # TODO broken on modern compilers
    # "flashdimmsim",
    "goblin",
    # TODO problem on macOS
    # "hbm",
    # TODO requires dramsim2 and nvdimmsim
    # "hybridsim",
    # TODO broken on modern compilers
    # "nvdimmsim",
    # TODO broken on modern compilers
    # "ramulator",
]
_UNSAFE_VARIANTS_ELEMENTS = [
    "dramsim2",
    "dramsim3",
    "flashdimmsim",
    "hbm",
    "hybridsim",
    "nvdimmsim",
    "otf",
    "ramulator",
]
# _SAFE_VARIANTS_MACRO = []


def make_all_variants(flags: Sequence[str], enable: bool) -> List[str]:
    enable_or_disable = "+" if enable else "~"
    return [f"{enable_or_disable}{flag}" for flag in flags]


def combine_flags(flags: Sequence[str]) -> str:
    return " ".join(flag for flag in flags if flag)


def make_all_core_variants(version: str) -> List[str]:
    if version >= "14.0.0":
        variants = _SAFE_VARIANTS_CORE + ["curses"]
    else:
        variants = _SAFE_VARIANTS_CORE
    return [
        combine_flags(flags)
        for flags in [make_all_variants(variants, True), make_all_variants(variants, False)]
    ]


def make_all_elements_variants(version: str) -> List[str]:
    unsafe_variants = make_all_variants(_UNSAFE_VARIANTS_ELEMENTS, False)
    created_variant_lines = [
        make_all_variants(_SAFE_VARIANTS_ELEMENTS, True) + unsafe_variants,
        make_all_variants(_SAFE_VARIANTS_ELEMENTS, False) + unsafe_variants,
        # TODO broken
        # make_all_variants(["dramsim2"], True),
        # TODO broken
        # make_all_variants(["dramsim3"], True),
        # TODO not supported?
        # make_all_variants(["otf"], True),
        make_all_variants(["otf2"], True) + unsafe_variants,
    ]
    if platform.system() == "Linux":
        created_variant_lines.append(
            make_all_variants(["pin"], True) + unsafe_variants,
        )
        if version > "14.1.0":
            created_variant_lines.append(
                make_all_variants(["ariel_mpi"], True) + unsafe_variants,
            )

    return [combine_flags(flags) for flags in created_variant_lines]


def add_specs(*, sst_version: str, python_version: str, compiler_spec: Optional[str]) -> List[str]:
    """Form the list of specs to install in the env."""
    specs: List[str] = list()
    constraints = "^berkeley-db ~cxx ~stl"
    if compiler_spec is None:
        compiler_spec = ""
    specs.extend(
        combine_flags(
            (
                f"sst-core@{sst_version}",
                compiler_spec,
                variant_line,
                constraints,
                f"^python@{python_version}",
            )
        )
        for variant_line in make_all_core_variants(sst_version)
    )
    specs.extend(
        combine_flags(
            (
                f"sst-elements@{sst_version}",
                compiler_spec,
                variant_line,
                constraints,
                f"^sst-core@{sst_version}",
                # re-specifying Python for elements because run requirement is
                # separate from core linkage, and it is safest to keep them in
                # sync
                f"^python@{python_version}",
            )
        )
        for variant_line in make_all_elements_variants(sst_version)
    )
    specs.extend(
        (
            f"sst-macro@{sst_version} {compiler_spec} +core ^sst-core@{sst_version}+pdes_mpi ^python@{python_version}",
            f"sst-macro@{sst_version} {compiler_spec} +pdes_mpi ^python@{python_version}",
            f"sst-macro@{sst_version} {compiler_spec} ~core ~pdes_mpi",
            # pdes_mpi requires core
            # f"sst-macro@{sst_version} ~core +pdes_mpi {compiler_spec}",
        )
    )

    return specs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("sst_version", type=str)
    parser.add_argument("python_version", type=str)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--compiler-spec", type=str, default=None)
    args = parser.parse_args()

    specs = add_specs(
        sst_version=args.sst_version,
        python_version=args.python_version,
        compiler_spec=args.compiler_spec,
    )
    if args.dry_run:
        from pprint import pprint

        pprint(specs)
    else:
        for spec in specs:
            spec_tokens = shlex.split(spec)
            sp.run(["spack", "add"] + spec_tokens)
