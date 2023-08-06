import glob
import importlib
import os
from os.path import dirname, normpath, realpath, sep
from pathlib import Path
from typing import List, Union


def full_path(file) -> Path:
    dir = dirname(realpath(file))
    normalized = normpath(dir)
    out = Path(normalized)
    return out


def get_repo_directory():
    # NOTE: This assumes that the repo directory, the directory
    #       where all the code lives, is the first path in the
    #       PYTHONPATH environment variable.
    #       I think this is reasonable, since usually if we're
    #       trying to run our code, we'll want to the top-level
    #       repo directory in our PYTHONPATH. This just makes
    #       the small assumption that it is the first item.
    python_path = os.environ.get("PYTHONPATH")

    assert python_path, "PYTHONPATH env variable not set"
    repo_dir = python_path.split(":")[0]
    return repo_dir


def get_all_python_files_in(directory: Union[str, Path]) -> List[str]:
    """Returns the relative paths (relative to the
    top-level repo directory) of all Python files
    within the given directory.
    """
    assert sep == "/", f"This code only works on Linux ({sep})"
    directory = normpath(directory)

    directory = str(directory).rstrip(sep)
    paths = glob.glob(
        directory + "/**/*.py",
        recursive=True,
    )  # absolute paths

    # Convert to relative to top-level repo directory paths
    repo_dir = get_repo_directory()
    prefix = repo_dir + "/"
    assert all(x.startswith(prefix) for x in paths), f"Wrong prefixes: {paths}"
    n = len(prefix)
    relative_paths = [path[n:] for path in paths]
    relative_paths = [path.rstrip(sep) for path in relative_paths]  # just in case

    return relative_paths


def convert_to_import_strings(relative_filepaths: List[str]) -> List[str]:
    """Converts a list of Python filenames (specified
    relative to the top-level repo directory) into
    import strings (e.g. "talon.core.file_utils").
    """
    assert all(
        x.endswith(".py") for x in relative_filepaths
    ), f"Wrong suffixes: {relative_filepaths}"
    paths = [path[:-3] for path in relative_filepaths]

    import_strings = [path.replace(sep, ".") for path in paths]
    return import_strings


def import_all_modules(directory: Union[Path, str]) -> List[str]:
    """Returns all the modules within the given
    directory (i.e. Python module objects,
    imported using `importlib`).
    """
    import_strings = get_all_import_strings(directory)
    import_strings = sorted(import_strings)

    for x in import_strings:
        importlib.import_module(x)

    return import_strings


def get_all_import_strings(directory: Union[Path, str]) -> List[str]:
    python_files = get_all_python_files_in(directory)
    python_files = [f for f in python_files if not f.endswith("__init__.py")]
    import_strings = convert_to_import_strings(python_files)
    return import_strings
