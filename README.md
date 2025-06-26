# Yu-Gi-Oh Proxy Sheet Creator

A lightweight Python script that assembles a PDF of card proxies from a list of image files. The utility resizes images to 300 DPI and arranges them on A4 pages ready for printing.

## Requirements

- Python 3.8+
- [ReportLab](https://pypi.org/project/reportlab/)
- [Pillow](https://pypi.org/project/Pillow/)

Install the dependencies with:

```bash
pip install reportlab pillow
```

## Preparing the image list

Create a text file where each line contains an image path followed by the number of copies to include. For example:

```text
images/Drudomancer_Eulogy.png 4
images/Drudomancer_Respite.png 2
```

Save this file as `images.txt` or provide a custom file via the command line.

## Usage

```bash
python create_proxy_sheet.py --input images.txt --output proxies.pdf
```

The resulting `proxies.pdf` will contain the cards laid out in a grid with 10&nbsp;mm margins and 5&nbsp;mm padding.

## Customisation

Card dimensions, margins and padding are defined at the top of `create_proxy_sheet.py` in millimetres. Adjust these constants to suit your specific printing requirements.
