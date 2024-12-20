import os.path as op
from pathlib import Path
from typing import Optional


def auto_rename(old_name: Path | str, *, suffix: Optional[str] = None) -> Path | str:
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
