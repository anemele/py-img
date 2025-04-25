"""Make film directory displayed with a cover.

\x1b[33m{cover}.*\x1b[m --> \x1b[32m{icon_name}\x1b[m

Any file named {cover}.* in the root of the film directory
will be recognized and used as the cover image, which is
named as {icon_name}.

e.g.

{{root}}/
    \x1b[33m{cover}.jpg\x1b[m
    \x1b[32m{icon_name}\x1b[m
"""

from pathlib import Path
from typing import Sequence

import win32api
import win32con
from PIL import UnidentifiedImageError

from .sqrpng import convert as square_image

COVER_NAME = "cover"
ICON_NAME = "icon.ico"
ICON_SIZE = 256
ICON_SIZE_TUPLE = [(ICON_SIZE, ICON_SIZE)]


def make_icon(film_path: Path) -> bool:
    match = film_path.glob(f"{COVER_NAME}.*")
    # 此处尝试每一个匹配，如果成功则结束，否则认为不存在，抛出 StopIteration
    for img_path in match:
        try:
            sqr_img = square_image(img_path, ICON_SIZE)
            break
        except UnidentifiedImageError:
            continue
    else:
        print(f"no {COVER_NAME}.* file found in {film_path}")
        return False

    if sqr_img is None:
        print("failed to create squared image")
        return False

    ico_path = film_path / ICON_NAME
    sqr_img.save(ico_path, sizes=ICON_SIZE_TUPLE)
    # 设置隐藏属性
    win32api.SetFileAttributes(str(ico_path), win32con.FILE_ATTRIBUTE_HIDDEN)

    return True


def write_ini(film_path: Path) -> bool:
    desktop_ini = film_path / "desktop.ini"
    # 如果已经存在，要设为普通文件，否则无法编辑
    if desktop_ini.exists():
        win32api.SetFileAttributes(str(desktop_ini), win32con.FILE_ATTRIBUTE_NORMAL)
    desktop_ini.write_text(f"[.ShellClassInfo]\nIconResource={ICON_NAME},0\n")
    # 设置系统属性和隐藏属性
    win32api.SetFileAttributes(
        str(desktop_ini),
        win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM,
    )
    return True


def make_cover(film_path: Path):
    # step 1: icon file
    if not make_icon(film_path):
        return
    # step 2: desktop.ini
    if not write_ini(film_path):
        return
    # step 3: attributes
    win32api.SetFileAttributes(str(film_path), win32con.FILE_ATTRIBUTE_READONLY)

    print(f"done: {film_path}")


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description=__doc__.format(cover=COVER_NAME, icon_name=ICON_NAME),  # type: ignore
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("path", type=Path, nargs="+", help="Film path")
    os.system("")  # enable ANSI escape code
    args = parser.parse_args()
    arg_path: Sequence[Path] = args.path

    for path in arg_path:
        if not path.is_dir():
            print(f"{path} is not a directory")
            continue
        try:
            make_cover(path)
        except Exception as e:
            print(f"failed to make cover for {path}: {e}")


if __name__ == "__main__":
    main()
