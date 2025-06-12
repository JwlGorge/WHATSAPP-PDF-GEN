from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetricsimport os
def generate_pdf( msglist):
    output_dir = "static"
    output_path = os.path.join(output_dir, "output.pdf")
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin_x = 20 * mm
    margin_y = 20 * mm
    line_height = 14
    y = height - margin_y

    # Register DejaVu font (must be in your project)
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    c.setFont("DejaVu", 12)

    # Join all messages into one text block
    full_text = "\n".join(msglist)
    lines = full_text.splitlines()

    for line in lines:
        if y <= margin_y:
            c.showPage()
            c.setFont("DejaVu", 12)
            y = height - margin_y
        c.drawString(margin_x, y, line)
        y -= line_height

    c.save()
    return output_path





