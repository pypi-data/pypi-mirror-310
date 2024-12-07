#!/usr/bin/env python3

import argparse
import pathlib
import xml.etree.ElementTree as ET


MODELS = ["hdl", "rcc"]


class Version:
    """Class representation of major.minor.patch version."""

    def __init__(self, version_str):
        self._version_parts = [int(part) for part in version_str.split('.')]

    def __repr__(self):
        return f"Version({'.'.join(map(str, self._version_parts))})"

    def __lt__(self, other):
        return self._version_parts < other._version_parts

    def __le__(self, other):
        return self._version_parts <= other._version_parts

    def __eq__(self, other):
        return self._version_parts == other._version_parts

    def __gt__(self, other):
        return self._version_parts > other._version_parts

    def __ge__(self, other):
        return self._version_parts >= other._version_parts

    def __ne__(self, other):
        return self._version_parts != other._version_parts

    def __str__(self):
        return '.'.join(map(str, self._version_parts))


V2_4_7 = Version("2.4.7")


def yield_workers_from_library(library_directory):
    """Yield a generator of worker directory paths from a library path."""
    for path in library.iterdir():
        if not path.is_dir():
            continue
        if len(path.suffixes) == 0:
            continue
        model = path.suffix[1:]
        if model not in MODELS:
            continue
        yield path


def yield_specs_from_library(library_directory):
    """Yield a generator of spec file paths from a library path."""
    if not (library / "specs").exists():
        return
    for path in (library / "specs").iterdir():
        if path.suffix != ".xml":
            continue
        if not path.stem.endswith("spec"):
            continue
        yield path


def recursive_findall(element, tag):
    """Find all occurrences of a given XML tag at any depth in an XML tree."""
    matches = []
    if element.tag == tag:
        matches.append(element)
    for child in element:
        matches.extend(recursive_findall(child, tag))
    return matches


def v2_4_7_owd_rename(worker_directory, version_to):
    """
    Rename all OWD files to their v2.4.7 names.

    - Move all *.hdl/*.xml to *.hdl/*-hdl.xml
    - Move all *.rcc/*.xml to *.rcc/*-rcc.xml
        - This isn't done for RCC Workers that proxy one or more HDL Workers
          when moving to v2.4.7 or earlier.
        - See https://opencpi.dev/t/broken-hdl-worker-search-path-on-slave-attributes/105

    This function ignores OWDs that have already been migrated.
    """
    name = worker_directory.stem
    model = worker_directory.suffix[1:]
    old_owd_file = worker_directory / f"{name}.xml"
    # Ignore already converted workers
    if not old_owd_file.exists():
        return False
    # Ignore RCC Workers that proxy HDL Workers in v2.4.7 and earlier
    if version_to <= V2_4_7 and model == "rcc":
        slaves = ET.parse(old_owd_file).getroot().find("slaves")
        if slaves is not None:
            for instance in recursive_findall(slaves, "instance"):
                if child.attrib.get("worker").endswith("hdl"):
                    return False
    # Rename the file
    new_owd_file = worker_directory / f"{name}-{model}.xml"
    old_owd_file.rename(new_owd_file)
    print(f"Moved '{old_owd_file}' to '{new_owd_file}'")
    return True


def v2_4_7_move_spec_to_comp(spec_file):
    """Move all specs/*-spec.xml to *.comp/*-comp.xml."""
    # Make comp dir
    spec_file_name = spec_file.stem[:-5]
    comp_dir = spec_file.parent.parent / f"{spec_file_name}.comp"
    comp_dir.mkdir()
    print(f"Created '{comp_dir}'")
    # Move file to new location
    new_comp_file = comp_dir / f"{spec_file_name}-comp.xml"
    spec_file.rename(new_comp_file)
    print(f"Moved '{spec_file}' to '{new_comp_file}'")


# Replace the `spec` tag in a worker for any replaced spec file
def v2_4_7_replace_renamed_specs(worker_xml, spec_files):
    """Replace the `spec` attribute where required due to a file move."""
    print(f"Scanning '{worker_xml}' ... ")
    with worker_xml.open("r") as file:
        lines = file.readlines()
    changed_something = False
    for i, line in enumerate(lines):
        for spec_file in spec_files:
            # Case where spec="<spec>[-_]spec.xml"
            # Case where spec="<spec>[-_]spec"
            for case in [spec_file.name, spec_file.stem]:
                if case in line:
                    lines[i] = line.replace(case, spec_file.stem[:-5])
                    print(f"Replaced '{case}' with '{spec_file.stem[:-5]}' on line {i} of '{worker_xml}'")
                    changed_something = True
                    break
    if changed_something:
        with worker_xml.open("w") as file:
            file.writelines(lines)


def main():
    # Argument parsing
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--project",
        action="append",
        type=pathlib.Path,
        help="The projects to search when modifying `spec=\"\"` attributes",
    )
    argparser.add_argument(
        "--library",
        action="append",
        type=pathlib.Path,
        help="The libraries to search when moving `[-_]spec` files",
    )
    argparser.add_argument(
        "--to-version",
        type=Version,
        help="The OpenCPI version to migrate to (2.4.7 [default] or newer)",
        default=V2_4_7,
    )
    args, unknown_args = argparser.parse_known_args()
    if len(unknown_args) != 0:
        print(f"Extra arguments not recognised: {unknown_args}")

    # Validate arguments
    if args.project is None:
        raise ValueError("--project must be provided at least once")
    if args.library is None:
        raise ValueError("--library must be provided at least once")

    # Start of processing
    print(f"Running over projects '{args.project}' and libraries '{args.library} ...")
    projects = args.project
    libraries = args.library
    files_moved = []
    for library in libraries:
        for worker in yield_workers_from_library(library):
            v2_4_7_owd_rename(worker, version_to=args.to_version)
        for spec_file in yield_specs_from_library(library):
            v2_4_7_move_spec_to_comp(spec_file)
            files_moved.append(spec_file)
    # Edit any worker that referenced a moved spec
    for project in projects:
        for worker_directory in (f for model in MODELS for f in project.rglob(f"*.{model}")):
            model = worker_directory.suffix
            if not worker_directory.is_dir():
                continue
            worker_xml = worker_directory / f"{worker_directory.name}-{model}.xml"
            if not worker_xml.exists():
                worker_xml = worker_directory / f"{worker_directory.name}.xml"
                if not worker_xml.exists():
                    continue
            v2_4_7_replace_renamed_specs(worker_xml, files_moved)


def try_main():
    try:
        main()
    except Exception as err:
        print(f"ERROR: {err}")


if __name__ == "__main__":
    try_main()
