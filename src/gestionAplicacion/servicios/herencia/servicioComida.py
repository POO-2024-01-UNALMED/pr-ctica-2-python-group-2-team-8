import datetime
from gestionAplicacion.servicios.herencia.servicio import Servicio

class ServicioComida(Servicio):
    
    def __init__(self, nombre, sucursalUbicacion):
        super().__init__(nombre, sucursalUbicacion)
    
    def actualizarInventario(self):
        inventario_general = self.cliente.getCineUbicacionActual().getInventarioCine()
        inventario = []
        for producto in inventario_general:
            if producto.getTipoProducto() == "comida":
                inventario.append(producto)
        return inventario


    def descuentarPorCompra(self, metodo):
        if metodo.getNombre() != "efectivo":
            for producto in self._orden:
                if (producto.getTamaño() in ["Cangreburger", "Deadpool"]) and (producto.getPrecio() > 100000):
                    self._valorPedido -= self._valorPedido * 0.05
                    return True
            return False
        return False
        
    def factura(self):

        factura = (
            "                          CINEMAR \n"
            "==================== Factura de Comida ====================\n"
            f" Nombre dueño : {self.cliente.getNombre()}\n"
            f" Fecha de compra: {datetime.date.today()}\n"
            f"{self.mostrarOrden()}\n"
            f" Total a pagar aplicando descuentos : ${self._valorPedido}\n"
            "===========================================================\n"
        )
        return factura

    def procesarPagoRealizado(self, cliente):
        self.descuento = True