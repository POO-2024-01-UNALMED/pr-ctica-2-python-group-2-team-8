from gestionAplicacion.sucursalCine import SucursalCine

class Cliente():
    
    def __init__(self, nombre = "", edad = 0 , documento = 0, tipoDocumento = None, membresia = None,
                  cuenta = None, codigosDescuento =[], codigosBonos= [], bonos= []):
        self._nombre = nombre
        self._edad = edad
        self._documento = documento
        self._tipoDocumento = tipoDocumento
        self._membresia = membresia

        #Atributos Funcionalidad 4
        self._cuenta = cuenta
        self._codigosDescuento = codigosDescuento
        self._codigosBonos = codigosBonos
        self._bonos = bonos

        SucursalCine.getClientes.append(self)



    #Metodos

    #Description: Este metodo se encarga de mostrar el historial de peliculas que cada cliente ha visto hasta el momento para poder 
    #hacer una calificacion en concreto de las peliculas que el cliente se vio, evitando que el cliente pueda calificar 
    #una pelicula que no haya visto.

    def mostrar_pelicula_para_calificar(peliculas_disponibles_para_calificar):
        peliculas = ""
        for i, pelicula in enumerate(peliculas_disponibles_para_calificar, start=1):
            if peliculas:
                peliculas += "\n"
            peliculas += f"{i}. {pelicula.nombre} {pelicula.tipo_de_formato}"
        return peliculas
        
    #Description:Este metodo se encarga de mostrar el historial de comida que cada cliente ha consumido hasta el momento
    # para poder  hacer una calificacion en concreto de los productos que el cliente cosnumio, evitando que el cliente pueda calificar 
    #un producto que no haya consumido.

    def mostrar_productos_para_calificar(productos_disponibles_para_calificar):
        pedidos = ""
        for i, producto in enumerate(productos_disponibles_para_calificar, start=1):
            if pedidos:
                pedidos += "\n"
            pedidos += f"{i}. {producto.nombre} {producto.tamaño}"
        return pedidos

    def verificarCuenta(self):

        """
        Description: Este método verifica si el usuario tiene asociada una cuenta de tarjeta cinemar.

        :return boolean: Retorna true or false dependiendo si el cliente tiene cuenta Cinemar o no.
        """
        if self._cuenta != None:
            return True
        else:
            return False
        
    def mostrarCodigosDescuento(self):

        """
        :Description: Este metodo se encarga de retornar la lista de los codigos de descuento que el usuario
	    tiene disponibles para redimir por la compra de tickets de peliculas.

        :return String: retorna la Lista de codigos disponibles
        """
        
        cadena = ""

        for i in range(0,len(self._codigosDescuento)):
            cadena+= (i+1) + ". "+ self._codigosDescuento[i]+"\n"

        cadena+= (len(self._codigosDescuento)+1) + ". Ninguno\n" + (len(self._codigosDescuento)+2) + ". Salir y Guardar\n"
 
    
 
 
    #Getters and Setters
    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getMembresia(self):
        return self._membresia

    def setNombre(self, membresia):
        self._membresia = membresia

    def getCodigosDescuento(self):
        return self._codigosDescuento

    def setCodigosDescuento(self, codigosDescuento):
        self._codigosDescuento = codigosDescuento

    def getCodigosBonos(self):
        return self._codigosBonos

    def setCodigosBonos(self, codigosBonos):
        self._codigosBonos = codigosBonos

    def getBonos(self):
        return self._bonos

    def setBonos(self, bonos):
        self._bonos = bonos

    def getEdad(self):
        return self._edad

    def setEdad(self, edad):
        self._edad = edad

    def getDocumento(self):
        return self._documento

    def setDocumento(self, documento):
        self._documento = documento

    def getTipoDocumento(self):
        return self._tipoDocumento

    def setTipoDocumento(self, tipoDocumento):
        self._tipoDocumento = tipoDocumento