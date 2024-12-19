import os.path as op
from pathlib import Path
from typing import Optional, Union

P = Union[Path, str]


def auto_rename(old_name: P, *, suffix: Optional[str] = None) -> P:
    if not op.exists(old_name):
        return old_name

    base, _suffix = op.splitext(old_name)
    if suffix is None:
        suffix = _suffix

    num = 1
    while True:
        new_name = f'{base}_{num}{suffix}'
        if not op.exists(new_name):
            return new_name
        num += 1
