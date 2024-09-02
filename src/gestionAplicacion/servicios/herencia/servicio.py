import random
import datetime
from typing import List, Optional

class Producto:
    def __init__(self, nombre: str, tamaño: str, cantidad: int, precio: float = 0.0, genero: str = ""):
        self.nombre = nombre
        self.tamaño = tamaño
        self.cantidad = cantidad
        self.precio = precio
        self.genero = genero

    def setCantidad(self, cantidad: int):
        self.cantidad = cantidad

    def setPrecio(self, precio: float):
        self.precio = precio

    def setGenero(self, genero: str):
        self.genero = genero

class Bono:
    def __init__(self, producto: Producto, codigo: str, tipo_servicio: str, cliente):
        self.producto = producto
        self.codigo = codigo
        self.tipo_servicio = tipo_servicio
        self.cliente = cliente

class SucursalCine:
    sucursales_cine = []
    fecha_actual = datetime.datetime.now()

    @staticmethod
    def getSucursalesCine():
        return SucursalCine.sucursales_cine

    @staticmethod
    def getFechaActual():
        return SucursalCine.fecha_actual

class Cliente:
    def __init__(self, cine_actual: SucursalCine):
        self.cine_actual = cine_actual
        self.bonos = []

    def getCineActual(self):
        return self.cine_actual

    def getBonos(self):
        return self.bonos

class Servicio:
    def __init__(self, nombre: str = ""):
        self.nombre = nombre
        self.cliente = None
        self.inventario: List[Producto] = []
        self.orden: List[Producto] = []
        self.bonos_cliente: List[Bono] = []
        self.valor_pedido = 0.0

    def descuentar_por_compra(self, metodo_pago):
        raise NotImplementedError

    def actualizar_inventario(self):
        raise NotImplementedError

    @staticmethod
    def mostrar_bonos(servicio) -> str:
        bono = "\n====== Tienes los siguientes bonos disponibles ======\n" + "\n0. No reclamar ningún bono."
        for i, b in enumerate(servicio.bonos_cliente):
            bono += f"\n{i + 1}. {b.producto.nombre} {b.producto.tamaño} código: {b.codigo}"
        return bono

    def actualizar_bonos(self):
        self.bonos_cliente = [bono for bono in self.cliente.getCineActual().bonos_creados 
                              if bono.tipo_servicio.lower() == self.nombre.lower() and bono.cliente == self.cliente]

    def descuentar_por_genero(self, cine) -> Optional[Producto]:
        for producto in self.orden:
            for ticket in cine.getTicketsParaDescuento():
                if producto.genero.lower() == ticket.getPelicula().getGenero().lower() and self.cliente == ticket.getDueno():
                    fecha = SucursalCine.getFechaActual().date()
                    if fecha == ticket.getHorario().date() and ticket.isDescuento():
                        ticket.setDescuento(False)
                        return producto
        return None

    def calcular_total(self) -> float:
        return sum(producto.precio for producto in self.orden)

    def agregar_orden(self, producto: Producto):
        for i, p in enumerate(self.orden):
            if producto.nombre == p.nombre and producto.tamaño == p.tamaño:
                p.setCantidad(p.cantidad + producto.cantidad)
                p.setPrecio(p.precio + producto.precio)
                break
        else:
            self.orden.append(producto)

    def descontar_producto(self, producto: Producto):
        for p in self.orden:
            if p.nombre == producto.nombre and p.tamaño == producto.tamaño:
                p.setPrecio(p.precio - producto.precio)
                break

    @staticmethod
    def validar_bono(codigo: str, servicio) -> Optional[Producto]:
        for bono in servicio.bonos_cliente:
            if bono.codigo == codigo and bono.tipo_servicio.lower() == servicio.nombre.lower():
                producto = bono.producto
                servicio.cliente.getCineActual().bonos_creados = [b for b in servicio.cliente.getCineActual().bonos_creados if b.producto != producto]
                servicio.cliente.bonos = [b for b in servicio.cliente.bonos if b.producto != producto]
                return producto
        return None

    def mostrar_orden(self) -> str:
        pedido = ""
        total = 0
        for i, producto in enumerate(self.orden):
            pedido += f"\n{i + 1} -- {producto.cantidad} {producto.nombre} {producto.tamaño} : ${producto.precio}"
            total += producto.precio
        pedido += f"\nTotal: ${total}"
        return pedido

    def mostrar_inventario(self) -> str:
        productos = "\n----------Productos disponibles----------\n\n0. Ningún producto"
        if not self.inventario:
            return "\nNO HAY PRODUCTOS DISPONIBLES :(\n"
        for i, producto in enumerate(self.inventario):
            disponibilidad = " --> NO HAY EN EL MOMENTO DE ESTE PRODUCTO" if producto.cantidad == 0 else ""
            productos += f"\n{i + 1}. {producto.nombre} {producto.tamaño} ${producto.precio}{disponibilidad}"
        return productos

    def hacer_pedido(self, indice: int, cantidad: int) -> Optional[Producto]:
        producto_inventario = self.inventario[indice]
        if producto_inventario.cantidad >= cantidad:
            producto_inventario.setCantidad(producto_inventario.cantidad - cantidad)
            producto = Producto(producto_inventario.nombre, producto_inventario.tamaño, cantidad)
            producto.setPrecio(producto_inventario.precio * cantidad)
            producto.setGenero(producto_inventario.genero)
            return producto
        return None

    def seleccionar_sucursal_aleatoriamente(self, sucursal_cine: SucursalCine) -> SucursalCine:
        while True:
            numero_aleatorio = random.randint(0, len(SucursalCine.getSucursalesCine()) - 1)
            sucursal_seleccionada = SucursalCine.getSucursalesCine()[numero_aleatorio]
            if sucursal_cine != sucursal_seleccionada:
                return sucursal_seleccionada

    # Getters and setters
    def getNombre(self) -> str:
        return self.nombre

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getCliente(self) -> Cliente:
        return self.cliente

    def setCliente(self, cliente: Cliente):
        self.cliente = cliente

    def getInventario(self) -> List[Producto]:
        return self.inventario

    def setInventario(self, inventario: List[Producto]):
        self.inventario = inventario

    def getOrden(self) -> List[Producto]:
        return self.orden

    def setOrden(self, orden: List[Producto]):
        self.orden = orden

    def getValorPedido(self) -> float:
        return self.valor_pedido

    def setValorPedido(self, valor_pedido: float):
        self.valor_pedido = valor_pedido

    def getBonosCliente(self) -> List[Bono]:
        return self.bonos_cliente

    def setBonosCliente(self, bonos_cliente: List[Bono]):
        self.bonos_cliente = bonos_cliente
