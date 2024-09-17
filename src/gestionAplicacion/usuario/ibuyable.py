from abc import ABC, abstractmethod

class Ibuyable(ABC):

    @abstractmethod
    def procesarPagoRealizado(self, cliente):
        pass
    
    @abstractmethod
    def factura(self):
        pass
