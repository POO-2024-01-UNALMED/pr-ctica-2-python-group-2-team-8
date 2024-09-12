import random
from datetime import datetime

class Pelicula:

#Attributes
################################################

    _cantidadPeliculasGeneradas = 0

    def __init__(self, nombre, precio, genero, duracion, clasificacion, tipoDeFormato, sucursalCine):
        self._nombre = nombre
        self._precio = precio
        self._genero = genero
        self._duracion = duracion
        self._clasificacion = clasificacion
        self._tipoDeFormato = tipoDeFormato

        Pelicula._cantidadPeliculasGeneradas += 1
        self._idPelicula = Pelicula._cantidadPeliculasGeneradas
        self._horariosPresentacion = []
        self._asientosSalasVirtuales = []
        self._salaCinePresentacion = None
        sucursalCine.getCartelera().append(self)
        
        self._valoracion = 4.0
        self._totalEncuestasRealizadas = 25
        self._sucursalCartelera = sucursalCine
        self._strikeCambio = True

        

#Methods
################################################

    def crearSalaVirtual(self, horario):

        """
        :Description: Este método se encarga de crear una matriz que representa la sala virtual, posteriormente se añade al array 
	    de asientos virtuales de la película y se añade el horario al array de horarios.

	    :param horario: Este método recibe una fecha (De tipo datetime) para crear la salaDeCineVirtual.
        """

        asientosSalaVirtual = []

        for i in range(0, 8):
            asientosSalaVirtual.append([])
            for j in range (0, 8):
                asientosSalaVirtual[i].append(0)
        
        self._horariosPresentacion.append(horario)
        self._asientosSalasVirtuales.append(asientosSalaVirtual)
    
    @classmethod
    def filtrarCarteleraPorCliente(cls, cliente, sucursalCine):

        """
        :Description : Este método se encarga de filtar las películas en cartelera con los siguientes criterios:
	    <ol>  
	    <li>Su categoría es menor o igual a la edad del cliente.</li>
	    <li>La película tiene al menos 1 horario en el cuál será presentada o se encuentra en presentación y no supera el
	    límite de tiempo para comprar un ticket de una película en presentación (15 minutos).</li>  
	    </ol>
	    Todo esto con el fin de mostrar en pantalla, posteriormente, el array de las películas que cumplan estos criterios.

	    :param clienteProceso: Este método recibe como parámetro un cliente (De tipo cliente), que realizará el proceso de reserva de ticket.
	    
        :param sucursalCine: Este método recibe como parámetro la sede (De tipo SucursalCine) para acceder a su cartelera.
	    
        :return list(String): Retorna una lista con las peliculas filtradas por el criterio anterior.
        """

        carteleraPersonalizadaCliente = []

        for pelicula in sucursalCine.getCartelera():
            if len(pelicula.filtrarHorarios()) > 0 or pelicula.isPeliculaEnPresentacion(sucursalCine):
                if int(pelicula._clasificacion) <= cliente.getEdad():
                    carteleraPersonalizadaCliente.append(pelicula)
        
        return carteleraPersonalizadaCliente
    
    @classmethod
    def filtrarCarteleraPorNombre(cls, filtroPeliculasPorCliente):

        """
        Description : Este método genera una lista filtrada según el nombre de las películas disponibles sin repetición.
	    
        :param filtroPeliculasPorCliente: Este método recibe como parámetro las peliculas ( De tipo list(Pelicula) ) 
	    resultantes de realizar el filtro por cliente (Edad y disponibilidad horaria).
	    
        :return list(String): Retorna una lista de nombres de las películas distintos entre sí.
        """

        filtroNombrePeliculas = []

        for pelicula in filtroPeliculasPorCliente:
            if pelicula._nombre not in filtroNombrePeliculas:
                filtroNombrePeliculas.append(pelicula._nombre)

        return filtroNombrePeliculas

    @classmethod
    def filtarCarteleraPorGenero(cls, filtroPeliculasPorCliente, genero):

        """
	    :Description: Este método genera una lista filtrada según el nombre de las películas que coinciden con 
        determinado género, sin repetición.

	    :param filtroPeliculasPorCliente: Este método recibe como parámetro las peliculas ( De tipo list(Pelicula) ) 
        resultantes de realizar el filtro por cliente (Edad y disponibilidad horaria). 
	    
        :param genero : Este método recibe como parámetro el género (De tipo String) más visualizado por el cliente.

	    :return list(String): Retorna una lista de nombres de las películas distintos entre sí, cuyo género es igual.
	
        """
        
        filtroNombrePeliculasPorGenero = []

        for pelicula in filtroPeliculasPorCliente:
            if pelicula._genero is genero:
                if pelicula._nombre not in filtroNombrePeliculasPorGenero:
                    filtroNombrePeliculasPorGenero.append(pelicula._nombre)
        
        return filtroNombrePeliculasPorGenero

    #def showNombrePeliculas(cls, filtroNombrePeliculas, clienteProceso, nombrePeliculasRecomendadas):

    @classmethod
    def obtenerPeliculasPorNombre(cls, nombrePelicula, peliculasDisponiblesCliente):

        """
        :Description: Este método se encarga de retornar las películas cuyo nombre coincide con el nombre de la película 
        seleccionada por el cliente.
	    
        :param nombrePelicula: Este método recibe como parámetro el nombre de la película ( De tipo String ) con el cuál 
        se realizará el filtrado.
	    
        :param peliculasDisponiblesCliente: Este método recibe como parámetro una lista ( De tipo list(Pelicula) ) que contiene 
	    las películas previamente filtradas según los datos del cliente y su disponibilidad horaria.
	    
        :return list(Pelicula): Este método retorna un ArrayList de las películas cuyo nombre coinciden con el nombre seleccionado 
	    por el cliente.
        """
        
        filtroPeliculasMismoNombre = []

        for pelicula in peliculasDisponiblesCliente:
            if pelicula._nombre == nombrePelicula:
                filtroPeliculasMismoNombre.append(pelicula)
        
        return filtroPeliculasMismoNombre

    #def showTiposFormatoPeliculaSeleccionada(cls, peliculasFiltradasPorNombre):

    #def mostrarAsientosSalaVirtual(self, fecha):

    def modificarSalaVIrtual(self, horario, fila, columna):

        """
        :Description: Este método se encarga de cambiar la disponibilidad del asiento, seleccionado por el cliente, de la sala 
        virtual.
	    
        :param horario: Recibe la fecha seleccionada por el cliente para obtener su índice de sala virtual y así acceder a sus 
        asientos ( De tipo datetime ).
	    
        :param fila: Recibe el número de la fila seleccionada por el cliente (De tipo int).
	    
        :param columna: Recibe el número de la columna seleccionada por el cliente (De tipo int).
        """

        self._asientosSalasVirtuales[self._horariosPresentacion.index(horario)][fila - 1][columna - 1] = 1

    def isDisponibilidadAsientoSalaVirtual(self, horario, fila, columna):

        """
        :Description : Este método se encarga revisar la desponibilidad de un asiento determinado de la sala de cine virtual.
	    
        :param horario: Recibe la fecha seleccionada por el cliente para obtener su índice de sala virtual y así acceder a sus asientos ( De tipo datetime ).
	    
        :param fila: Recibe el número de la fila seleccionada por el cliente (De tipo int).
	    
        :param columna: Recibe el número de la columna seleccionada por el cliente (De tipo int).
	    
        :return boolean: Este método retorna un boolean que representa la disponibilidad del asiento selccionado por el cliente.
        """
        
        return self._asientosSalasVirtuales[self._horariosPresentacion.index(horario)][fila - 1][columna - 1] == 0

    def isDisponibilidadAlgunAsientoSalaVirtual(self, horario):

        """
        :Description: Este método se encarga de evaluar si la película dado un horario tiene algún asiento disponible.
	    
        :param horario: Este método recibe como parámetro un horario (De tipo datetime) del cuál accederá a su matriz de asientos.
	    
        :return boolean: Este método retorna un boolean que representa si tiene asientos disponibles en ese horario.
        """

        for filaAsientos in self._asientosSalasVirtuales[self._horariosPresentacion.index(horario)]:
            for asiento in filaAsientos:
                if asiento == 0: return True
        
        return False

    def filtrarHorariosPelicula(self):

        """
        :Description: Este método se encarga de filtrar los horarios de la película más próximos que no han sido presentados 
        aún y tienen asientos disponibles.

	    :return list(datetime): Este método se encarga de retornar los primeros 7 horarios más cercanos a la fecha actual 
        que cumplen los criterios de filtrado.
        """
        
        filtroHorariosProxPresentaciones = []

        for horario in self._horariosPresentacion:
            if horario > self._sucursalCartelera.getFechaActual():
                if self.isDisponibilidadAlgunAsientoSalaVirtual(horario):
                    filtroHorariosProxPresentaciones.append(horario)
            
            if len(filtroHorariosProxPresentaciones) == 7 : break
        
        return filtroHorariosProxPresentaciones

    def filtrarHorariosPeliculaParaSalaCine(self):

        """
        :Description: Este método se encarga de filtrar los horarios de la película ejecutando el método que están disponibles 
        durante el día actual, retornando la lista de horarios encontrados, con el fin de optimizar la actualización de las
        salas de cine.

	    :return list(datetime): Este método retorna los horarios de la película que serán o fueron presentados el día de hoy.
        """
        
        filtrarHorariosPresentacionesHoy = []

        for horario in self._horariosPresentacion:
            if horario.date() == self._sucursalCartelera.getFechaActual().date():
                filtrarHorariosPresentacionesHoy.append(horario)
            elif horario.date() > self._sucursalCartelera.getFechaActual().date():
                break
        
        return filtrarHorariosPresentacionesHoy

    #def mostrarHorarioPelicula(self, horarioPelicula):

    def isPeliculaEnPresentacion(self, sucursalCine):

        """
        :Description: Este método se encarga de buscar si la pelicula que ejecuta este método se encuentra en presentación, la 
	    utilidad de este método radica en que retornará verdadero en caso de:
	    <ol> 
	    <li> Encontrar la sala de cine donde está siendo presentada.</li>
	    <li> No lleva más de 15 minutos en presentación.</li>
	    <li> Tenga algún asiento disponible.</li>
	    </ol>
	    Respecto a este retorno, se ejecutará un menú determinado en el proceso de la funcionalidad 1.
	    
        :param sucursalCine: Este método recibe como parámetro la sede (De tipo SucursalCine) en donde se realiza este proceso, para
	    obtener sus salas de cine.
	    
        :return boolean: Este método retorna un boolean, que representa si la película cumple, o no, con los criterios.
        """

        for salaDeCine in sucursalCine.getSalasDeCine():
            try:
                if salaDeCine.getPeliculaEnPresntacion() is self and salaDeCine.getHorarioPeliculaEnPresentacion() + self._sucursalCartelera.getTiempoLimiteReservaTicket() < self._sucursalCartelera.getFechaActual():
                    if salaDeCine.isDisponibilidadAlgunAsientoReserva(): return True
            except AttributeError:
                pass
        
        return False

    def whereIsPeliculaEnPresentacion(self, sucursalCine):

        """
        :Description: Este método se encarga de retornar la sala de cine donde película que ejecuta este método se encuentra en 
        presentación.
	    
        :param sucursalCine: Este método recibe como parámetro la sede (De tipo SucursalCine) en donde se realiza este proceso
	    para obtener sus salas de cine.
	    
        :return SalaCine: Este método retorna la sala de cine donde está siendo proyectada la película.
        """
        
        for salaDeCine in sucursalCine.getSalasDeCine():
            if salaDeCine.getPeliculaEnPresentacion() is self:
                return salaDeCine

    def crearPeliculas(self):

        """
        :Description : Este método se encarga de automatizar la creación de películas en varios formatos con distinto precio, 
        para hacer esto se evalua si el género de la película que ejecuta este método se encuentra en los géneros que tienen 
        permitido el 3D y 4D o únicamente 3D, en caso de ser así, crea una película nueva con toda su misma información, 
        a excepción del tipo de formato y precio.
	    
        :param sucursalCine: Este método recibe como parámetro la sede (De tipo SucursalCine) en la que será presentada la película.
        """
        
        generos4D = ["Aventura", "Acción", "Ciencia ficción", "Terror", "Infantil"]
        generos3D = ["Historia", "Comedia"]

        if self._genero in generos4D:
            Pelicula(self._nombre, self._precio + 15000, self._genero, self._duracion, self._clasificacion, "3D", self._sucursalCartelera)
            Pelicula(self._nombre, self._precio + 50000, self._genero, self._duracion, self._clasificacion, "4D", self._sucursalCartelera)
        elif self._genero in generos3D:
            Pelicula(self._nombre, self._precio + 15000, self._genero, self._duracion, self._clasificacion, "3D", self._sucursalCartelera)


