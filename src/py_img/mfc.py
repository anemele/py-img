"""Make film directory displayed with a cover."""

import argparse
import glob
import os.path as op
from itertools import chain

import win32api
import win32con
from PIL import UnidentifiedImageError

from .sqrpng import convert as square_image


COVER_NAME = "cover"
ICON_NAME = "icon.ico"
ICON_SIZE = 256
ICON_SIZE_TUPLE = [(ICON_SIZE, ICON_SIZE)]


def make_icon(film_path: str) -> bool:
    match = glob.iglob(f"{film_path}/{COVER_NAME}.*")
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

    ico_path = op.join(film_path, ICON_NAME)
    sqr_img.save(ico_path, sizes=ICON_SIZE_TUPLE)
    # 设置隐藏属性
    win32api.SetFileAttributes(ico_path, win32con.FILE_ATTRIBUTE_HIDDEN)

    return True


def write_ini(film_path: str) -> bool:
    desktop_ini = op.join(film_path, "desktop.ini")
    # 如果已经存在，要设为普通文件，否则无法编辑
    if op.exists(desktop_ini):
        win32api.SetFileAttributes(desktop_ini, win32con.FILE_ATTRIBUTE_NORMAL)
    with open(desktop_ini, "w") as fp:
        fp.write(f"[.ShellClassInfo]\nIconResource={ICON_NAME},0\n")
    # 设置系统属性和隐藏属性
    win32api.SetFileAttributes(
        desktop_ini,
        win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM,
    )
    return True


def make_cover(film_path: str):
    # step 1: icon file
    make_icon(film_path)
    # step 2: desktop.ini
    write_ini(film_path)
    # step 3: attributes
    win32api.SetFileAttributes(film_path, win32con.FILE_ATTRIBUTE_READONLY)


def main():
    parser = argparse.ArgumentParser(prog="mfc", description=__doc__)
    parser.add_argument("path", nargs="+", help="Film path")
    args = parser.parse_args()

    arg_path: list[str] = args.path
    paths = filter(op.isdir, chain.from_iterable(map(glob.iglob, arg_path)))
    for path in paths:
        make_cover(path)


if __name__ == "__main__":
    main()
