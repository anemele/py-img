"""输入图片，输出 ico 文件。"""

import argparse
import glob
import os.path as osp
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Optional

from .sqrpng import convert as square_image

MAX_SIZE = 256


def genico(path: Path | str, size: int) -> Optional[Path | str]:
    sqr_img = square_image(path, MAX_SIZE)
    if sqr_img is None:
        return None

    name, _ = osp.splitext(path)
    ico_name = f"{name}.ico"
    size = min(size, MAX_SIZE)
    sqr_img.save(ico_name, sizes=[(size, size)])

    return ico_name


def main():
    parser = argparse.ArgumentParser(
        prog=osp.basename(__file__).removesuffix(".py"),
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "file", nargs="+", type=str, help="Image file, wildcard supported."
    )
    parser.add_argument(
        "--size", type=int, default=MAX_SIZE, help="The icon file size, <= 256"
    )

    args = parser.parse_args()
    # print(args)
    args_file: list[str] = args.file
    args_size: int = args.size

    _genico = partial(genico, size=args_size)

    files = filter(osp.isfile, chain.from_iterable(map(glob.iglob, args_file)))
    for file in files:
        print(f"done: {file} --> {_genico(file)}")


if __name__ == "__main__":
    main()
