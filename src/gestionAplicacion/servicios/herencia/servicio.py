from abc import ABC, abstractmethod
from producto import Producto
import sucursalCine


class Servicio (ABC):
    cliente  = None
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = []
        self.orden = []
        self.bonosCliente = []
        self.valorPedido = 0.0
        
    @abstractmethod
    def descuentarPorCompra(self, metodo):
        pass

    @abstractmethod
    def actualizarInventario(self):
        pass

    @staticmethod
    def mostrarBonos(servicio):
        n = 0
        bono = "\n====== Tienes los siguientes bonos disponibles ======\n" 
        + "\n0. No reclamar ningún bono."
        for bono in servicio.getBonosCliente():
            n += 1
            bono += f"\n{n}. {bono.getProducto().getNombre()} {bono.getProducto().getTamaño()} código: {bono.getCodigo()}"
        return bono

    def actualizarBonos(self):
        for bono in self.cliente.getCineActual().getBonosCreados():
            if bono.getTipoServicio() == self.nombre and bono.getCliente() == self.cliente:
               self.bonosCliente.append(bono) 

    def descuentarPorGenero(self, cine):
        for producto in self.orden:
            for ticket in cine.getTicketsParaDescuento():
                if producto.getGenero() == ticket.getPelicula().getGenero() and self.cliente == ticket.getDueno():
                    fecha = sucursalCine.getFechaActual().date()
                    if fecha == ticket.getHorario().date() and ticket.isDescuento():
                        ticket.setDescuento(False)
                        return producto
        return None

    def calcularTotal(self):
        total = 0
        for producto in self.orden:
            total += producto.getPrecio()
        return total

    def agregarOrden(self, producto):
        if 0 < len(self.orden):
            for p in self.orden:
                if producto.getNombre() == p.getNombre() and producto.getTamaño() == p.getTamaño():
                    p.setCantidad(p.getCantidad() + producto.getCantidad())
                    p.setPrecio(p.getPrecio() + producto.getPrecio())
                    break
        else:
            self.orden.append(producto)

    def descontarProducto(self, producto):
        for p in self.orden:
            if p.getNombre() == producto.getNombre() and p.getTamaño() == producto.getTamaño():
                p.setPrecio(p.getPrecio() - producto.getPrecio())
                break

    @staticmethod
    def validarBono(codigo, servicio):
        for bono in servicio.bonos_cliente:
            if bono.getCodigo() == codigo and bono.getTipoServicio() == servicio.getNombre():
                producto = bono.getProducto
                for b in servicio.getCliente().getCineActual().getBonosCreados():
                    if b.getProducto() == producto and b.getCliente == Servicio.getCliente:
                        servicio.getCliente().getCineActual().getBonosCreados().remove(b)
                for b in servicio.getCliente().getBonos():
                    if b.getProducto() == producto :
                        servicio.getCliente().getBonos().remove(b)
                return producto
        return None

    def mostrarOrden(self):
        pedido = ""
        total = 0
        n = 0
        for producto in self.orden:
            n = n + 1 
            pedido += f"\n{n} -- {producto.getCantidad()} {producto.getNombre()} {producto.getTamaño()} : ${producto.getPrecio()}"
            total += producto.getPrecio()
        pedido += f"\nTotal: ${total}"
        return pedido

    def mostrarInventario(self):
        productos = "\n----------Productos disponibles----------\n\n0. Ningún producto"
        i = 0
        if len(self.inventario) == 0:
            return "\nNO HAY PRODUCTOS DISPONIBLES :(\n"
        for producto in self.inventario:
            if producto.getCantidad() == 0:
                disponibilidad = " --> NO HAY EN EL MOMENTO DE ESTE PRODUCTO"
            productos += f"\n{i + 1}. {producto.getNombre()} {producto.getTamaño()} ${producto.getPrecio()}{disponibilidad}"
        return productos

    def hacerPedido(self, indice, cantidad):
        producto_inventario = self.inventario[indice]
        if producto_inventario.getCantidad >= cantidad:
            producto_inventario.setCantidad(producto_inventario.getCantidad() - cantidad)
            producto = Producto(producto_inventario.nombre, producto_inventario.tamaño, cantidad)
            producto.setPrecio(producto_inventario.getPrecio() * cantidad)
            producto.setGenero(producto_inventario.getGenero())
            return producto
        return None

    # Getters and setters
    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def getCliente(self):
        return self.cliente

    def setCliente(self, cliente):
        self.cliente = cliente

    def getInventario(self):
        return self.inventario

    def setInventario(self, inventario):
        self.inventario = inventario

    def getOrden(self):
        return self.orden

    def setOrden(self, orden):
        self.orden = orden

    def getValorPedido(self):
        return self.valor_pedido

    def setValorPedido(self, valorPedido):
        self.valorPedido = valorPedido

    def getBonosCliente(self):
        return self.bonos_cliente

    def setBonosCliente(self, bonosCliente):
        self.bonosCliente = bonosCliente
