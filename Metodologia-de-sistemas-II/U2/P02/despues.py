# ==========================================
# CLASES BASE 
# ==========================================
class OldGeoService:
    def get_location(self, ip: str) -> dict:
        pass # La interfaz original que el sistema espera

class Coordinates:
    def __init__(self, lat, lng):
        self.latitude = lat
        self.longitude = lng

class Address:
    def __init__(self, locality, nation):
        self.locality = locality
        self.nation = nation

class GeoResponse:
    def __init__(self, lat, lng, locality, nation):
        self.coordinates = Coordinates(lat, lng)
        self.address = Address(locality, nation)

class NewGeoProvider:
    def locate(self, ip: str) -> GeoResponse:
        return GeoResponse(-31.6333, -60.7000, "Santa Fe", "Argentina")

# ==========================================
# ADAPTER
# ==========================================
class GeoServiceAdapter(OldGeoService):
    def __init__(self):
        # El adaptador envuelve al objeto incompatible mediante un campo (Composición)
        self.provider = NewGeoProvider()

    def get_location(self, ip: str) -> dict:
        # delega el trabajo al nuevo proveedor llamando a su método específico
        resultado = self.provider.locate(ip)
        
        # traduce la respuesta al diccionario simple que el sistema espera
        return {
            "lat": resultado.coordinates.latitude,
            "lng": resultado.coordinates.longitude,
            "city": resultado.address.locality,
            "country": resultado.address.nation
        }

# ==========================================
# EL CODIGO CLIENTE (Los 40 archivos)
# ==========================================
if __name__ == "__main__":
    # despues, unico cambio en la configuración:
    # El sistema piensa que usa el servicio viejo, pero esta usando el Adapter
    geo = GeoServiceAdapter()
    
    # Los 40 archivos siguen igual
    data = geo.get_location("200.45.123.10")
    
    print("--- Sistema funcionando con API NUEVA mediante Adapter ---")
    print(f"Ciudad: {data['city']}")
    print(f"Latitud: {data['lat']}")

    """
========================================================================
JUSTIFICACIÓN
========================================================================
Se aplicó el patrón Adapter en lugar de una refactorización masiva para 
evitar un alto costo del cambio y el riesgo de introducir bugs en los 
40 archivos clientes, protegiendo así la calidad interna del sistema. 
Se descartó el uso de una fachada porque el objetivo no era simplificar 
un subsistema complejo, sino hacer compatibles dos interfaces específicas. 
Mediante la Gestión de Límites, el adaptador actúa como un "Wrapper", 
garantizando que el sistema principal permanezca intacto y cumpla con OCP.

========================================================================
¿Qué tendría que cambiar si llega un tercer proveedor mañana?

Si mañana llega un "FutureGeoProvider", los 40 archivos del sistema cliente 
seguirán exactamente igual, sin sufrir modificaciones. La única pieza 
que debería cambiar es el interior de nuestra clase `GeoServiceAdapter` 
(instanciando al nuevo proveedor y ajustando el mapeo de sus datos al 
formato diccionario que espera el sistema), aislando así el impacto del cambio.
"""