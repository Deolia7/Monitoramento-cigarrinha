
from fpdf import FPDF
from io import BytesIO

def gerar_pdf(df, clima_df, imagem):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Técnico de Monitoramento", ln=True)
    pdf.set_font("Arial", size=12)
    for i, row in df.iterrows():
        pdf.cell(0, 10, f"Ponto {row['ponto']}: Adultos={row['adultos']} Ninfas={row['ninfas']}", ln=True)
    pdf.cell(0, 10, "", ln=True)
    pdf.cell(0, 10, "Resumo Previsão Populacional:", ln=True)
    for i, row in clima_df.head(5).iterrows():
        pdf.cell(0, 10, f"{row['data'].strftime('%d/%m/%Y')}: {row['pop_total']:.1f}", ln=True)
    if imagem:
        img_bytes = imagem.read()
        img_path = "/tmp/temp_img.jpg"
        with open(img_path, "wb") as f:
            f.write(img_bytes)
        pdf.image(img_path, x=10, y=None, w=100)
    output = BytesIO()
    pdf.output(output)
    return output.getvalue()
