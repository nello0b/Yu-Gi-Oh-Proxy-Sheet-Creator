from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image
import os

# pip install reportlab pillow
# python create_proxy_sheet.py

# --- CONFIG ---
page_width, page_height = A4
image_width = 59 * mm
image_height = 86 * mm
margin_x = 10 * mm
margin_y = 10 * mm
padding_x = 5 * mm
padding_y = 5 * mm
input_file = 'images.txt'
output_pdf = 'output.pdf'

# DPI settings for high quality
target_dpi = 300
mm_to_inch = 25.4  # 1 inch = 25.4 mm

# --- LOAD IMAGE LIST ---
image_list = []
with open(input_file, 'r') as f:
    for line in f:
        if line.strip():
            name, count = line.strip().split()
            image_list.extend([name] * int(count))

# --- INIT PDF ---
c = canvas.Canvas(output_pdf, pagesize=A4)
# Set PDF to high quality mode
c.setPageCompression(0)  # Disable compression for maximum quality

# --- CALCULATE GRID ---
cols = int((page_width - 2 * margin_x + padding_x) // (image_width + padding_x))
rows = int((page_height - 2 * margin_y + padding_y) // (image_height + padding_y))

x_start = margin_x
y_start = page_height - margin_y - image_height

x = x_start
y = y_start
col = 0
row = 0

# --- DRAW IMAGES ---
for image_path in image_list:
    if not os.path.exists(image_path):
        continue  # Skip missing files

    try:
        # Calculate target pixel dimensions for 300 DPI
        target_width_pixels = int((image_width / mm_to_inch) * target_dpi)
        target_height_pixels = int((image_height / mm_to_inch) * target_dpi)
        
        # Open and resize image with high quality resampling
        img = Image.open(image_path)
        
        # Use LANCZOS for high-quality resampling
        img_resized = img.resize((target_width_pixels, target_height_pixels), Image.Resampling.LANCZOS)
        
        # Save with high quality settings
        temp_img = image_path + "_resized.png"
        img_resized.save(temp_img, "PNG", optimize=False, compress_level=1, dpi=(target_dpi, target_dpi))

        # Draw image at exact DPI resolution
        c.drawImage(temp_img, x, y, width=image_width, height=image_height, preserveAspectRatio=True)
        os.remove(temp_img)

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

    except Exception as e:
        print(f"Error with {image_path}: {e}")

# --- SAVE PDF ---
c.save()
print("PDF created:", output_pdf)
