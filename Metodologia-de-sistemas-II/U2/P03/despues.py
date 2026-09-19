from abc import ABC, abstractmethod

# ==========================================
# LA INTERFAZ SUSCRIPTORA (abstracción)
# ==========================================
class StockObserver(ABC):
    @abstractmethod
    def on_low_stock(self, product_id: str, quantity: int):
        pass

# ==========================================
# SUSCRIPTORES CONCRETOS
# ==========================================
class EmailAlertObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int):
        print(f"[EMAIL] Alerta de stock bajo para {product_id}. Quedan: {quantity}")

class AnalyticsObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int):
        print(f"[ANALYTICS] Registrando evento de stock crítico para {product_id}")

class ReplenishObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int):
        print(f"[COMPRAS] Orden de reposición automática generada para {product_id} por 100 unidades")

#canal nuevo para demostrar extensibilidad (OCP)
class SMSObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int):
        print(f"[SMS] Enviando mensaje de texto: Stock crítico de {product_id}")

#observador roto
class BrokenObserver(StockObserver):
    def on_low_stock(self, product_id: str, quantity: int):
        print(f"[ROTO] Intentando procesar {product_id}...")
        raise Exception("Error de red simulado: el servicio se cayó.")
# ==========================================
# MANAGER REFACTORIZADO
# ==========================================
class InventoryManager:
    def __init__(self):
        self.stock = {}
        self.observers = []

    def subscribe(self, observer: StockObserver):
        self.observers.append(observer)

    def unsubscribe(self, observer: StockObserver):
        self.observers.remove(observer)

    def notify(self, product_id: str, quantity: int):
        for observer in self.observers:
            try:
                observer.on_low_stock(product_id, quantity)
            except Exception as e:
                # Si un observer falla, lo registra pero el loop continua
                print(f"[LOG DE ERROR] Falló un observador: {e}")

    def update_stock(self, product_id: str, quantity: int):
        self.stock[product_id] = quantity
        print(f"\n--- Actualizando stock de {product_id} a {quantity} ---")
        
        if quantity < 10:
            self.notify(product_id, quantity)

    def sell_product(self, product_id: str, sold: int):
        if product_id in self.stock:
            self.stock[product_id] -= sold
            print(f"\n--- Venta de {sold} unidades de {product_id}. Stock restante: {self.stock[product_id]} ---")
            
            if self.stock[product_id] < 10:
                self.notify(product_id, self.stock[product_id])

# ==========================================
# EJECUCION DE PRUEBA
# ==========================================
if __name__ == "__main__":
    manager = InventoryManager()
    
    manager.subscribe(EmailAlertObserver())
    manager.subscribe(AnalyticsObserver())
    
    manager.subscribe(BrokenObserver())
    
    manager.subscribe(ReplenishObserver())
    manager.subscribe(SMSObserver())
    
    manager.update_stock("PROD-001", 15)
    manager.sell_product("PROD-001", 8)