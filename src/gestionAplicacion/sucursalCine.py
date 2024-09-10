from datetime import datetime, time, timedelta
import random
#from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.proyecciones.pelicula import Pelicula
from gestionAplicacion.proyecciones.salaCine import SalaCine
from gestionAplicacion.servicios.herencia.servicioComida import ServicioComida
from gestionAplicacion.servicios.herencia.servicioSouvenirs import ServicioSouvenir
from gestionAplicacion.usuario.cliente import Cliente

class SucursalCine:

#Attributes
################################################

    #Static Attributes
    _cantidadSucursales = 0
    _fechaActual = None
    _fechaValidacionNuevoDiaDeTrabajo = None
    _fechaRevisionLogicaDeNegocio = None
    _sucursalesCine = []
    _ticketsDisponibles = []
    _juegos = []
    _clientes = []
    _metodosDePagoDisponibles = []

    #Constants
    _INICIO_HORARIO_LABORAL = time(10,00)
    _FIN_HORARIO_LABORAL = time(23, 00)
    _TIEMPO_LIMPIEZA_SALA_DE_CINE = timedelta( minutes=30 )
    _TIEMPO_LIMITE_RESERVA_TICKET = timedelta( minutes=15 )
   

    #Instance Attributes
    def __init__(self, ubicacion):
        self._ubicacion = ubicacion
        
        SucursalCine._cantidadSucursales += 1
        self._idSucursal = SucursalCine._cantidadSucursales
        SucursalCine._sucursalesCine.append(self)

        self._inventarioCine = []
        self._ticketsParaDescuento = []
        self._servicios = []
        self._bonosCreados = []
        self._salasDeCine = []
        self._cartelera = []
        self._cantidadTicketsCreados = 1
    