#Description: Este método se encarga de filtrar los horarios de la película ejecutando el método
#que están disponibles durante el día actual, retornando la lista de horarios encontrados, con 
#el fin de efectuar la actualización y solicitud de actualización de las salas de cine.


    def seleccionar_horario_mas_lejano(self,horario: datetime):
        horarios_pelicula = None
        is_asientos_disponibles = False

        horarios = self.filtrar_horarios_pelicula()
        if len(horarios) > 0:
            for horario in horarios:
                is_asientos_disponibles = self.is_disponibilidad_asiento_sala_virtual(horario)
                if is_asientos_disponibles:
                    horarios_pelicula = horario

        return horarios_pelicula
        

#Description:Este metodo se encarga de seleccionar un asiento aleatoriamente en la sala de cine, esto se hace
#con el fin de dar un combo o un regalo al cliente que haya calificado un producto o una pelicula y en modo de
#obsequio le ofrecemos este bono,el metodo retorna un numAsiento de forma aleatoria y ese asiento es al que se 
#le va a dar al cliente.
	 
    def seleccionar_asiento_aleatorio(self, horario_proceso: datetime) -> str:
        validacion = True
        num_asiento = None
        
        while validacion:
            fila = random.randint(1, 8)
            columna = random.randint(1, 8)
            validacion = not self.is_disponibilidad_asiento_sala_virtual(horario_proceso, fila, columna)
            num_asiento = f"{fila}-{columna}"
        
        return num_asiento

