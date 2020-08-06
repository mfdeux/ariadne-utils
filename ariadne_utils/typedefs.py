import typing
from glob import glob
from pathlib import Path


def load_typedef_files(paths: typing.List[str], typedefs: str = None) -> str:
    """
    Collect and load typedef files from disk
    """
    if not typedefs:
        typedefs = ""

    typedef_paths = []

    for path in paths:
        for p in glob(path, recursive=True):
            typedef_paths.append(Path(p))

    for typedef_path in typedef_paths:
        with typedef_path.open() as f:
            typedefs += f.read()

    return typedefs
