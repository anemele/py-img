import argparse
import os
import os.path as op
from typing import Optional

from PIL import Image


def main():
    parser = argparse.ArgumentParser(
        prog=op.basename(__file__).removesuffix(".py"),
        description="Split a GIF into individual frames.",
    )
    parser.add_argument("path", help="Path to the GIF file.")
    parser.add_argument(
        "-o", "--out-dir", help="Output directory for the individual frames."
    )
    args = parser.parse_args()

    path: str = args.path
    out_dir: Optional[str] = args.out_dir

    if out_dir is None:
        out_dir, _ = op.splitext(path)

    if op.exists(out_dir):
        if not op.isdir(out_dir):
            print(f"File with the same name {out_dir} exist.")
            exit(1)
    else:
        os.mkdir(out_dir)

    img = Image.open(path)

    try:
        while True:
            cur = img.tell()
            pth = op.join(out_dir, f"{cur:03d}.png")
            img.save(pth)
            img.seek(cur + 1)
    except (IOError, EOFError):
        pass

    print(f"Frames saved to {out_dir}.")


if __name__ == "__main__":
    main()