#Methods
################################################

    #def mostrarSucursalesCine(cls)

    @classmethod
    def actualizarPeliculasSalasDeCine(cls):

        """
        :Description: Este método se encarga de actualizar las salas de todas las sedes, para esto, 
        iteramos sobre el ArrayList de las sedes, luego iteramos sobre el ArrayList de las salas de 
        cine de cada sede y ejecutamos su método de actualizar peliculas en presentación.
        """

        for sede in SucursalCine._sucursalesCine:
            for salaDeCine in sede._salasDeCine:

                try:
                    if salaDeCine.getHorarioPeliculaEnPresentacion() + salaDeCine.getPeliculaEnPresentacion().getDuracion() <= SucursalCine._fechaActual:
                        salaDeCine.actualizarPeliculaEnPresentacion()
                except AttributeError:
                    salaDeCine.actualizarPeliculaEnPresentacion()
    
    @classmethod
    def _dropHorariosVencidos(cls):

        """
        :Description: Este método se encarga de eliminar los horarios que ya no pueden ser presentados al pasar de día
	    o luego de la deserialización, de todas las películas de cada sucursal, eliminando los horarios anteriores al día 
	    de la fecha actual. 
        """
        
        for sede in SucursalCine._sucursalesCine:

            for pelicula in sede._cartelera:

                horariosAEliminar = []

                for horario in pelicula.getHorariosPresentacion():

                    if horario.date() < SucursalCine._fechaActual.date():
                        horariosAEliminar.append(horario)
                
                for horario in horariosAEliminar:

                    pelicula.getAsientosSalasVirtuales().pop(pelicula.getHorariosPresentacion().indexOf(horario))
                    pelicula.getHorariosPresentacion().remove(horario)

    def _crearHorariosPeliculasPorSala(self):

        """
        :Description: Este método se encarga de crear máximo 20 horarios por cada película en cartelera de la sucursal de cine, 
	    teniendo en cuenta los siguientes criterios: 
	    <ol>
	    <li>El horario en el que se presentará la película se encuentra entre el horario de apertura y cierre de nuestras 
	    instalaciones.</li>
	    <li>La hora a la que termina la película es menor a la hora de cierre. </li>
	    <li>Al finalizar una película se tiene en cuenta el tiempo de limpieza de la sala de cine.</li>
	    <li>La creación de horarios no exceda una semana (Para ejecutar correctamente la lógica semanal de nuestro cine).</li>
	    <li>Si varias películas serán presentadas en una sala se presentarán de forma intercalada evitando colisiones.</li>
	    </ol>
        """
        
        peliculasDeSalaDeCine = []

        LIMITE_CREACION_HORARIOS_PRESENTACION = (SucursalCine._fechaActual + timedelta(weeks = 1)).date()

        for salaDeCine in self._salasDeCine:

            horarioParaPresentar = SucursalCine._fechaActual.replace(minute = 0, second = 0, microsecond = 0)

            for pelicula in self._cartelera:

                if pelicula.getSalaCinePresentacion() is salaDeCine:
                    peliculasDeSalaDeCine.append(pelicula)

            for i in range (0,20):

                if horarioParaPresentar.date() >= LIMITE_CREACION_HORARIOS_PRESENTACION:
                    break

                for pelicula in peliculasDeSalaDeCine:
                    
                    condicionCreacionEnJornadaLaboral = horarioParaPresentar.time() < SucursalCine._FIN_HORARIO_LABORAL and horarioParaPresentar.time() >= SucursalCine._INICIO_HORARIO_LABORAL
                    condicionCreacionDuranteJornadaLaboral = (horarioParaPresentar + pelicula.getDuracion()).time() <= SucursalCine._FIN_HORARIO_LABORAL and (horarioParaPresentar + pelicula.getDuracion()).date() == horarioParaPresentar.date()
                    
                    if  condicionCreacionEnJornadaLaboral and condicionCreacionDuranteJornadaLaboral:
                            pelicula.crearSalaVirtual(horarioParaPresentar)
                            horarioParaPresentar += pelicula.getDuracion() + SucursalCine._TIEMPO_LIMPIEZA_SALA_DE_CINE
                    else: 
                        if horarioParaPresentar.time() > SucursalCine._INICIO_HORARIO_LABORAL:
                            horarioParaPresentar += timedelta(days = 1)
                        
                        if horarioParaPresentar.date() >= LIMITE_CREACION_HORARIOS_PRESENTACION:
                            break
                    
                        horarioParaPresentar = horarioParaPresentar.replace(hour = SucursalCine._INICIO_HORARIO_LABORAL.hour, minute = SucursalCine._INICIO_HORARIO_LABORAL.minute)
                        horarioParaPresentar += pelicula.getDuracion() + SucursalCine._TIEMPO_LIMPIEZA_SALA_DE_CINE
        
            peliculasDeSalaDeCine.clear()

    def _distribuirPeliculasPorSala(self):

        """
        :Description: Este método se encarga de distribuir las películas en cartelera en las distintas salas de cine 
	    de la sucursal de cine que ejecuta este método, para esta distribución se tienen encuenta 3 casos posibles:
	    <ol>
	    <li>Hay menos películas que salas de cine o igual cantidad de ambas.</li>
	    <li>Hay más películas que salas de cine, pero caben exactamente la misma cantidad de películas en cada sala.</li>
	    <li>Hay más películas que salas de cine, pero al menos una sala de cine debe tener 1 película más que todas 
	    las otras (Principio de Dirichlet o del palomar).</li>
	    </ol>
        """
        
        formatos = ["2D", "3D", "4D"]

        for formato in formatos:

            grupoSalasPorFormato = []
            grupoPeliculasPorFormato = []

            cantidadMaxPeliculaPorSala = 0
            contador = 0

            indiceSalaDeCine = 0

            for salaDeCine in self._salasDeCine:
                if salaDeCine.getTipoSala() == formato:
                    grupoSalasPorFormato.append(salaDeCine)

            for pelicula in self._cartelera:
                if pelicula.getTipoDeFormato() == formato:
                    grupoPeliculasPorFormato.append(pelicula)
            
            if len(grupoPeliculasPorFormato) > len(grupoSalasPorFormato):

                cantidadMaxPeliculaPorSala = int(len(grupoPeliculasPorFormato) / len(grupoSalasPorFormato)) if len(grupoPeliculasPorFormato) % len(grupoSalasPorFormato) == 0 else int(len(grupoPeliculasPorFormato) / len(grupoSalasPorFormato)) + 1

                for pelicula in grupoPeliculasPorFormato:
                    pelicula.setSalaCinePresentacion(grupoSalasPorFormato[indiceSalaDeCine])
                    contador += 1

                    if contador == cantidadMaxPeliculaPorSala:
                        contador = 0
                        indiceSalaDeCine += 1

            else:
                
                for pelicula in grupoPeliculasPorFormato:

                    pelicula.setSalaCinePresentacion(grupoSalasPorFormato[indiceSalaDeCine])
                    indiceSalaDeCine += 1

    @classmethod
    def logicaSemanalSistemNegocio(cls):

        """
        :Description: Este método se encarga de realizar los preparativos para ejecutar la lógica de la funcionalidad #3:
	    <ol>
	    <li>Renueva las cantidades disponibles de los productos en inventario</li>
	    <li>Eliminar los horarios de la semana anterior.</li>
	    <li>Distribución de películas en las salas de cine y la creación de sus horarios.</li>
	    <li>Eliminar los tickets comprados de películas de la semana anterior.</li>
	    </ol>
        """
        
        SucursalCine._ticketsDisponibles.clear()

        for sede in SucursalCine._sucursalesCine:
            
            sede._distribuirPeliculasPorSala()
            sede._crearHorariosPeliculasPorSala()

    @classmethod
    def logicaInicioSIstemaReservarTicket(cls):

        """
        :Description: Este método se encarga de ejecutar toda la lógica para realizar reservas de ticket por primera vez,
	    se compone de 3 puntos principales:
	    <ol>
	    <li>Distribuir las películas en cartelera de cada sucursal de forma equitativa respecto a sus salas de cine.</li>
	    <li>Una vez realizada la distribución, crear los horarios en los que se presentará cada película.</li>
	    <li>Actualizar las películas cuyo horario se esta presentando en estos momentos.</li>
	    <li>Establecer las fechas cuando se ejecutarán la lógica diaria y semanal del negocio.</li>
	    </ol>
        """

        SucursalCine._fechaActual = datetime.now()

        for sede in SucursalCine._sucursalesCine:

            sede._distribuirPeliculasPorSala()
            sede._crearHorariosPeliculasPorSala()
        
        SucursalCine.actualizarPeliculasSalasDeCine()
        SucursalCine._fechaValidacionNuevoDiaDeTrabajo = SucursalCine._fechaActual.date() + timedelta(days = 1)
        SucursalCine._fechaRevisionLogicaDeNegocio = SucursalCine._fechaActual.date() + timedelta(weeks = 1)


    @classmethod
    def logicaDiariaReservarTicket(cls):
        
        ticketsAEliminar = []

        for sede in SucursalCine._sucursalesCine:

            #sede._ticketsParaDescuento.clear()

            for ticket in sede._ticketsDisponibles:
                
                if ticket.getSucursalCompra() == sede._ubicacion and ticket.getHorario().date() == SucursalCine._fechaActual:
                    #sede._ticketsParaDescuento.append(ticket)
                    pass

                if (ticket.getHorario() + ticket.getPelicula().getDuracion) < SucursalCine._fechaActual:
                    ticketsAEliminar.append(ticket)
                
        SucursalCine._dropHorariosVencidos()

        for ticket in ticketsAEliminar:
            SucursalCine._ticketsDisponibles.remove(ticket)
        
        for cliente in SucursalCine._clientes:
            cliente.dropTicketsCaducados() 

    #def obtenerSucursalPorId(cls):

    #def obetenerSalaDeCinePorId(self):

    #def obtenerPeliculaPorId(self):

    @classmethod
    def notificarFechaLimiteMembresia(cls):
        pass

