
from fpdf import FPDF
from datetime import datetime

class RelatorioPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Monitoramento da Cigarrinha", ln=True, align="C")

    def add_info(self, dados):
        self.set_font("Arial", "", 12)
        for chave, valor in dados.items():
            self.cell(0, 10, f"{chave}: {valor}", ln=True)

    def add_imagem(self, caminho, titulo):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, titulo, ln=True)
        self.image(caminho, w=180)
