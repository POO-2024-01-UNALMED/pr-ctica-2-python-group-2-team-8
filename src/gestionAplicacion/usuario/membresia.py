class Membresia ():

    #Inicializador
    def __init__(self, nombre, categoria, descuentoAsociado, valorSuscripcionMensual, duracionMembresiaDias, tipoMembresia):
        self._nombre = nombre
        self._categoria = categoria
        self._descuentoAsociado = descuentoAsociado
        self._valorSuscripcionMensual = valorSuscripcionMensual
        self._duracionMembresiaDias = duracionMembresiaDias
        self._tipoMembresia = tipoMembresia

    #Metodos
	#<b>Description</b>: Este método se encarga de verificar si el cliente tiene membresia activa
	#@param cliente : Se pide al cliente para revisar su atributo de tipo Membresia
	#@return <b>string</b> : Se retorna un texto personalizado indicando si tiene membresia
	#o no.
    @classmethod
    def verificarMembresiaActual(cls, clienteProceso):
        pass

    #<b>Description</b>: Este método se encarga de verificar si el cliente tiene membresia activa
	#@param cliente : Se pide al cliente para revisar su atributo de tipo Membresia
	#@return <b>string</b> : Se retorna un texto personalizado indicando si tiene membresia
	#o no.
    @classmethod
    def asignarDescuento(cls):
        pass

    #<b>Description</b>: Este método se encarga de asignar los descuentos dependiendo de la
	#categoria de la membresia.
	#@param none : No se necesitan parametros.
	#@return <b>void</b> : No realiza retorno. El sistema asigna el correspondiente descuento
	#dependiendo de la categoria recorrida en el array.
    @classmethod
    def mostrarCategoria(cls, clienteProceso, sucursalCineProceso):
        pass

    #<b>Description</b>: Este método verifica a que categorias puede acceder el cliente. Se revisa
	#si hay membresias disponibles y si el cliente tiene la cantidad de puntos e historial de peliculas como requisitos.
	#@param clienteProceso : Se pide al cliente para revisar su historial de peliculas para la 
	#verificación. Si tiene X peliculas vistas en el cine, tiene acceso a ciertas categorias.
	#@param categoriaSeleccionada : Se pide el número de la categoria que quiera adquirir.
	#@param sucursalCineProceso : Se pide la sucursal de cine para revisar la cantidad de membresias.
	#@return <b>boolean</b> : Se retorna un dato booleano que indica si el cliente puede 
	#adquirir la categoria de membresia seleccionada.
    @classmethod
    def verificarRestriccionMembresia(cls, clienteProceso, categoriaSeleccionada, sucursalCineProceso):
        #Se crea las instancias
        mensaje = None
        membresiaActual = clienteProceso.getMembresia()
        nombreMembresiaActual = None

        #Se actualiza el nombre de la membresia.
        if (membresiaActual == None):
            mensaje = "Bienvenido, " + clienteProceso.getNombre() + "\nActualmente, no tiene membresia activa en el sistema.\nPor favor, seleccione la membresia que desea adquirir:\n"
        else:
            nombreMembresiaActual = clienteProceso.getMembresia().getNombre()
            mensaje = "Bienvenido, " + clienteProceso.getNombre() + "\n"



    #<b>Description</b>: Este método asigna el tipo a la categoria de la membresia para
	#ser usado posteriormente en otras funcionalidades.
	#@param none : No se solicitan parametros.
	#@return <b>void</b> : No retorna ningún dato ya que solo actualiza el tipo 
	#de las membresias existentes.
    @classmethod
    def asignarTipoMembresia(cls):
        pass

    #<b>Description</b>: Este método se encarga de añadir al inventario de cada sucursal de cine, 
	#los productos de tipo Membresia que se usarán para limitar las membresias que se puede adquirir en cada sucursal.
	#Por cada sucursal de cine en el lista, se crean los productos que corresponden a cada membresia con una cantidad limitada.
	#Esto se usa para tener un control sobre el número de membresia que se pueden adquirir en cada cine.
	#@param sucursalesCine : Se pide la lista que contiene las sucursales de cine creadas para acceder a su inventario y añadir los objetos
	#de tipo Producto pertenecientes a Membresía.
    @classmethod
    def stockMembresia(cls, sucursalesCine = []):
        pass

    #Getters and Setter
    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre

    def getCategoria(self):
        return self._categoria
    
    def setCategoria(self, categoria):
        self._categoria = categoria

    def getDuracionMembresiaDias(self):
        return self._duracionMembresiaDias
    
    def setDuracionMembresiaDias(self, duracionMembresiaDias):
        self._duracionMembresiaDias = duracionMembresiaDias

    def getTipoMembresia(self):
        return self._tipoMembresia
    
    def setTipoMembresia(self, tipoMembresia):
        self._tipoMembresia = tipoMembresia

    








