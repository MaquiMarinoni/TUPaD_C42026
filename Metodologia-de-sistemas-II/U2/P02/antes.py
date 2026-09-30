# ==========================================
# PROVEEDOR VIEJO 
# ==========================================
class OldGeoService:
    def get_location(self, ip: str) -> dict:
        return {
            "lat": -31.6333,
            "lng": -60.7000,
            "city": "Santa Fe",
            "country": "Argentina"
        }

# ==========================================
# PROVEEDOR NUEVO 
# # ==========================================
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
# CODIGO CLIENTE (Simulando los 40 archivos)
# ==========================================
if __name__ == "__main__":
    geo = OldGeoService()
    data = geo.get_location("200.45.123.10")

    print("--- Sistema funcionando con API vieja ---")
    print(f"Ciudad: {data['city']}")
    print(f"Latitud: {data['lat']}")