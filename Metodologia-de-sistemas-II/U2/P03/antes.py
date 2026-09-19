# ==========================================
# SERVICIOS CONCRETOS 
# ==========================================
class EmailAlertService:
    def send_low_stock_alert(self, product_id, quantity):
        print(f"[EMAIL] Alerta de stock bajo para {product_id}. Quedan: {quantity}")

class AnalyticsDashboard:
    def record_low_stock_event(self, product_id):
        print(f"[ANALYTICS] Registrando evento de stock crítico para {product_id}")

class AutoReplenishment:
    def trigger_order(self, product_id, amount):
        print(f"[COMPRAS] Orden de reposición automática generada para {product_id} por {amount} unidades")

# ==========================================
# MANAGER (Alto Acoplamiento)
# ==========================================
class InventoryManager:
    def __init__(self):
        self.stock = {}
        # Conoce a las clases concretas (Violación de DIP y OCP)
        self.email_service = EmailAlertService()
        self.analytics = AnalyticsDashboard()
        self.replenishment = AutoReplenishment()

    def update_stock(self, product_id, quantity):
        self.stock[product_id] = quantity
        print(f"\n--- Actualizando stock de {product_id} a {quantity} ---")
        
        if quantity < 10:
            self.email_service.send_low_stock_alert(product_id, quantity)
            self.analytics.record_low_stock_event(product_id)
            self.replenishment.trigger_order(product_id, 100)

    def sell_product(self, product_id, sold):
        if product_id in self.stock:
            self.stock[product_id] -= sold
            print(f"\n--- Venta de {sold} unidades de {product_id}. Stock restante: {self.stock[product_id]} ---")
            
            if self.stock[product_id] < 10:
                self.email_service.send_low_stock_alert(product_id, self.stock[product_id])
                self.analytics.record_low_stock_event(product_id)
                self.replenishment.trigger_order(product_id, 100)

# ==========================================
# EJECUCION DE PRUEBA
# ==========================================
if __name__ == "__main__":
    manager = InventoryManager()
    
    manager.update_stock("PROD-001", 15)
    manager.sell_product("PROD-001", 8)