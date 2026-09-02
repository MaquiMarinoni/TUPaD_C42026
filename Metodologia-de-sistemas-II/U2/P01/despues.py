from abc import ABC, abstractmethod
from datetime import datetime

# 1. La interfaz que todos los reportes cumplen (Producto)
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

# 2. Las clases concretas (Productos Concretos)
class PDFReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- PDF ---\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self) -> str: return self.output

class ExcelReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- EXCEL ---\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self) -> str: return self.output

class CSVReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- CSV ---\nHeader: {self.header}\nData: {self.data}\nFooter: {self.footer}"
    def get_output(self) -> str: return self.output

# Nuevo producto agregado SIN tocar el ReportService
class HTMLReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- HTML ---\n<h1>{self.header}</h1>\n<p>{self.data}</p>\n<footer>{self.footer}</footer>"
    def get_output(self) -> str: return self.output

# 3. La fábrica concentra la decisión de construcción
class ReportFactory:
    
    # Justificación Factory vs Abstract Factory:
    # Se utiliza Factory Method (variante Static Factory) porque solo
    # necesitamos crear variantes de un ÚNICO tipo de objeto (Report).
    # Abstract Factory sería necesario si debiéramos crear familias de 
    # objetos relacionados (ej: Reportes + Dashboards + Exportadores) 
    # que deban ser compatibles entre sí.
    
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
        # El servicio delega la creación a la fábrica. 
        # Ya no conoce las clases concretas.
        report = ReportFactory.create(format_type)
        
        # La lógica de uso sigue intacta, operando sobre la interfaz
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + datetime.now().strftime("%Y-%m-%d"))
        report.render()
        
        return report.get_output()

# --- Bloque de prueba ---
if __name__ == "__main__":
    servicio = ReportService()
    # Ejecutamos con el nuevo formato pedido
    resultado = servicio.generate("Datos de ventas Q1", "html")
    print(resultado)