#Description: Este metodo se encarga de remover los productos que fueron mal calificadas en dos sucursales, por lo
#tanto por temas de negocio decidimos eliminar este producto por malas ventas, usando la funcion remove, quitandola
#de la cartelera principal de peliculas.
	 
	 
    def eliminar_producto(self, productos_eliminar):
        for producto in productos_eliminar:
            if producto in self.inventario_cine:
                self.inventario_cine.remove(producto)

#Description : Este método se encarga de retornar los productos cuyo nombre coincide con el nombre del producto seleccionada por el cliente.
#@param nombreProducto : Este método recibe como parámetro el nombre del producto (De tipo String) con el cuál se realizará el filtrado.
#@param Inventario : Este método recibe como parámetro una lista (De tipo ArrayList<Producto>) que contiene 
#los productos previamente filtrados según los datos del cliente y su disponibilidad horaria.
#@return <b>ArrayList<Producto></b> : Este método retorna un ArrayList de los productos cuyo nombre coinciden con el nombre seleccionado 
#por el cliente.
	 
    def filtrar_por_nombre_de_producto(nombre_producto, inventario):
     productos_encontrados = []

     for producto in inventario:
        if producto.get_nombre() == nombre_producto:
            productos_encontrados.append(producto)

     return productos_encontrados 
    
