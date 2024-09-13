from gestionAplicacion.sucursalCine import SucursalCine
from datetime import datetime, time, timedelta
from gestionAplicacion.servicios.producto import Producto

class Membresia ():

    #Inicializador
    def __init__(self, nombre, categoria, valorSuscripcionMensual, duracionMembresiaDias):
        self._nombre = nombre
        self._categoria = categoria
        self._descuentoAsociado = 0.0
        self._valorSuscripcionMensual = valorSuscripcionMensual
        self._duracionMembresiaDias = duracionMembresiaDias
        self._tipoMembresia = 0
        SucursalCine.getTiposDeMembresia().append(self)

    #Metodos
    @classmethod
    def verificarMembresiaActual(cls, clienteProceso):
        """<b>Description</b>: Este método se encarga de verificar si el cliente tiene membresia activa.

	    <b>Param</b>: cliente : Se pide al cliente para revisar su atributo de tipo Membresia
	    <b>Return</b>: <b>string</b> : Se retorna un texto personalizado indicando si tiene membresia o no.
        """

        #Se crea las instancias
        mensaje = None
        membresiaActual = clienteProceso.getMembresia()
        nombreMensajeActual = None

        #Se actualiza el nombre de la membresia.
        if (membresiaActual == None):
            mensaje = "Bienvenido, " + clienteProceso.getNombre() + ".\nActualmente, no tiene membresía activa en el sistema.\nPor favor, seleccione la membresía que desea adquirir:\n"
        else:
            nombreMensajeActual = membresiaActual.getNombre()
            mensaje = "Bienvenido, " + clienteProceso.getNombre() + ".\nActualmente, su membresía es " + nombreMensajeActual + " de categoría " + membresiaActual.getCategoria() + "\nPor favor, seleccione la membresía que desea adquirir/actualizar:\n"

        return mensaje

    @classmethod
    def asignarDescuento(cls):
        """<b>Description</b>: Este método se encarga de asignar los descuentos dependiendo de la categoria de la membresia.

	    <b>param</b>: none : No se necesitan parametros.
	    <b>return</b>: <b>void</b> : No realiza retorno. El sistema asigna el correspondiente descuento dependiendo de la categoria recorrida en el array.
        """
        #Se realiza un ciclo y se toma la categoria de cada membresia para asignar el descuento con switch.
        for membresia in SucursalCine.getTiposDeMembresia:
            categoria = membresia.getCategoria()
            descuento = 0.05
            descuento+=0.05*categoria

            membresia.setDescuentoAsociado(descuento)


    @classmethod
    def mostrarCategoria(cls, clienteProceso, sucursalCineProceso):
        """<b>Description</b>: Este método se encarga de mostrar las categorias de membresias disponibles que hayan en la sucursal actual.
	    Se realiza una búsqueda de los objetos de tipo Producto que sean de Membresia en el inventario de la sucursal. En caso
	    de que la cantidad de alguno de estos productos este en 0, se indica al cliente que la opción esta agotada.
	    Otra notación es que si el cliente ya posse una membresía y aún no esta en plazo de renovación, se omite su selección para tener mejor control sobre nuestras unidades limitadas en el inventario de la sucursal de la compra.

	    <b>param</b>: clienteProceso : Se pide al cliente para verificar si posee membresía, lo cual modifica el resultado del método.
	    <b>param</b>: sucursalCineProceso : Se pide la sucursal actual para poder realizar la búsqueda de objetos de tipo Producto pertenecientes a Membresía.
	    <b>return</b>: <b>string</b> : Se retorna un texto mostrando el nombre de las categorias disponibles en la sucursal de la compra.
        """

        resultado = []
        i = 1
        membresiaActual = clienteProceso.getMembresia()
        nombreMembresiaActual = None
        #Se actualiza el nombre de la membresia.
        if (membresiaActual == None):
            nombreMembresiaActual = "Sin membresía"

        else:
            nombreMembresiaActual = membresiaActual.getNombre()

        #Se recorre la lista de tipos de membresia.
        for productoMembresia in sucursalCineProceso.getInventarioCine():
            #Se ignora los productos que no sean de tipo Membresia.
            if (productoMembresia.getTipoProducto()!="Membresia"):
                continue

            if (productoMembresia.getCantidad == 0 and nombreMembresiaActual != productoMembresia.getNombre()):
                texto = f"Categoría {i}. {productoMembresia.getNombre()} (AGOTADA)"
                resultado.append(texto)
                i+=1
                continue

            #Si el cliente ya tiene esta membresia y además, le faltan más de 5 dias para que expire, no se muestra en el menu.
            elif(nombreMembresiaActual == productoMembresia.getNombre() and 
                    (clienteProceso.getFechaLimiteMembresia() - datetime(6)) > SucursalCine.getFechaActual() and
                    clienteProceso.getFechaLimiteMembresia() > SucursalCine.getFechaActual()):
                i+=1
                continue

            elif(productoMembresia.getNombre() == "Challenger" or productoMembresia.getNombre() == "Radiante"):
                    if (productoMembresia.getNombre() == "Challenger"):
                        texto = f"Categoría {i}. {productoMembresia.getNombre()}. Requisitos: {int(productoMembresia.getPrecio())} puntos y peliculas vistas: 10"
                        resultado.append(texto)
                    else:
                        texto = f"Categoría {i}. {productoMembresia.getNombre()}. Requisitos: {int(productoMembresia.getPrecio())} puntos y peliculas vistas: 15"
                        resultado.append(texto)
            else:
                texto = f"Categoría {i}. {productoMembresia.getNombre()}. Requisitos: {int(productoMembresia.getPrecio())} puntos"
                resultado.append(texto)
            i+=1
        return resultado


    @classmethod
    def verificarRestriccionMembresia(cls, clienteProceso, categoriaSeleccionada, sucursalCineProceso):
        """<b>Description</b>: Este método verifica a que categorias puede acceder el cliente. Se revisa si hay membresias disponibles y si el cliente tiene la cantidad de puntos e historial de peliculas como requisitos.

	    <b>param</b>: clienteProceso : Se pide al cliente para revisar su historial de peliculas para la verificación. Si tiene X peliculas vistas en el cine, tiene acceso a ciertas categorias.
	    <b>param</b>: categoriaSeleccionada : Se pide el número de la categoria que quiera adquirir.
	    <b>param</b>: sucursalCineProceso : Se pide la sucursal de cine para revisar la cantidad de membresias.
	    <b>return</b>: <b>boolean</b> : Se retorna un dato booleano que indica si el cliente puede adquirir la categoria de membresia seleccionada.
        """

        membresiaProceso = Membresia.asignarMembresiaNueva(categoriaSeleccionada)
        esValido = False

        #Se obtiene los puntos que posea el cliente.
        puntos = 0.0
        for metodoPago in clienteProceso.getMetodosDePago():
            if (metodoPago.getNombre() == "Puntos"):
                puntos = metodoPago
                break
            else:
                puntos = clienteProceso.getPuntos()

        #Se obtiene la cantidad de la membresia que hayan en el cine.
        membresiaStock = 0
        for productoMembresia in sucursalCineProceso.getInventarioCine():
            if (productoMembresia.getNombre() == membresiaProceso.getNombre()):
                membresiaStock = productoMembresia.getCantidad()
                break

        #Se realizan diferentes validaciones dependiendo si el cliente va a realizar una renovación o nueva subscripción.
        if (clienteProceso.getMembresia() == None or clienteProceso.getMembresia().getCategoria() != categoriaSeleccionada):
        #Si la categoria es 4 o 5, se revisa si se cumple los requisitos.
            #En caso de no tener membresía.
            if (categoriaSeleccionada == 1):
                esValido = True if membresiaStock > 0 else False
            elif (categoriaSeleccionada == 2):
                esValido = True if membresiaStock > 0 and puntos >= 5000 else False
            elif (categoriaSeleccionada == 3):
                esValido = True if membresiaStock > 0 and puntos >= 10000 else False
            elif (categoriaSeleccionada == 4):
                esValido = True if membresiaStock > 0 and len(clienteProceso.getHistorialDePeliculas()) >= 10 and puntos >= 15000 else False
            elif (categoriaSeleccionada == 5):
                esValido = True if membresiaStock > 0 and len(clienteProceso.getHistorialDePeliculas()) >= 15 and puntos >= 20000 else False

        #En caso de realizar la renovación de la misma membresia.
        elif (clienteProceso.getMembresia() != None and
              (clienteProceso.getFechaLimiteMembresia() - datetime(6))> SucursalCine.getFechaActual and
              clienteProceso.getMembresia().getCategoria() == categoriaSeleccionada):
            if (categoriaSeleccionada == 1):
                esValido = True
            elif(categoriaSeleccionada == 2):
                esValido = True if puntos >= 5000 else False
            elif(categoriaSeleccionada == 3):
                esValido = True if puntos >= 10000 else False
            elif(categoriaSeleccionada == 4):
                esValido = True if len(clienteProceso.getHistorialDePeliculas()) >= 10 and puntos >= 15000 else False
            elif(categoriaSeleccionada == 5):
                esValido = True if len(clienteProceso.getHistorialDePeliculas()) >= 15 and puntos >= 20000 else False

        return esValido
    
    @classmethod
    def asignarTipoMembresia(cls):
        """<b>Description</b>: Este método asigna el tipo a la categoria de la membresia para ser usado posteriormente en otras funcionalidades.

	    <b>param</b>: none : No se solicitan parametros.
	    <b>return</b>: <b>void</b> : No retorna ningún dato ya que solo actualiza el tipo de las membresias existentes.
        """

        #Se revisa la lista de Tipos de Membresia y se asigna el tipo
        for membresia in SucursalCine.getTiposDeMembresia:
            if (membresia.getCategoria() > 0 and membresia.getCategoria() <= 3):
                membresia.setTipoMembresia(1)
            elif(membresia.getCategoria() > 3 and membresia.getCategoria() <= 5):
                membresia.setTipoMembresia(2)


    @classmethod
    def asignarMembresiaNueva(categoriaMembresia):
        """<b>Description</b>: Este método se encarga de asignar la nueva membresia con un apuntador de Membresia que coincida con la opción seleccionada durante el proceso de compra.

	    <b>param</b>: membresia : Se pide una instancia de tipo de membresia para usarlo como apuntador.
	    <b>param</b>: categoriaMembresia : Se pide un entero que es la selección de la membresia.
	    <b>return</b>: <b>Membresia</b> : Se retorna un dato de tipo Membresia que contiene el apuntador de tipo Membresia que coincide con la categoria deseada.
        """
        #Se crea una instancia de tipo Membresia None
        membresiaNueva = None

        #Se busca las instancias de tipo Membresia en Tipos de Membresia y si la categoria coincide, la instancia anterior apunta a este resultado
        for membresia2 in SucursalCine.getTiposDeMembresia():
            if (membresia2.getCategoria() == categoriaMembresia):
                membresiaNueva = membresia2
                break

        return membresiaNueva


    @classmethod
    def stockMembresia(cls, sucursalesCine = []):
        """<b>Description</b>: Este método se encarga de añadir al inventario de cada sucursal de cine, 
	    los productos de tipo Membresia que se usarán para limitar las membresias que se puede adquirir en cada sucursal.
	    Por cada sucursal de cine en el lista, se crean los productos que corresponden a cada membresia con una cantidad limitada.
	    Esto se usa para tener un control sobre el número de membresia que se pueden adquirir en cada cine.

	    <b>param</b>: sucursalesCine : Se pide la lista que contiene las sucursales de cine creadas para acceder a su inventario y añadir los objetos de tipo Producto pertenecientes a Membresía.
        """
        i = 50
        puntos = 0
        #Se revisa la lista de las sucursales de cine creadas.
        for sucursalCine in SucursalCine.getSucursalesCine():
            #Por cada membresia, se crea un producto de este tipo y se añade al inventario de la sucursal.
            for membresia in SucursalCine.getTiposDeMembresia():
                membresiaSucursal = Producto(nombre=membresia.getNombre(), cantidad=i, tipoProducto="Membresia", precio=puntos, sucursalSede=sucursalCine)
                puntos+=5000
                i-=10
            #Se reinicia el contador de cantidad y puntos cada vez que se itere a una nueva sucursal de la lista.
            i = 50
            puntos = 0

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
