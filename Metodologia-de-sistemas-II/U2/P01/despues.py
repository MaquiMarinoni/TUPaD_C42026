from abc import ABC, abstractmethod
from datetime import datetime

# 1. La interfaz que todos los reportes cumplen
class Report(ABC):
    @abstractmethod
    def set_data(self, data): pass
    @abstractmethod
    def add_header(self, text): pass
    @abstractmethod
    def add_footer(self, text): pass
    @abstractmethod
    def render(self): pass
    @abstractmethod
    def get_output(self) -> str: pass

# 2. Las clases concretas (Productos)
class PDFReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"Renderizando PDF...\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self) -> str: return self.output

class ExcelReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"Renderizando Excel...\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self) -> str: return self.output

class CSVReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"Renderizando CSV...\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self) -> str: return self.output

# NUEVO REPORTE agregado sin tocar el servicio
class HTMLReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"Renderizando HTML...\n<h1>{self.header}</h1>\n<p>{self.data}</p>\n<footer>{self.footer}</footer>"
    def get_output(self) -> str: return self.output

# 3. La fábrica concentra la decisión de construcción
class ReportFactory:
    @staticmethod
    def create(format_type: str) -> Report:
        if format_type == "pdf": return PDFReport()
        elif format_type == "excel": return ExcelReport()
        elif format_type == "csv": return CSVReport()
        elif format_type == "html": return HTMLReport()
        else: raise ValueError("Formato no soportado")

# 4. El servicio ahora es agnóstico al formato
class ReportService:
    def generate(self, data, format_type):
        # El servicio pide el objeto a la fábrica. No sabe qué clase concreta le devuelven.
        report = ReportFactory.create(format_type)
        
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + datetime.now().strftime("%Y-%m-%d"))
        report.render()
        
        return report.get_output()

if __name__ == "__main__":
    servicio = ReportService()
    # Probamos generar el nuevo reporte HTML que pide la consigna
    print(servicio.generate("Ventas Q1: $1000", "html"))