#Description: Este metodo se encarga de analizar por semana que productos han sido bien o mal calificadas, evaluando
#las calificaciones de los clientes, si un producto es calificado por debajo de 3, lo consideramos como mal calificado
#y lo cambiamos de sede, y si la valoracion del producto esta por encima de 3 esta catalogada como bien, ya en el caso en que el 
#bono este calificado como mayor a 4.5, lo cambiamos de sede, ya que consideramos que es un muy buen producto, y 
#nos hara ganar mayor rentabilidad.Tambien se encarga de cambiar productos de sede, ya que en nuestra logica de negocio implementamos
#el sistema de calificaciones, entonces tenemos que estar constantemente pendientes de que productos han sido
#bien o mal recibidos por los clientes, y cambiandolos de sede, esperamos que su calificacion mejore, si esto
#no se da, el producto es eliminado del inventario, ya que se considera como malo.

    def logica_calificacion_productos(self, producto):
        productos_calificados = self.filtrar_por_nombre_de_producto(producto.get_nombre())
        
        verificacion_cambio = True

        if producto.get_valoracion_comida() < 3:
            if verificacion_cambio:
                sucursal = self.seleccionar_sucursal_aleatoriamente(producto.get_sucursal_sede())
                for producto1 in productos_calificados:
                    if producto1 in self.inventario_cine:
                        self.inventario_cine.remove(producto1)
                    if producto1.get_tipo_producto() == "comida":
                        new_producto = Producto(producto1.get_nombre(), producto1.get_tamaño(), producto1.get_tipo_producto(), producto1.get_precio() * 0.9, producto1.get_cantidad(), producto1.get_genero(), sucursal)
                        self.inventario_cine.append(new_producto)
                    elif producto1.get_tipo_producto() == "souvenir":
                        new_producto = Producto(producto1.get_nombre(), producto1.get_tamaño(), producto1.get_tipo_producto(), producto1.get_precio() * 0.9, producto1.get_cantidad(), producto1.get_genero(), sucursal)
                        self.inventario_cine.append(new_producto)
            else:
                self.eliminar_producto(productos_calificados)

        elif producto.get_valoracion_comida() > 4.5:
            sucursal1 = self.seleccionar_sucursal_aleatoriamente(producto.get_sucursal_sede())
            for producto2 in productos_calificados:
                if producto2.get_tipo_producto() == "comida":
                    new_producto = Producto(producto2.get_nombre(), producto2.get_tamaño(), producto2.get_tipo_producto(), producto2.get_precio() * 1.10, producto2.get_cantidad(), producto2.get_genero(), sucursal1)
                    self.inventario_cine.append(new_producto)
                elif producto2.get_tipo_producto() == "souvenir":
                    new_producto = Producto(producto2.get_nombre(), producto2.get_tamaño(), producto2.get_tipo_producto(), producto2.get_precio() * 1.10, producto2.get_cantidad(), producto2.get_genero(), sucursal1)
                    self.inventario_cine.append(new_producto)         

#Description: Este método se encarga de realizar la distribución de productos en los inventarios de los productos
#ccada semana luego de haber efectuado el cambio de producto de sucursal propio de la funcionalidad 3. 


    def logica_semanal_producto(sucursales_cine):
     for sede in sucursales_cine:
        for producto in sede.get_inventario_cine():
            if producto.get_tipo_producto() == "comida" or producto.get_tipo_producto() == "souvenir":
                sede.logica_calificacion_productos(producto) 

