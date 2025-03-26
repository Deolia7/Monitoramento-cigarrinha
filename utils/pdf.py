from fpdf import FPDF

def gerar_pdf(df, previsao, recomendacao):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório Técnico - Monitoramento de Cigarrinha", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Recomendação:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, recomendacao)
    pdf.ln(5)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Últimos Dados Coletados:", ln=True)
    pdf.set_font("Arial", size=10)
    for _, row in df.tail(1).iterrows():
        for k, v in row.items():
            pdf.cell(200, 8, f"{k}: {v}", ln=True)

    pdf.output("relatorio_final.pdf")