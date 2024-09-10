import datetime
from gestionAplicacion.servicios.herencia.servicio import Servicio

class ServicioSouvenir(Servicio):
    
    def __init__(self, nombre=""):
        super().__init__(nombre)
    
    def actualizarInventario(self):
        inventario_general = self.cliente.getCineActual().getInventarioCine()
        inventario = []
        for producto in inventario_general:
            if producto.getTipoProducto() == "souvenir" and len(inventario_general) > 0:
                inventario.append(producto)
        return inventario


    def descuentarPorCompra(self, metodo):
        if metodo.getNombre() != "efectivo":
            for producto in self.orden:
                if (producto.getTamaño() in ["katana", "emociones"]) and (producto.getPrecio() > 100000):
                    self._valorPedido -= self._valorPedido * 0.05
                    return True
            return False
        return False
        
    def factura(self):

        factura = (
            "                          CINEMAR \n"
            "==================== Factura de Souvenir ====================\n"
            f" Nombre dueño : {self.cliente.getNombre()}\n"
            f" Fecha de compra: {datetime.date.today()}\n"
            f"{self.mostrarOrden()}\n"
            f" Total a pagar aplicando descuentos : ${self._valorPedido}\n"
            "===========================================================\n"
        )
        return factura
