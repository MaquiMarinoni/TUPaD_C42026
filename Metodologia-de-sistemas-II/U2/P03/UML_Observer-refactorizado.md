```mermaid
classDiagram
    class InventoryManager
    class StockObserver
    class EmailAlertObserver
    class AnalyticsObserver
    class ReplenishObserver
    class SMSObserver
    class BrokenObserver

    InventoryManager --> StockObserver : Cumple DIP
    
    EmailAlertObserver ..|> StockObserver : Implementa
    AnalyticsObserver ..|> StockObserver : Implementa
    ReplenishObserver ..|> StockObserver : Implementa
    SMSObserver ..|> StockObserver : Cumple OCP
    BrokenObserver ..|> StockObserver : Implementa
