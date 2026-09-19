# ==========================================
# 1. EL PROVEEDOR VIEJO (Lo que el sistema espera)
# ==========================================
class OldGeoService:
    def get_location(self, ip: str) -> dict:
        # Simula la respuesta del proveedor viejo
        return {
            "lat": -31.6333,
            "lng": -60.7000,
            "city": "Santa Fe",
            "country": "Argentina"
        }

# ==========================================
# 2. EL PROVEEDOR NUEVO (Incompatible)
# ==========================================
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
        # Simula la respuesta del proveedor nuevo
        return GeoResponse(-31.6333, -60.7000, "Santa Fe", "Argentina")

# ==========================================
# 3. EL CÓDIGO CLIENTE (Simulando los 40 archivos)
# ==========================================
if __name__ == "__main__":
    # Así está en los 40 archivos del sistema:
    geo = OldGeoService()
    data = geo.get_location("200.45.123.10")
    
    print("--- Sistema funcionando con API vieja ---")
    print(f"Ciudad: {data['city']}")
    print(f"Latitud: {data['lat']}")
    
    # Si intentáramos cambiar "geo = NewGeoProvider()", 
    # la llamada geo.get_location() fallaría porque el método se llama locate(),
    # y la respuesta data['city'] fallaría porque ahora es un objeto, no un diccionario.