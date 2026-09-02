from abc import ABC, abstractmethod
from datetime import datetime

# interfaz que todos los reportes cumplen (Producto)
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

# clases 
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

# Nuevo producto agregado sin tocar el ReportService
class HTMLReport(Report):
    def set_data(self, data): self.data = data
    def add_header(self, text): self.header = text
    def add_footer(self, text): self.footer = text
    def render(self): self.output = f"--- HTML ---\n<h1>{self.header}</h1>\n<p>{self.data}</p>\n<footer>{self.footer}</footer>"
    def get_output(self) -> str: return self.output

# Factory 
class ReportFactory:
    
# Factory Method vs. Abstract Factory)
#    Se selecciona Factory Method en lugar de Abstract Factory porque se requiere un mecanismo para instanciar variantes de un unico producto central (Report). Abstract Factory se recomienda para escenarios donde se necesiten crear familias enteras de objetos interrelacionados que deban ser compatibles (ej: Reportes + Dashboards + Gráficos corporativos). Aplicar Abstract Factory aquí habría generado procesamiento innecesario.
    
    @staticmethod
    def create(format_type: str) -> Report:
        if format_type == "pdf": return PDFReport()
        elif format_type == "excel": return ExcelReport()
        elif format_type == "csv": return CSVReport()
        elif format_type == "html": return HTMLReport()
        else: raise ValueError("Formato no soportado")

# Implementacion
# El metodo Static centraliza la lógica de construcción de los objetos concretos. Permite que el servicio dpermanezca desacoplado de las implementaciones y abierto a la extensión ante nuevos formatos.

# El servicio ahora es agnóstico al formato
class ReportService:
    def generate(self, data, format_type):
        # El servicio delega la creación a fabric. 
        report = ReportFactory.create(format_type)
        
        report.set_data(data)
        report.add_header("Reporte Mensual")
        report.add_footer("Generado el " + datetime.now().strftime("%Y-%m-%d"))
        report.render()
        
        return report.get_output()