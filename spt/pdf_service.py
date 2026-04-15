from io import BytesIO

# from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

from xhtml2pdf import pisa

def generate_spt_pdf(spt):
    pimpinan = User.objects.filter(groups__name="pimpinan").first()
    pimpinan = pimpinan.profile if pimpinan else None
    html = render_to_string("spt/pdf.html", {"spt": spt, "pimpinan": pimpinan})
    
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)

    return result.getvalue()
    # return ContentFile(result.getvalue())

# def generate_spt_pdf(spt):
#     html = render_to_string("spt/pdf.html", {"spt": spt})
#     pdf_file = HTML(string=html).write_pdf()
#     return ContentFile(pdf_file)

# def generate_spt_pdf(spt):
#     buffer = BytesIO()

#     # pakai reportlab / weasyprint / html2pdf
#     pdf = create_pdf_from_template(spt)

#     buffer.write(pdf)
#     buffer.seek(0)

#     return File(buffer)