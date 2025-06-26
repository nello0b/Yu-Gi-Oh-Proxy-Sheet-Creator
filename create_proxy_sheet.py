"""Create a PDF sheet of card proxies from a list of image paths."""

from __future__ import annotations

import argparse
import os
from typing import List, Tuple

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


# Layout configuration (in millimetres)
IMAGE_WIDTH_MM = 59
IMAGE_HEIGHT_MM = 86
MARGIN_MM = 10
PADDING_MM = 5

# DPI settings for high quality output
TARGET_DPI = 300
MM_TO_INCH = 25.4


def parse_hex_color(value: str) -> Tuple[float, float, float]:
    """Return an RGB tuple (0-1 range) from ``value`` like ``#RRGGBB``."""
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Invalid hex color: {value}")
    r = int(value[0:2], 16) / 255.0
    g = int(value[2:4], 16) / 255.0
    b = int(value[4:6], 16) / 255.0
    return r, g, b


def load_image_list(path: str) -> List[str]:
    """Return a flat list of image paths from ``path``.

    Each line in ``path`` should contain an image file followed by the
    number of copies to include in the PDF.
    """

    images: List[str] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            name, count = line.split()
            images.extend([name] * int(count))
    return images


def create_proxy_sheet(
    image_list: List[str], output_pdf: str, background: Tuple[float, float, float]
) -> None:
    """Generate ``output_pdf`` containing ``image_list`` arranged on A4 pages."""

    page_width, page_height = A4
    image_width = IMAGE_WIDTH_MM * mm
    image_height = IMAGE_HEIGHT_MM * mm
    margin_x = MARGIN_MM * mm
    margin_y = MARGIN_MM * mm
    padding_x = PADDING_MM * mm
    padding_y = PADDING_MM * mm

    target_width_px = int((IMAGE_WIDTH_MM / MM_TO_INCH) * TARGET_DPI)
    target_height_px = int((IMAGE_HEIGHT_MM / MM_TO_INCH) * TARGET_DPI)

    cols = int((page_width - 2 * margin_x + padding_x) // (image_width + padding_x))
    rows = int((page_height - 2 * margin_y + padding_y) // (image_height + padding_y))

    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.setPageCompression(0)
    c.setFillColorRGB(*background)

    x_start = margin_x
    y_start = page_height - margin_y - image_height

    x = x_start
    y = y_start
    col = 0
    row = 0

    for image_path in image_list:
        if not os.path.exists(image_path):
            print(f"Warning: {image_path} not found, skipping")
            continue

        try:
            img = Image.open(image_path)
            resized = img.resize((target_width_px, target_height_px), Image.Resampling.LANCZOS)
            reader = ImageReader(resized)
            # draw background rectangle then the image
            c.rect(x, y, image_width, image_height, stroke=0, fill=1)
            c.drawImage(
                reader,
                x,
                y,
                width=image_width,
                height=image_height,
                preserveAspectRatio=True,
            )
        except Exception as exc:  # pragma: no cover - simple script
            print(f"Error processing {image_path}: {exc}")
            continue

        col += 1
        if col >= cols:
            col = 0
            row += 1
            x = x_start
            y -= image_height + padding_y
            if row >= rows:
                c.showPage()
                row = 0
                y = y_start
        else:
            x += image_width + padding_x

    c.save()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a PDF proxy sheet from a list of images")
    parser.add_argument("-i", "--input", default="images.txt", help="path to image list")
    parser.add_argument("-o", "--output", default="output.pdf", help="output PDF file")
    parser.add_argument(
        "-b",
        "--background",
        default="#FFFFFF",
        help="hex color for image background (e.g. #FF0000)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    images = load_image_list(args.input)
    if not images:
        print("No images to process")
        return
    try:
        background = parse_hex_color(args.background)
    except ValueError as exc:
        print(exc)
        return
    create_proxy_sheet(images, args.output, background)
    print(f"PDF created: {args.output}")


if __name__ == "__main__":
    main()

