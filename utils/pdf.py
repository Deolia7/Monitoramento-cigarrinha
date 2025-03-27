
from fpdf import FPDF

def gerar_pdf(dados, caminho_pdf, imagem_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for chave, valor in dados.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)
    if imagem_path:
        pdf.image(imagem_path, x=10, y=None, w=100)
    pdf.output(caminho_pdf)
