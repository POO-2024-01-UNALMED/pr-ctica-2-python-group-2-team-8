import datetime
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.usuario.cliente import Cliente
#from gestionAplicacion.usuario.metodo_pago import MetodoPago
from gestionAplicacion.servicios.herencia.servicio import Servicio

class ServicioComida(Servicio):
    
    def __init__(self, nombre=""):
        super().__init__(nombre)
    
    def actualizar_inventario(self):
        """ Description: Este método filtra y actualiza los productos que hay en el inventario 
            dependiendo de la sucursal de cine y del tipo del producto.
            return inventario: Genera un inventario con los productos disponibles del servicio
            según su localidad para tener una carta más eficiente a la hora de mostrarla al cliente.
        """
        inventario_general = self.cliente.get_cine_actual().get_inventario_cine()
        inventario = []
        for producto in inventario_general:
            if producto.get_tipo_producto().lower() == "comida" and len(inventario_general) > 0:
                inventario.append(producto)
        return inventario

    def descuentar_por_compra(self, metodo):
        """ Description: Me verifica si el método de pago tiene un descuento asociado y si cumple la condición para generar su descuento.
            param metodo: Recibe un parámetro de tipo metodo de pago el cual nos sirve para saber si tiene descuento o no.
            return: Retorna un booleano para informarle al usuario si se hizo el descuento.
        """
        if metodo.get_nombre().lower() != "efectivo":
            for producto in self.orden:
                if (producto.get_tamaño().lower() in ["cangreburger", "deadpool"]) and (producto.get_precio() > 100000):
                    self.valor_pedido -= self.valor_pedido * 0.05
                    return True
            return False
        return False

    def procesar_pago_realizado(self, cliente):
        """ Description: Este método me restablece los métodos de pago del cliente,
            además de restablecer la orden y el valor del pedido.
            param cliente: se recibe un cliente para poder restablecerle los métodos de pago.
        """
        #MetodoPago.asignar_metodos_de_pago(cliente)
        
        # Añade el producto a los productos disponibles para calificar y al historial en caso de ser la primera vez que lo compra
        for producto_orden in self.orden:
            validacion_ingreso_historial = True
            for producto_historial in cliente.get_historial_de_pedidos():
                if (producto_orden.get_nombre().lower() == producto_historial.get_nombre().lower() and 
                    producto_orden.get_tamaño().lower() == producto_historial.get_tamaño().lower()):
                    validacion_ingreso_historial = False
            if validacion_ingreso_historial:
                cliente.get_productos_disponibles_para_calificar().append(producto_orden)
                cliente.get_historial_de_pedidos().append(producto_orden)
        
        self.orden = []
        self.valor_pedido = 0.0

    def factura(self):
        """ Description: Me genera una factura la cual muestra toda la orden con su información
            y fecha de compra.
            return: Genera un String con la fecha actual, el nombre del cliente,
            y el total menos sus descuentos.
        """
        factura = (
            "                          CINEMAR \n"
            "==================== Factura de Comida ====================\n"
            f" Nombre dueño : {self.cliente.get_nombre()}\n"
            f" Fecha de compra: {datetime.date.today()}\n"
            f"{self.mostrar_orden()}\n"
            f" Total a pagar aplicando descuentos : ${self.valor_pedido}\n"
            "===========================================================\n"
        )
        return factura
