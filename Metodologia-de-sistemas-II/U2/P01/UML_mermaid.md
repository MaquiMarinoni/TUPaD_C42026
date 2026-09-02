- IA PARA GENERAR UML
https://mermaid.live/

/* CODIGO MERMAID PARA UML INICIAL*/


classDiagram
    class ReportService {
        +generate(data, format_type)
    }
    
    class PDFReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output()
    }
    
    class ExcelReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output()
    }
    
    class CSVReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output()
    }

    class HTMLReport {
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output()
    }

    ReportService ..> PDFReport : Instancia
    ReportService ..> ExcelReport : Instancia
    ReportService ..> CSVReport : Instancia

/* CODIGO MERMAID PARA UML REFACTORIZADO*/

classDiagram
    class Report {
        <<interface>>
        +set_data(data)
        +add_header(text)
        +add_footer(text)
        +render()
        +get_output()
    }
    
    Report <|.. PDFReport : Implementa
    Report <|.. ExcelReport : Implementa
    Report <|.. CSVReport : Implementa
    Report <|.. HTMLReport : Implementa
    
    class ReportFactory {
        +create(format_type)$ Report
    }
    
    class ReportService {
        +generate(data, format_type)
    }
    
    ReportFactory ..> PDFReport : Instancia
    ReportFactory ..> ExcelReport : Instancia
    ReportFactory ..> CSVReport : Instancia
    ReportFactory ..> HTMLReport : Instancia
    
    ReportService ..> ReportFactory : Delega creación
    ReportService ..> Report : Usa abstracción