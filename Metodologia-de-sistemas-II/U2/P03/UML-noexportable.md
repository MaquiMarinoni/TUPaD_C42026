```mermaid
classDiagram
    class InventoryManager {
        -observers: List
        +subscribe(StockObserver)
        +unsubscribe(StockObserver)
        +notify(product_id, qty)
    }
    
    class StockObserver {
        <<interface>>
        +on_low_stock(product_id, qty)
    }
    
    class EmailAlertObserver
    class AnalyticsObserver
    class ReplenishObserver
    class SMSObserver
    class BrokenObserver
    
    InventoryManager --> StockObserver : DIP
    
    EmailAlertObserver ..|> StockObserver : Implementa
    AnalyticsObserver ..|> StockObserver : Implementa
    ReplenishObserver ..|> StockObserver : Implementa
    SMSObserver ..|> StockObserver : OCP
    BrokenObserver ..|> StockObserver : Implementa