from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

def gerar_relatorio_pdf(dados, recomendacoes, grafico, fotos):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, "Relatório de Monitoramento - Cigarrinha-do-Milho")

    c.setFont("Helvetica", 12)
    y = height - 90
    for chave, valor in dados.items():
        c.drawString(40, y, f"{chave}: {valor}")
        y -= 20

    c.drawString(40, y, "Recomendações:")
    y -= 20
    for rec in recomendacoes:
        c.drawString(60, y, f"- {rec}")
        y -= 20

    y -= 10
    if grafico:
        grafico_img = ImageReader(grafico)
        c.drawImage(grafico_img, 40, y - 200, width=500, preserveAspectRatio=True, mask='auto')
        y -= 220

    for foto in fotos:
        try:
            img = ImageReader(foto)
            c.drawImage(img, 40, y - 150, width=200, preserveAspectRatio=True, mask='auto')
            y -= 160
        except:
            continue

    c.save()
    buffer.seek(0)
    return buffer