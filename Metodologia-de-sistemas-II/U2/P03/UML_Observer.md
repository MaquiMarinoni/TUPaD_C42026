```mermaid
classDiagram
    class InventoryManager_Viejo {
        +email_service
        +analytics
        +replenishment
        +update_stock()
    }
    class EmailAlertService
    class AnalyticsDashboard
    class AutoReplenishment
    
    InventoryManager_Viejo --> EmailAlertService : Conoce clase concreta
    InventoryManager_Viejo --> AnalyticsDashboard : Conoce clase concreta
    InventoryManager_Viejo --> AutoReplenishment : Conoce clase concreta

```