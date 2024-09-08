class Producto():
    def __init__(self, nombre = "", tamaño = "", cantidad = 0, tipoProducto = "", genero = "", precio = 0.0, sucursalSede = None) :
        self._genero=genero
        self._nombre=nombre
        self._precio=precio
        self._tamaño=tamaño
        self._tipoProducto=tipoProducto
        self._cantidad=cantidad
        self._valoracionComida=4.0
        self._sucursalSede=sucursalSede
        self._totalEncuestasDeValoracionRealizadasComida=25
        self._strikeCambio = False
        sucursalSede.getInventarioCine().append(self)

    def comprobarBonoEnOrden(self, servicio):
        for producto in servicio.getOrden():
            if producto.getNombre() == self._nombre and producto.getTamaño() == self._tamaño and producto.getPrecio() > 0:
               return True 
        return False
    
    def getGenero(self):
        return self._genero

    def setGenero(self, genero):
        self._genero = genero

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getPrecio(self):
        return self._precio

    def setPrecio(self, precio):
        self._precio = precio

    def getTamaño(self):
        return self._tamaño

    def setTamaño(self, tamaño):
        self._tamaño = tamaño

    def getTipoProducto(self):
        return self._tipoProducto

    def setTipoProducto(self, tipoProducto):
        self._tipoProducto = tipoProducto

    def getCantidad(self):
        return self._cantidad

    def setCantidad(self, cantidad):
        self._cantidad = cantidad

    def getValoracionComida(self):
        return self._valoracionComida

    def setValoracionComida(self, valoracionComida):
        self._valoracionComida = valoracionComida

    def getSucursalSede(self):
        return self._sucursalSede

    def setSucursalSede(self, sucursalSede):
        self._sucursalSede = sucursalSede

    def getTotalEncuestasDeValoracionRealizadasComida(self):
        return self._totalEncuestasDeValoracionRealizadasComida

    def setTotalEncuestasDeValoracionRealizadasComida(self, totalEncuestasDeValoracionRealizadasComida):
        self._totalEncuestasDeValoracionRealizadasComida = totalEncuestasDeValoracionRealizadasComida

    def getStrikeCambio(self):
        return self._strikeCambio

    def setStrikeCambio(self, strikeCambio):
        self._strikeCambio = strikeCambio