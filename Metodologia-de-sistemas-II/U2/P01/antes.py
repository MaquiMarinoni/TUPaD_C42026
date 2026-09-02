from datetime import datetime

class PDFReport:
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- PDF ---\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self): return self.output

class ExcelReport:
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- EXCEL ---\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self): return self.output

class CSVReport:
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- CSV ---\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self): return self.output

class ReportService:
    def generate(self, data, format_type):
        # decisión de construcción mezclada con lógica de uso
        if format_type == "pdf":
            report = PDFReport()
        elif format_type == "excel":
            report = ExcelReport()
        elif format_type == "csv":
            report = CSVReport()
        else:
            raise ValueError("Formato no soportado")
        
        # lógica de uso igual para todos los tipos
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + datetime.now().strftime("%Y-%m-%d"))
        report.render()
        
        return report.get_output()

# --- Bloque de prueba ---
if __name__ == "__main__":
    servicio = ReportService()
    resultado = servicio.generate("Datos de ventas Q1", "pdf")
    print(resultado)