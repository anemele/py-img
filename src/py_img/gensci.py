"""生成纯色透明图。"""

from typing import Optional

from PIL.Image import new

DEFAULT_SIZE = 256


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("color", type=str, nargs="?", default="#ffff", help="")
    parser.add_argument("-W", "--width", type=int, default=DEFAULT_SIZE)
    parser.add_argument("-H", "--height", type=int, default=DEFAULT_SIZE)
    parser.add_argument("-o", "--output", type=str)

    args = parser.parse_args()
    color: str = args.color
    width: int = args.width
    height: int = args.height
    output: Optional[str] = args.output

    if output is None:
        output = f"{color}_{width}x{height}.png"
    elif not output.endswith(".png"):
        output = f"{output}.png"

    try:
        img = new("RGBA", (width, height), color)
        img.save(output)
        print(f"Saved to {output}")
    except Exception as e:
        print(f"Failed to generate image: {e}")
