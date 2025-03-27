from fpdf import FPDF
from PIL import Image
import io

def gerar_pdf(nome_fazenda, talhao, data_avaliacao, adultos, ninfas, recomendacoes, fotos, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Monitoramento", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fazenda: {nome_fazenda}", ln=True)
    pdf.cell(0, 10, f"Talhão: {talhao}", ln=True)
    pdf.cell(0, 10, f"Data da Avaliação: {data_avaliacao}", ln=True)
    pdf.cell(0, 10, f"Adultos: {adultos}", ln=True)
    pdf.cell(0, 10, f"Ninfas: {ninfas}", ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Recomendações:
{recomendacoes}")

    for foto in fotos:
        image = Image.open(foto)
        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)
        pdf.image(image_buffer, x=10, y=None, w=100)

    pdf.output(output_path)