#Description: Este metodo se encarga de revisar en el arrayList de inventario que producto ha tenido
#la mejor calificacion, osea, el producto mas eficiente segun los gustos de los clientes, con este producto vamos 
#a generar combos en recompensa a los clientes que nos dejaron sus reseñas
	 
    def mejor_producto(self):
        producto_mejor_calificado = None
        primera_comparacion = True

        for producto in self.inventario_cine:
            if producto.get_tipo_producto().lower() in ["comida", "souvenir"]:
                if primera_comparacion:
                    producto_mejor_calificado = producto
                    primera_comparacion = False
                elif producto.get_valoracion_comida() > producto_mejor_calificado.get_valoracion_comida():
                    producto_mejor_calificado = producto

        return producto_mejor_calificado                   

#Description: Este metodo se encarga de revisar en el arrayList de inventario que producto ha tenido
#la peor calificacion, osea, el producto mas deficiente segun los gustos de los clientes, con este producto vamos 
#a generar combos en recompensa a los clientes que nos dejaron sus reseñas.

    def peor_producto(self):
        producto_peor_calificado = None
        primera_comparacion = True

        for producto in self.inventario_cine:
            if producto.get_tipo_producto().lower() in ["comida", "souvenir"]:
                if primera_comparacion:
                    producto_peor_calificado = producto
                    primera_comparacion = False
                elif producto.get_valoracion_comida() < producto_peor_calificado.get_valoracion_comida():
                    producto_peor_calificado = producto

        return producto_peor_calificado
    
#Description: Este metodo se encarga de revisar en el arrayList de peliculasDisponibles que pelicula ha tenido
#la mejor calificacion, osea, la pelicula mas eficiente segun los gustos de los clientes, con esta pelicula vamos 
#a generar combos en recompensa a los clientes que nos dejaron sus reseñas.
	 
    def mejor_pelicula(self):
        pelicula_mejor_calificada = None
        primera_comparacion = True

        for pelicula in self.cartelera:
            if pelicula.seleccionar_horario_mas_lejano() is None:
                continue

            if primera_comparacion:
                pelicula_mejor_calificada = pelicula
                primera_comparacion = False
            elif pelicula.get_valoracion() > pelicula_mejor_calificada.get_valoracion():
                pelicula_mejor_calificada = pelicula

        return pelicula_mejor_calificada
    
#Description: Este metodo se encarga de revisar en el arrayList de peliculasDisponibles que pelicula ha tenido
#la peor calificacion, osea, la pelicula mas deficiente segun los gustos de los clientes, con esta pelicula vamos 
#a generar combos en recompensa a los clientes que nos dejaron sus reseñas.

    def peor_pelicula(self):
        pelicula_peor_calificada = None
        primera_comparacion = True

        for pelicula in self.cartelera:
            if pelicula.seleccionar_horario_mas_lejano() is None:
                continue

            if primera_comparacion:
                pelicula_peor_calificada = pelicula
                primera_comparacion = False
            elif pelicula.get_valoracion() < pelicula_peor_calificada.get_valoracion():
                pelicula_peor_calificada = pelicula

        return pelicula_peor_calificada
    
#Description: Este metodo se encarga de analizar por semana que peliculas han sido bien o mal calificadas, evaluando
#las calificaciones de los clientes, si una pelicula es calificada por debajo de 3, la consideramos como mal calificada
#y la cambiamos de sede, y si la pelicula esta por encima de 3 esta catalogada como bien, ya en el caso en que la 
#pelicula este calificada como mayor a 4.5, la cambiamos de sede, ya que consideramos que es una muy buena pelicula, y 
#nos hara ganar mayor rentabilidad.Tambien se encarga de cambiar peliculas de sede, ya que en nuestra logica de negocio implementamos
#el sistema de calificaciones, entonces tenemos que estar constantemente pendientes de que peliculas han sido
#buenas o malas recibidas por los clientes, y cambiandolas de sede, esperamos que su calificacion mejore, si esto
#no se da, la pelicula es eliminada de la cartelera, ya que se considera como mala.

    def logica_calificacion_peliculas(self, pelicula):
        peliculas_calificadas = Pelicula.filtrar_por_nombre_de_pelicula(pelicula.get_nombre(), self.cartelera)
        if not peliculas_calificadas:
            return

        promedio = 0
        verificacion_cambio = True
        
        for pelicula in peliculas_calificadas:
            promedio += pelicula.get_valoracion()
            verificacion_cambio = verificacion_cambio and pelicula.is_strike_cambio()

        calificacion_real = promedio / len(peliculas_calificadas)

        if calificacion_real < 3:
            if verificacion_cambio:
                sucursal = self.seleccionar_sucursal_aleatoriamente()
                for pelicula1 in peliculas_calificadas:
                    self.eliminar_peliculas([pelicula1])
                    if pelicula1.get_tipo_de_formato() == "2D":
                        Pelicula(pelicula1.get_nombre(), int(pelicula1.precio * 0.9), pelicula1.genero, pelicula1.duracion, pelicula1.clasificacion, pelicula1.get_tipo_de_formato(), sucursal)
            else:
                self.eliminar_peliculas(peliculas_calificadas)
        elif calificacion_real > 4.5:
            sucursal = self.seleccionar_sucursal_aleatoriamente()
            for pelicula2 in peliculas_calificadas:
                if pelicula2.get_tipo_de_formato() == "2D":
                    Pelicula(pelicula2.get_nombre(), int(pelicula2.precio * 1.10), pelicula2.genero, pelicula2.duracion, pelicula2.clasificacion, pelicula2.get_tipo_de_formato(), sucursal)


