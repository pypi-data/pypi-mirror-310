#!/usr/bin/env python3

"""Script that automatically updates OpenCPI Projects."""

from __future__ import annotations

import argparse
import importlib.metadata
import logging
import pathlib
import sys
import typing
import xml.etree.ElementTree as ET


MODELS = ["hdl", "rcc"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("ocpiupdate")


class Version:
    """Class representation of major.minor.patch version."""

    class ComparisonWithNotAVersionError(TypeError):
        """Error when Version is compared to an invalid type."""

        def __init__(self, operator: str, other: object) -> None:
            """Construct."""
            super().__init__(f"`{operator}` operator not defined between "
                             f"`{self.__class__.__name__}` and "
                             f"`{other.__class__.__name__}`")

    @classmethod
    def raise_if_compared_to_different_type(cls, operator: str, other: object) -> None:
        """Raise error if a comparison is performed with an invalid type."""
        if not isinstance(other, cls):
            raise cls.ComparisonWithNotAVersionError(operator, other)

    def __init__(self, version_str: str) -> None:
        """Construct."""
        self._version_parts = [int(part) for part in version_str.split(".")]

    def __repr__(self) -> str:
        """Dunder method: Convert to string evaluating to class constructor."""
        return f"Version(\"{'.'.join(map(str, self._version_parts))}\")"

    def __lt__(self, other: object) -> bool:
        """Dunder method: Less than."""
        self.raise_if_compared_to_different_type("<", other)
        return self._version_parts < other._version_parts

    def __le__(self, other: object) -> bool:
        """Dunder method: Less than or equal to."""
        self.raise_if_compared_to_different_type("<", other)
        return self._version_parts <= other._version_parts

    def __eq__(self, other: object) -> bool:
        """Dunder method: Equal to."""
        self.raise_if_compared_to_different_type("<", other)
        return self._version_parts == other._version_parts

    def __gt__(self, other: object) -> bool:
        """Dunder method: Greater than."""
        self.raise_if_compared_to_different_type("<", other)
        return self._version_parts > other._version_parts

    def __ge__(self, other: object) -> bool:
        """Dunder method: Greater than or equal to."""
        self.raise_if_compared_to_different_type("<", other)
        return self._version_parts >= other._version_parts

    def __ne__(self, other: object) -> bool:
        """Dunder method: Not equal to."""
        self.raise_if_compared_to_different_type("<", other)
        return self._version_parts != other._version_parts

    def __hash__(self) -> int:
        """Dunder method: Hash."""
        return hash(self.name)

    def __str__(self) -> str:
        """Dunder method: Convert to string."""
        return ".".join(map(str, self._version_parts))


V2_4_7 = Version("2.4.7")


def yield_owd_from_project(
    project_directory: pathlib.Path,
) -> typing.Iterable[pathlib.Path]:
    """Yield a generator of worker directory paths from a project path."""
    for path in (f for model in MODELS for f in project_directory.rglob(f"*.{model}")):
        if not path.is_dir():
            continue
        model = path.suffix[1:]
        owd = path / f"{path.stem}-{model}.xml"
        if not owd.exists():
            owd = path / f"{path.stem}.xml"
            if not owd.exists():
                continue
        yield owd


def yield_workers_from_library(
    library_directory: pathlib.Path,
) -> typing.Iterable[pathlib.Path]:
    """Yield a generator of worker directory paths from a library path."""
    for path in library_directory.iterdir():
        if not path.is_dir():
            continue
        if len(path.suffixes) == 0:
            continue
        model = path.suffix[1:]
        if model not in MODELS:
            continue
        yield path


def yield_specs_from_library(
    library_directory: pathlib.Path,
) -> typing.Iterable[pathlib.Path]:
    """Yield a generator of spec file paths from a library path."""
    if not (library_directory / "specs").exists():
        return
    for path in (library_directory / "specs").iterdir():
        if path.suffix != ".xml":
            continue
        if not path.stem.endswith("spec"):
            continue
        yield path


def recursive_findall(element: ET.Element, tag: str) -> list[ET.Element]:
    """Find all occurrences of a given XML tag at any depth in an XML tree."""
    matches = []
    if element.tag == tag:
        matches.append(element)
    for child in element:
        matches.extend(recursive_findall(child, tag))
    return matches


class Arguments:
    """Class containing all globally relevant command line arguments."""

    dry_run: bool
    to_version: Version
    verbose: bool

    def __init__(self, namespace: argparse.Namespace) -> None:
        """Construct."""
        self.dry_run = namespace.dry_run
        self.to_version = namespace.to_version
        self.verbose = namespace.verbose


def v2_4_7_owd_rename(worker_directory: pathlib.Path, arguments: Arguments) -> bool:
    """
    Rename all OWD files to their v2.4.7 names.

    - Move all *.hdl/*.xml to *.hdl/*-hdl.xml
    - Move all *.rcc/*.xml to *.rcc/*-rcc.xml
        - This isn't done for RCC Workers that proxy one or more HDL Workers
          when moving to v2.4.7 or earlier.
        - See https://opencpi.dev/t/broken-hdl-worker-search-path-on-slave-attributes/105

    This function ignores OWDs that have already been migrated.
    """
    if arguments.to_version < V2_4_7:
        return False
    name = worker_directory.stem
    model = worker_directory.suffix[1:]
    old_owd_file = worker_directory / f"{name}.xml"
    # Ignore already converted workers
    if not old_owd_file.exists():
        return False
    # Ignore RCC Workers that proxy HDL Workers in v2.4.7 and earlier
    if arguments.to_version <= V2_4_7 and model == "rcc":
        slaves = ET.parse(old_owd_file).getroot().find("slaves")
        if slaves is not None:
            for instance in recursive_findall(slaves, "instance"):
                if instance.attrib.get("worker").endswith("hdl"):
                    return False
    # Rename the file
    new_owd_file = worker_directory / f"{name}-{model}.xml"
    if not arguments.dry_run:
        old_owd_file.rename(new_owd_file)
    logger.info("Moved '%s' to '%s'", old_owd_file, new_owd_file)
    return True


def v2_4_7_move_spec_to_comp(spec_file: pathlib.Path, arguments: Arguments) -> bool:
    """Move all specs/*-spec.xml to *.comp/*-comp.xml."""
    if arguments.to_version < V2_4_7:
        return False
    # Make comp dir
    spec_file_name = spec_file.stem[:-5]
    comp_dir = spec_file.parent.parent / f"{spec_file_name}.comp"
    if not arguments.dry_run:
        comp_dir.mkdir(exist_ok=True)
    logger.info("Created '%s'", comp_dir)
    # Move file to new location
    new_comp_file = comp_dir / f"{spec_file_name}-comp.xml"
    if not arguments.dry_run:
        spec_file.rename(new_comp_file)
    logger.info("Moved '%s' to '%s'", spec_file, new_comp_file)
    return True


# Replace the `spec` tag in a worker for any replaced spec file
def v2_4_7_replace_renamed_specs(
    worker_xml: pathlib.Path,
    spec_files: list[pathlib.Path],
    arguments: Arguments,
) -> bool:
    """Replace the `spec` attribute where required due to a file move."""
    if arguments.to_version < V2_4_7:
        return False
    logger.debug("Scanning '%s' ... ", worker_xml)
    with worker_xml.open("r") as file:
        lines = file.readlines()
    changed_something = False
    for i, line in enumerate(lines):
        for spec_file in spec_files:
            # Case where spec="<spec>[-_]spec.xml"
            # Case where spec="<spec>[-_]spec"
            name = spec_file.stem[:-5]
            for case in [spec_file.name, spec_file.stem]:
                if case in line:
                    lines[i] = line.replace(case, name)
                    logger.info("Replaced '%s' with '%s' on line %d of '%s'",
                                case, name, i, worker_xml)
                    changed_something = True
                    break
    if changed_something and not arguments.dry_run:
        with worker_xml.open("w") as file:
            file.writelines(lines)
    return changed_something


class MissingArgumentError(Exception):
    """Error when script is not given a required argument."""

    def __init__(self, argument: str) -> None:
        """Construct."""
        super().__init__(f"{argument} must be provided at least once")


def main() -> None:
    """Run the script."""
    # Argument parsing
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--dry-run",
        action="store_true",
    )
    argparser.add_argument(
        "--library",
        action="append",
        type=pathlib.Path,
        help="The libraries to search when moving `[-_]spec` files",
    )
    argparser.add_argument(
        "--project",
        action="append",
        type=pathlib.Path,
        help="The projects to search when modifying `spec` attributes",
    )
    argparser.add_argument(
        "--to-version",
        type=Version,
        help="The OpenCPI version to migrate to (2.4.7 [default] or newer)",
        default=V2_4_7,
    )
    argparser.add_argument(
        "--verbose",
        action="store_true",
    )
    argparser.add_argument(
        "--version",
        action="store_true",
    )
    args, unknown_args = argparser.parse_known_args()
    if len(unknown_args) != 0:
        logger.error("Extra arguments not recognised: %s", unknown_args)
        sys.exit(1)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.version:
        print(importlib.metadata.version(__package__ or __name__))  # noqa: T201
        sys.exit(0)

    try:
        # Validate arguments
        if args.project is None:
            argument = "--project"
            raise MissingArgumentError(argument)  # noqa: TRY301
        if args.library is None:
            argument = "--library"
            raise MissingArgumentError(argument)  # noqa: TRY301

        # Start of processing
        projects = args.project
        libraries = args.library
        arguments = Arguments(args)
        logger.debug("Running over projects '%s' and libraries '%s ...",
                     projects, libraries)
        files_moved = []
        for library in libraries:
            for worker in yield_workers_from_library(library):
                v2_4_7_owd_rename(worker, arguments)
            for spec_file in yield_specs_from_library(library):
                v2_4_7_move_spec_to_comp(spec_file, arguments)
                files_moved.append(spec_file)
        # Edit any worker that referenced a moved spec
        for project in projects:
            for owd in yield_owd_from_project(project):
                v2_4_7_replace_renamed_specs(owd, files_moved, arguments)
    except Exception as err:
        logger.error(str(err))  # noqa: TRY400
        if args.verbose:
            raise


if __name__ == "__main__":
    main()
