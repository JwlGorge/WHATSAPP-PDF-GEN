from fpdf import FPDF
import os
def generate_pdf( msglist):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.ln(10)

    for idx, msg in enumerate(msglist, start=1):
        pdf.multi_cell(0, 10, txt=f"{idx}. {msg}")
        pdf.ln(5)



    output_dir = "static"
    output_path = os.path.join(output_dir, "output.pdf")

    # Create directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf.output(output_path)
    return output_path