#################### PORQUE ESTA ESTE METODO AQUI Y EN SERVICIO?????????????????????
#                    LE CORREGI LOS ERRORES QUE CHAT GPT LE HABIA HECHOPARA PODER EJECUTARLO

#Description: Este metodo se encarga de seleccionar las sucursales del arrayList y con el uso de la funcion random de la libreria math,
#se selecciona una sucursal aleatoriamente, ya que esto nos permetira mas adelante el cambio de sucursal de una
#pelicula a otra.
# 	 
    def seleccionar_sucursal_aleatoriamente(self,sucursal_cine):
     if len(sucursal_cine) <= 1:
        raise ValueError("No hay suficientes sucursales para seleccionar una diferente.")
    
     while True:
        numero_aleatorio = random.randint(0, len(sucursal_cine) - 1)
        sucursal_seleccionada = sucursal_cine[numero_aleatorio]
        if sucursal_cine != sucursal_seleccionada:
            return sucursal_seleccionada





#Getters and Setters
################################################

    def getIdSucursal(self):
        return self._idSucursal
    
    def setIdSucursal(self, idSucursal):
        self._idSucursal = idSucursal

    @classmethod
    def getCantidadSucursales(cls):
        return SucursalCine._cantidadSucursales
    
    @classmethod
    def setCantidadSucursales(cls, cantidadSucursales):
        SucursalCine._cantidadSucursales = cantidadSucursales
    
    def getUbicacion(self):
        return self._ubicacion
    
    def setUbicacion(self, ubicacion):
        self._ubicacion = ubicacion
    
    def getSalasDeCine(self):
        return self._salasDeCine
    
    def setSalasDeCine(self, salasDeCine):
        self._salasDeCine = salasDeCine
    
    def getCartelera(self):
        return self._cartelera
    
    def setCartelera(self, cartelera):
        self._cartelera = cartelera
    
    def getCantidadTicketsGenerados(self):
        return self._cantidadTicketsCreados

    def setCantidadTicketsCreados(self, cantidadTicketsCreados):
        self._cantidadTicketsCreados = cantidadTicketsCreados
    
    def getFechaActual(self):
        return SucursalCine._fechaActual
    
    def setFechaActual(self, fechaActual):
        SucursalCine._fechaActual = fechaActual

    @classmethod
    def getMetodosDePagoDisponibles(cls):
        return SucursalCine._metodosDePagoDisponibles
    
    @classmethod
    def setMetodosDePagoDisponibles(cls, metodosDePagoDisponibles):
        SucursalCine._metodosDePagoDisponibles = metodosDePagoDisponibles
    
    @classmethod
    def getTiempoLimpiezaSalaDeCine(cls):
        return SucursalCine._TIEMPO_LIMPIEZA_SALA_DE_CINE
    
    @classmethod
    def getTiempoLimiteReservaTicket(cls):
        return SucursalCine._TIEMPO_LIMITE_RESERVA_TICKET
    
    def getTicketsDisponibles(self):
        return SucursalCine._ticketsDisponibles
    
    @classmethod
    def setTicketsDisponibles(cls, ticketsDisponibles):
        SucursalCine._ticketsDisponibles = ticketsDisponibles

    @classmethod
    def getJuegos(cls):
        return SucursalCine._juegos

    @classmethod
    def setJuegos(cls, juegos):
        SucursalCine._juegos = juegos
    
    @classmethod
    def getClientes(cls):
        return SucursalCine._clientes

    @classmethod
    def setClientes(cls, clientes):
        SucursalCine._clientes = clientes

    @classmethod
    def getSucursalesCine(cls):
        return SucursalCine._sucursalesCine
    
    def getInventarioCine(self):
        return self._inventarioCine

    def setInventarioCine(self, inventarioCine):
        self._inventarioCine = inventarioCine

    def getTicketsParaDescuento(self):
        return self._ticketsParaDescuento

    def setTicketsParaDescuento(self, ticketsParaDescuento):
        self._ticketsParaDescuento = ticketsParaDescuento

    def getServicios(self):
        return self._servicios

    def setServicios(self, servicios):
        self._servicios = servicios

    def getBonosCreados(self):
        return self._bonosCreados

    def setBonosCreados(self, bonosCreados):
        self._bonosCreados = bonosCreados

