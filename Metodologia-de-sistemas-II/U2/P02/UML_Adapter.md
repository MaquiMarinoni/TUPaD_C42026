```mermaid
classDiagram
    class Cliente {
        <<40 archivos del sistema>>
    }
    
    class OldGeoService {
        +get_location(ip)
    }
    
    class GeoServiceAdapter {
        -provider: NewGeoProvider
        +get_location(ip)
    }
    
    class NewGeoProvider {
        +locate(ip)
    }
    
    Cliente ..> OldGeoService : Espera usar
    GeoServiceAdapter --|> OldGeoService : Extiende (Implementa)
    GeoServiceAdapter --> NewGeoProvider : Compone (Envuelve)
    ```