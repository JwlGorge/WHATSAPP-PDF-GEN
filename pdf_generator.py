from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import os

def generate_pdf(msglist):
    output_dir = "static"
    output_path = os.path.join(output_dir, "output.pdf")
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin_x = 20 * mm
    margin_y = 20 * mm
    line_height = 14
    y = height - margin_y

    # Register DejaVu font
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    c.setFont("DejaVu", 12)

    for item in msglist:
        if isinstance(item, str):
            # Handle text
            lines = item.splitlines()
            for line in lines:
                if y <= margin_y:
                    c.showPage()
                    c.setFont("DejaVu", 12)
                    y = height - margin_y
                c.drawString(margin_x, y, line)
                y -= line_height

        elif isinstance(item, dict) and item.get('type') == 'image':
            # Handle image
            image_path = item.get('path')
            try:
                img = ImageReader(image_path)
                iw, ih = img.getSize()
                aspect = ih / float(iw)
                img_width = width - 2 * margin_x
                img_height = img_width * aspect

                if img_height > (height - 2 * margin_y):
                    img_height = height - 2 * margin_y
                    img_width = img_height / aspect

                if y - img_height < margin_y:
                    c.showPage()
                    c.setFont("DejaVu", 12)
                    y = height - margin_y

                c.drawImage(img, margin_x, y - img_height, img_width, img_height)
                y -= img_height + 10  # space after image
            except Exception as e:
                print(f"Error adding image {image_path}: {e}")

    c.save()
    return output_path
