"""将图片转为正方形、边缘带透明像素的 PNG 格式。"""

import os.path as osp
from typing import Optional

from PIL import UnidentifiedImageError
from PIL.Image import Image
from PIL.Image import new as imnew
from PIL.Image import open as imopen

from ._typing import StrOrBytesPath

from .utils import auto_rename

SUFFIX = ".png"


def convert(file: StrOrBytesPath, max_pixel: Optional[int] = None) -> Optional[Image]:
    try:
        input_image = imopen(file)
    except UnidentifiedImageError as e:
        print(e)
        return None

    w, h = input_image.size
    input_max_pixel = max(w, h)

    if max_pixel is None:
        max_pixel = input_max_pixel
    elif (rate := max_pixel / input_max_pixel) < 1:
        w, h = round(w * rate), round(h * rate)
        input_image = input_image.resize((w, h))  # type: ignore

    m = max_pixel
    offset_w = (m - w) >> 1
    offset_h = (m - h) >> 1

    new_image = imnew("RGBA", (m, m))
    new_image.paste(input_image, (offset_w, offset_h))

    return new_image


def main():
    import argparse
    import glob
    import os.path
    from itertools import chain

    parser = argparse.ArgumentParser(
        prog=osp.basename(__file__).removesuffix(".py"),
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("file", nargs="+")
    parser.add_argument("-m", "--max-pixel", type=int)

    args = parser.parse_args()
    arg_file: list[str] = args.file
    arg_max: Optional[int] = args.max_pixel

    files = filter(os.path.isfile, chain(*map(glob.iglob, arg_file)))
    for file in files:
        img = convert(file, arg_max)
        if img is None:
            print(f"failed: {file}")
        else:
            path = auto_rename(file, suffix=SUFFIX)
            img.save(path)


if __name__ == "__main__":
    main()
