
from fpdf import FPDF
from PIL import Image
import os

def gerar_pdf(caminho_pdf, dados, imagens):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for chave, valor in dados.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)

    for imagem in imagens:
        if imagem and os.path.exists(imagem):
            pdf.image(imagem, w=180)

    pdf.output(caminho_pdf)
