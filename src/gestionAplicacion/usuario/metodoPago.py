

class MetodoPago():

    #Inicializador
    def __init__(self, nombre, descuentoAsociado, limiteMaximoPago, tipo):
        self._nombre = nombre
        self._descuentoAsociado = descuentoAsociado
        self._limiteMaximoPago = limiteMaximoPago
        self._tipo = tipo

    #Metodos

    #<b>Description</b>: Este método se encarga de mostrar los métodos de pago disponibles con
	#sus descuentos.
	#El resultado puede cambiar si el cliente posee membresia y el tipo de esta.
	#@param cliente : Se usa el objeto de tipo Cliente para acceder a su lista de métodos de pago.
	#@return <b>string</b> : Se retorna un texto mostrando el nombre de los métodos de pago con
	#sus descuentos.
    @classmethod
    def mostrarMetodosDePago(cls, clienteProceso):
        pass

    #<b>Description</b>: Este método se encarga de asignar los métodos de pago disponibles por 
	#su tipo de membresia a su lista de métodos de pago.
	#que tiene el cliente.
	#@param cliente : Se usa el objeto de tipo Cliente para revisar su membresia y poder asignar
	#los métodos de pago.
	#@return <b>Lista de métodos de pago</b> : Se retorna una lista mostrando los métodos de pago luego
	#de realizar el filtrado por la membresia.
    @classmethod
    def asignarMetodosDePago(cls, clienteProceso):
        pass

    #<b>Description</b>: Este método se encarga de crear varias instancias de los métodos de
	#pago con distinto tipo. Esto para usarse en la funcionalidad 5.
	#@param metodopago : Se usa el objeto de MetodoPago para crear sus instancias.
	#@return <b>void</b> : No se retorna dato. Se toman los atributos del objeto para
	#crear varias instancias. Estos valores son modificados dependiendo del número de tipo en
	#el ciclo for.
    @classmethod
    def metodoPagoPorTipo(cls, metodoPago):
        pass

    #<b>Description</b>: Este método de asignar el método de pago para ser usado.
	#@param metodoPagoAUsar : Se usa el número de la selección para poder escoger el método de pago.
	#@param cliente : Se usa el objeto de cliente para acceder a los métodos de pago.
	#@return <b>MetodoPago</b> : Se retorna el método de pago que coincide con la opción seleccionada.
    @classmethod
    def usarMetodoPago(cls, clienteProceso, metodoPagoAUsar):
        pass

    #Description : Este método se encarga de tomar el valor a pagar, aplicar el descuento del método de pago elegido por el cliente
	#y restarle el monto máximo que se puede pagar con ese método de pago, si el método de pago cubre el valor a pagar, éste se cambia se cambia a 0.
	#Además, este método se encarga de pasar la referencia del método de pago a los métodos de pago usados y quita la referencia de métodos de pago 
	#disponibles asociados al cliente.
	#En caso de que el cliente tenga una membresía, se realiza la acumulación de puntos en base al valor pagado.
	#@param precio : Se pide el valor a pagar, este se obtuvo anteriormente como variable durante el proceso de la funcionalidad
	#@param cliente : Se pide al cliente que va a efectuar el proceso de realizar pago. Se revisa si tiene asignado una membresía.
	#@return <b>double</b> : En caso de que el método de pago cubra el valor a pagar retorna 0, en caso de que no
	#retorna el valor restante a pagar.   
    def realizarPago(self, precio, clienteProceso):
        pass

    #Getters and Setters
    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre

    def getTipo(self):
        return self._tipo
    
    def setTipo(self, tipo):
        self._tipo = tipo

    def getDescuentoAsociado(self):
        return self._descuentoAsociado
    
    def setDescuentoAsociado(self, descuentoAsociado):
        self._descuentoAsociado = descuentoAsociado

    def getLimiteMaximoPago(self):
        return self._limiteMaximoPago
    
    def setLimiteMaximoPago(self, limiteMaximoPago):
        self._limiteMaximoPago = limiteMaximoPago