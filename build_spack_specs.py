#!/usr/bin/env python

import platform
import shlex
import subprocess as sp
from typing import List, Sequence


# TODO consider building MPI independently of all other variants
_SAFE_VARIANTS_CORE = ["hdf5", "pdes_mpi", "preview", "profile", "trackevents", "trackperf", "zlib"]
# dramsim2 vs. dramsim3
# otf vs. otf2
# pin ~darwin
_SAFE_VARIANTS_ELEMENTS = [
    # TODO broken on modern compilers
    # "flashdimmsim",
    "goblin",
    "hbm",
    "hybridsim",
    # TODO broken on modern compilers
    # "nvdimmsim",
    "ramulator",
]
# _SAFE_VARIANTS_MACRO = []


def make_all_variants(flags: Sequence[str], enable: bool) -> str:
    enable_or_disable = "+" if enable else "~"
    return " ".join(f"{enable_or_disable}{flag}" for flag in flags)


def make_all_core_variants(version: str) -> List[str]:
    if version >= "14.0.0":
        variants = _SAFE_VARIANTS_CORE + ["curses"]
    else:
        variants = _SAFE_VARIANTS_CORE
    return [make_all_variants(variants, True), make_all_variants(variants, False)]


def make_all_elements_variants(version: str) -> List[str]:
    variants = _SAFE_VARIANTS_ELEMENTS
    created_variant_lines = [
        make_all_variants(variants, True),
        make_all_variants(variants, False),
        make_all_variants(["dramsim2"], True),
        # TODO broken
        # make_all_variants(["dramsim3"], True),
        make_all_variants(["otf"], True),
        make_all_variants(["otf2"], True),
    ]
    if platform.system() == "Linux":
        created_variant_lines.append(
            make_all_variants(["pin"], True),
        )
        if version > "14.1.0":
            created_variant_lines.append(
                make_all_variants(["ariel_mpi"], True),
            )

    return created_variant_lines


def add_specs(*, sst_version: str, python_version: str) -> List[str]:
    specs: List[str] = list()
    specs.extend(
        f"sst-core@{sst_version} {variant_line} ^python@{python_version}"
        for variant_line in make_all_core_variants(sst_version)
    )
    specs.extend(
        # re-specifying Python for elements because run requirement is
        # separate from core linkage, and it is safest to keep them in sync
        f"sst-elements@{sst_version} {variant_line} ^sst-core@{sst_version} ^python@{python_version}"
        for variant_line in make_all_elements_variants(sst_version)
    )
    # TODO macro
    # specs.extend(
    #     (
    #         f"sst-macro@{sst_version} +core ^sst-core@{sst_version} ^python@{python_version}",
    #         f"sst-macro@{sst_version} ~core",
    #     )
    # )

    return specs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("sst_version", type=str)
    parser.add_argument("python_version", type=str)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # for sst_version in ("13.1.0", "14.0.0", "14.1.0", "master"):
    #     add_specs(sst_version, "3.7")
    specs = add_specs(sst_version=args.sst_version, python_version=args.python_version)
    if args.dry_run:
        from pprint import pprint

        pprint(specs)
    else:
        for spec in specs:
            spec_tokens = shlex.split(spec)
            sp.run(["spack", "add"] + spec_tokens)