#Getters and Setters
################################################

    def getIdPelicula(self):
        return self._idPelicula
    
    def setIdPelicula(self, idPelicula):
        self._idPelicula = idPelicula
    
    @classmethod
    def getCantidadPeliculasGeneradas(cls):
        return Pelicula._cantidadPeliculasGeneradas
    
    @classmethod
    def setCantidadPeliculasGeneradas(cls, cantidadPeliculasGeneradas):
        Pelicula._cantidadPeliculasGeneradas = cantidadPeliculasGeneradas

    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre

    def getGenero(self):
        return self._genero
    
    def setGenero(self, genero):
        self._genero = genero

    def getDuracion(self):
        return self._duracion
    
    def setDuracion(self, duracion):
        self._duracion = duracion
    
    def getClasificacion(self):
        return self._clasificacion
    
    def setClasificacion(self, clasificacion):
        self._clasificacion = clasificacion
    
    def getTipoDeFormato(self):
        return self._tipoDeFormato
    
    def setTipoDeFormato(self, tipoDeFormato):
        self._tipoDeFormato = tipoDeFormato

    def getHorariosPresentacion(self):
        return self._horariosPresentacion
    
    def setHorariosPresentacion(self, horariosPresentacion):
        self._horariosPresentacion = horariosPresentacion
    
    def getAsientosSalasVirtuales(self):
        return self._asientosSalasVirtuales
    
    def setAsientosSalasVirtuales(self, asientosSalasVirtuales):
        self._asientosSalasVirtuales = asientosSalasVirtuales
    
    def getSalaCinePresentacion(self):
        return self._salaCinePresentacion
    
    def setSalaCinePresentacion(self, salaCinePresentacion):
        self._salaCinePresentacion = salaCinePresentacion