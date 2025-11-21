"""输入图片，输出 ico 文件。"""

import argparse
import os.path as osp
from typing import Optional, Sequence

from PIL import UnidentifiedImageError
from PIL.Image import open as imopen

from ._common import glob_paths
from .sqrpng import sqr_png

MAX_SIZE = 256


def genico(path: str, size: int) -> Optional[str]:
    try:
        img = imopen(path)
    except UnidentifiedImageError as e:
        print(e)
        return

    name, _ = osp.splitext(path)
    ico_name = f"{name}.ico"
    size = min(size, MAX_SIZE)

    sqr_img = sqr_png(img, MAX_SIZE)
    sqr_img.save(ico_name, sizes=[(size, size)])

    return ico_name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file", nargs="+", type=str, help="Image file, wildcard supported."
    )
    parser.add_argument(
        "--size", type=int, default=MAX_SIZE, help="The icon file size, <= 256"
    )

    args = parser.parse_args()
    args_file: Sequence[str] = args.file
    size: int = args.size

    for file in glob_paths(args_file):
        print(f"done: {file} --> {genico(file, size)}")
