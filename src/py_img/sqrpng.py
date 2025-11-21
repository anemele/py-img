"""将图片转为正方形、边缘带透明像素的 PNG 格式。"""

from typing import Optional, Sequence

from PIL import UnidentifiedImageError
from PIL.Image import Image
from PIL.Image import new as imnew
from PIL.Image import open as imopen

from ._common import auto_rename, glob_paths


def sqr_png(image: Image, max_pixel: Optional[int] = None) -> Image:
    w, h = image.size
    input_max_pixel = max(w, h)

    if max_pixel is None:
        max_pixel = input_max_pixel
    elif (rate := max_pixel / input_max_pixel) < 1:
        w, h = round(w * rate), round(h * rate)
        image = image.resize((w, h))

    m = max_pixel
    offset_w = (m - w) >> 1
    offset_h = (m - h) >> 1

    new_image = imnew("RGBA", (m, m))
    new_image.paste(image, (offset_w, offset_h))

    return new_image


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="+")
    parser.add_argument("-m", "--max-pixel", type=int)

    args = parser.parse_args()
    arg_file: Sequence[str] = args.file
    arg_max: Optional[int] = args.max_pixel

    for file in glob_paths(arg_file):
        try:
            img = imopen(file)
        except UnidentifiedImageError as e:
            print(e)
            continue

        img = sqr_png(img, arg_max)
        path = auto_rename(file, suffix=".png")
        img.save(path)