if __name__ == '__main__':

    servicioComida = ServicioComida("comida")
    servicioSouvenirs = ServicioSouvenir("souvenir")

    sucursalCine1 = SucursalCine("Bucaramanga")
    sucursalCine2 = SucursalCine("Marinilla")
    sucursalCine3 = SucursalCine("Medellín")

    # Productos de la sucursal de Marinilla

    producto1 = Producto("Hamburguesa","Grande","comida",20000,200,"Normal",sucursalCine2)
    producto2 = Producto("Hamburguesa","Cangreburger","comida",25000,200,"Comedia",sucursalCine2)
    producto3 = Producto("Perro caliente","Grande","comida",15000,200,"Normal",sucursalCine2)
    producto4 = Producto("Perro caliente","Don salchicha","comida",20000,200,"Comedia",sucursalCine2)
    producto5 = Producto("Crispetas","cazador de Demonios","comida",14000,200,"Acción",sucursalCine2)
    producto6 = Producto("Crispetas","Grandes","comida",13000,200,"Normal",sucursalCine2)
    producto7 = Producto("Gaseosa","Grande","comida",4000,200,"Normal",sucursalCine2)
    producto8 = Producto("Gaseosa","Pequeña","comida",2000,200,"Normal",sucursalCine2)

    producto1S = Producto("Camisa","XL","souvenir",16000,200,"Normal",sucursalCine2)
    producto2S = Producto("Camisa","Bob Esponja","souvenir",27000,200,"Comedia",sucursalCine2)
    producto3S = Producto("Gorra","L","souvenir",11000,200,"Normal",sucursalCine2)
    producto4S = Producto("Llavero","Katana","souvenir",22000,200,"Acción",sucursalCine2)
    producto5S = Producto("Peluche","Pajaro loco","souvenir",29000,200,"Comedia",sucursalCine2)

    sucursalCine2.getServicios().add(servicioComida)
    sucursalCine2.getServicios().add(servicioSouvenirs)

    cliente1 = Cliente("Rusbel", 18, 13434, "CC");

    salaDeCine1_1 = SalaCine(1, "2D", sucursalCine1)
    salaDeCine1_2 = SalaCine(2, "3D", sucursalCine1)
    salaDeCine1_3 = SalaCine(3, "4D", sucursalCine1)
    salaDeCine1_4 = SalaCine(4, "2D", sucursalCine1)
    salaDeCine1_5 = SalaCine(5, "3D", sucursalCine1)
    salaDeCine1_6 = SalaCine(6, "4D", sucursalCine1)

    pelicula1_1 = Pelicula("Deadpool 3", 18000, "Comedia", timedelta( minutes=110 ), "+18", "2D", sucursalCine1)
    pelicula1_1.crearPeliculas()
    pelicula1_2 = Pelicula("Misión Imposible 4", 13000, "Acción", timedelta( minutes=155 ), "+16", "2D", sucursalCine1)
    pelicula1_2.crearPeliculas()
    pelicula1_3 = Pelicula("El conjuro 3", 18000, "Terror", timedelta( minutes=140 ), "+16", "2D", sucursalCine1)
    pelicula1_3.crearPeliculas()
    pelicula1_4 = Pelicula("Your name", 18000, "Romance", timedelta( minutes=110 ), "+8", "2D", sucursalCine1)
    pelicula1_4.crearPeliculas()
    pelicula1_5 = Pelicula("Furiosa: A Mad Max Saga", 17000, "Ciencia ficción", timedelta( minutes=148 ), "+18", "2D", sucursalCine1)
    pelicula1_5.crearPeliculas()
    pelicula1_6 = Pelicula("Spy x Familiy Código: Blanco", 19000, "Infantil", timedelta( minutes=90 ), "+5", "2D", sucursalCine1)
    pelicula1_6.crearPeliculas()

    salaDeCine2_1 = SalaCine(1, "2D", sucursalCine2)
    salaDeCine2_2 = SalaCine(2, "3D", sucursalCine2)
    salaDeCine2_3 = SalaCine(3, "4D", sucursalCine2)
    salaDeCine2_4 = SalaCine(4, "2D", sucursalCine2)
    salaDeCine2_5 = SalaCine(5, "3D", sucursalCine2)
    salaDeCine2_6 = SalaCine(6, "4D", sucursalCine2)

    pelicula2_1 = Pelicula("Jujutsu Kaisen Cero", 17000, "Acción", timedelta( minutes=90), "+12", "2D", sucursalCine2) 
    pelicula2_1.crearPeliculas()
    pelicula2_2 = Pelicula("The Strangers: Chapter 1", 20000, "Terror", timedelta( minutes=114 ), "+18", "2D", sucursalCine2)
    pelicula2_2.crearPeliculas()
    pelicula2_3 = Pelicula("El pájaro loco", 15000, "Infantil", timedelta( minutes=120 ), "+5", "2D", sucursalCine2)
    pelicula2_3.crearPeliculas()
    pelicula2_4 = Pelicula("One Life", 19000, "Historia", timedelta( minutes=110 ), "+8", "2D", sucursalCine2)
    pelicula2_4.crearPeliculas()
    pelicula2_5 = Pelicula("IP Man", 16000, "Acción", timedelta( minutes=132 ), "+16", "2D", sucursalCine2)
    pelicula2_5.crearPeliculas()
    pelicula2_6 = Pelicula("Bad Boys: Hasta la muerte", 17000, "Comedia", timedelta( minutes=109 ), "+18", "2D", sucursalCine2)
    pelicula2_6.crearPeliculas()

    salaDeCine3_1 = SalaCine(1, "2D", sucursalCine3)
    salaDeCine3_2 = SalaCine(2, "3D", sucursalCine3)
    salaDeCine3_3 = SalaCine(3, "4D", sucursalCine3)
    salaDeCine3_4 = SalaCine(4, "2D", sucursalCine3)
    salaDeCine3_5 = SalaCine(5, "3D", sucursalCine3)
    salaDeCine3_6 = SalaCine(6, "4D", sucursalCine3)

    pelicula3_1 = Pelicula("El Paseo 9", 15000, "Comedia", timedelta( minutes=60 ), "+12", "2D", sucursalCine3) 
    pelicula3_1.crearPeliculas()
    pelicula3_2 = Pelicula("Scream 8", 18000, "Terror", timedelta( minutes=180 ), "+16", "2D", sucursalCine3)
    pelicula3_2.crearPeliculas()
    pelicula3_3 = Pelicula("Oppenheimer", 15000, "Historia", timedelta( minutes=120 ), "+18", "2D", sucursalCine3)
    pelicula3_3.crearPeliculas()
    pelicula3_4 = Pelicula("Jhon Wick 4", 17000, "Acción", timedelta( minutes=180 ), "+18", "2D", sucursalCine3)
    pelicula3_4.crearPeliculas()
    pelicula3_5 = Pelicula("Intensamente 2", 15000, "Infantil", timedelta( minutes=105 ), "+5", "2D", sucursalCine3)
    pelicula3_5.crearPeliculas()
    pelicula3_6 = Pelicula("BNHA temporada 7 movie", 12000, "Acción", timedelta( minutes=60 ), "+12", "2D", sucursalCine3)
    pelicula3_6.crearPeliculas()
    


    SucursalCine.logicaInicioSIstemaReservarTicket()





    
    
