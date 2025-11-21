"""Common utilities."""

import glob
import os.path as op
from itertools import chain
from os.path import isdir, isfile
from pathlib import Path
from typing import Iterable, Optional


def glob_paths(
    patterns: Iterable[str],
    recursive: bool = False,
    *,
    only_file: bool = False,
    only_dir: bool = False,
) -> Iterable[str]:
    paths = chain.from_iterable(
        glob.iglob(pattern, recursive=recursive) for pattern in patterns
    )
    if only_file:
        paths = filter(isfile, paths)
    elif only_dir:
        paths = filter(isdir, paths)

    return paths


def auto_rename(
    old_name: Path | str,
    *,
    suffix: Optional[str] = None,
) -> Path | str:
    if not op.exists(old_name):
        return old_name

    base, _suffix = op.splitext(old_name)
    if suffix is None:
        suffix = _suffix

    num = 1
    while True:
        new_name = f"{base}_{num}{suffix}"
        if not op.exists(new_name):
            return new_name
        num += 1
