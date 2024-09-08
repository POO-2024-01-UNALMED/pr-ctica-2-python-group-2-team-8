from asiento import Asiento

class SalaCine:

#Attributes
################################################

    _cantidadSalasDeCineCreadas = 0

    def __init__(self, numeroDeSala, tipoDeSala, sucursalUbicacion):
        self._numeroSala = numeroDeSala
        self._tipoSala = tipoDeSala
        self._sucursalUbicacion = sucursalUbicacion
        self._asientos = self._crearAsientosSalaDeCine()

        self._horarioPeliculaEnPresentacion = None
        self._peliculaEnPresentacion = None

        SalaCine._cantidadSalasDeCineCreadas += 1
        self._salaCineId = SalaCine._cantidadSalasDeCineCreadas

#Methods
################################################

    def _crearAsientosSalaDeCine(self):

        """
        :Description: Este método se encarga de generar asientos para la sala de cine, facilitando el proceso de crear una sala de cine.
	    
        :return Asiento[][]:  Este método retorna una matriz de asientos.
        """

        asientos = []

        for i in range(0, 8):
            asientos.append([])
            for j in range(0, 8):
                asientos[i].append(Asiento(i, j))

        return asientos
    
    #def mostrarAsientos

    def cambiarDisponibilidadAsientoAOcupado(self, numeroAsiento):

        """
        :Description: Este método se encarga de modificar la disponiblidad de un asiento dado número de asiento, si su disponibilidad 
        es verdadera la cambia a falsa, se usa para separar un asiento luego de ser reservado exitosamente.
	    
        :param numeroAsiento: Este método recibe como parámetro el numero del asiento seleccionado por el cliente
	    (De tipo String) durante el proceso de reserva de una sala de cine actual.
        """

        for filaAsiento in self._asientos:
            cambioRealizado = False
            for asiento in filaAsiento:
                if asiento.getNumeroAsiento() == numeroAsiento:
                    asiento.setDisponibilidad(False)
                    cambioRealizado = True
                    break
            
            if cambioRealizado : break
    
    def _actualizarDisponibilidadAOcupado(self, fila, columna):

        """
        :Description: Este método se encarga de modificar la disponiblidad de un asiento dada su posición,
	    si su disponibilidad es verdadera la cambia a falsa, se usa para cambiar la disponibilidad de un asiento
	    la actualizar la sala con base en la información de la sala virtual (En el método actualizarPeliculaEnPresentacion()).
	    
        :param fila: Índice de la fila del asiento que queremos modificar (De tipo int).
	    :param columna: Índice de la columna del asiento que queremos modificar (De tipo int).
        """
        
        self._asientos[fila][columna].setDisponibilidad(False)

    def _cambiarDisponibilidadAsientoALibre(self, fila, columna):

        """
        :Description: Este método se encarga de modificar la disponiblidad de un asiento dada su posición, 
        si su disponibilidad es false la cambia a true, es especialmente útil para preparar la sala de cine
	    para presentar una nueva película (En el método actualizarPeliculaEnPresentacion()).
	    
        :param fila: Índice de la fila del asiento que queremos modificar (De tipo int).
	    :param columna: Índice de la columna del asiento que queremos modificar(De tipo int).
        """

        if not self._asientos[fila][columna].isDisponibilidad():
            self._asientos[fila][columna].setDisponibilidad(True)

    def filtrarSalasDeCine(self, sucursalCine):

        """
        :Description: Este método se encarga de filtrar las salas de cine según si su película aún se encuentra en presentación,
	    para esto verifica que el horario de la película en presentación más su duración no sea menor a la hora actual.
	    
        :param sucursalCine: Este método recibe como parámetro la sede (De tipo SucursalCine) en donde se realiza la busqueda 
        desde sus salas de cine.

	    :return list(SalaCine): Este método retorna las salas de cine, ( De tipo list(SalaCine) ), que aún tienen su película 
        en presentación, con el fin de ser las únicas que serán mostradas en pantalla durante el proceso de ingreso a salas de cines. 
        """

        salasConPeliculasEnPresentacion = []

        for salaDeCine in sucursalCine.getSalasDeCine():
            try:
                if salaDeCine._horarioPeliculaEnPresentacion + salaDeCine._peliculaEnPresentacion.getDuracion() > self._sucursalUbicacion.getFechaActual():
                    salasConPeliculasEnPresentacion.append(salaDeCine)
            except AttributeError:
                pass

        return salasConPeliculasEnPresentacion

    #def mostrarSalaCine

    def verificarTicket(self, cliente):

        """
        :Description: Este método se encarga de verificar si una persona tiene al menos un ticket registrado en su array que 
        cumpla los siguientes criterios para ingresar a la sala de cine:
	    <ol>
	    <li> La película asociada al ticket coincide con la pelicula en presentacion de la sala de cine.</li>
	    <li> La fecha actual es anterior a la fecha en que finaliza la película.</li>
	    <li> La sala de cine asociada al ticket es la misma que la sala de cine que ejecuta este método.</li>
	    </ol>
	    :param cliente : Este método solicita al cliente (De tipo cliente) que va a ingresar a la SalaDeCine.
	    :return <b>boolean</b> : Este método se encarga de retornar un boolean que será el resultado del proceso de verificación 
        de entrada a la sala de Cine.
        """

        validacionIngresoASala = False
        ticketVerificado = None

        for ticket in cliente.getTickets():

            validacionIngresoASala = ( ticket.getSalaCine() is self ) and ( ticket.getPelicula() is self._peliculaEnPresentacion ) and ( self._horarioPeliculaEnPresentacion + self._peliculaEnPresentacion.getDuracion() > self._sucursalUbicacion.getFechaActual )
            
            if validacionIngresoASala : 

                if ticket.getPelicula() not in cliente.getHistorialDePeliculas():
                    cliente.getPeliculasDisponiblesParaCalificar()

                cliente.getHistorialDePeliculas().append(ticket.getPelicula())

                ticketVerificado = ticket

                break
        
        if ticketVerificado is not None : cliente.getTickets.remove(ticketVerificado)

        return validacionIngresoASala
            

    def actualizarPeliculaEnPresentacion(self):

        """
        :Description: Este método se encarga actualizar la película en presentación, según los siguientes criterios: 
	    <ol>
	    <li> La sala de cine en que se presentará alguna de las películas en cartelera de la sucursal de cine 
	    coincide con alguna de las salas de cine de esta. </li>
	    <li> Revisamos si esa película tiene algún horario cercano o igual a la fecha actual durante el cuál estará o 
        esta siendo presentada.</li>
	    </ol>
	    una vez hecho esto y cumpla con los dos criterios anteriores, limpiamos los asientos de la sala de cine, cambiando su 
        disponibilidad a libre, y por último actualizamos la información de la disponibilidad de los asientos, tomando como 
        referencia la información de los asientos virtuales que coincidieron en fecha y hora de la película en presentación,
        además, modificamos el atributo horario pelicula en presentación y pelicula en presentación de la sala de cine.
        """
        
        peliculaEnPresentacion = None
        horarioPeliculaEnPresentacion = None

        primeraComparacionPeliculaEnPresentacion = True

        for pelicula in self._sucursalUbicacion.getCartelera():

            horarioMasCercanoAlActual = None

            if pelicula.getSalaDeCine() is self:

                horariosDiaDeHoy = pelicula.filtrarHorariosPeliculaParaSalaCine()

                if len(horariosDiaDeHoy) == 0: continue

                for horario in horariosDiaDeHoy:
                    if horariosDiaDeHoy.indexOf(horario) == 0:
                        horarioMasCercanoAlActual = horario
                    
                    if horario > horarioMasCercanoAlActual and horario <= self._sucursalUbicacion.getFechaActual():
                        horarioMasCercanoAlActual = horario
                
                if horarioMasCercanoAlActual is None: continue

                #Añadir lógica try catch AttrributeError a este bloque (Puede no ser necesario)
                if horarioMasCercanoAlActual <= self._sucursalUbicacion.getFechaActual() and primeraComparacionPeliculaEnPresentacion:
                    horarioPeliculaEnPresentacion = horarioMasCercanoAlActual
                    peliculaEnPresentacion = pelicula
                    primeraComparacionPeliculaEnPresentacion = False

                elif horarioMasCercanoAlActual <= self._sucursalUbicacion.getFechaActual() and horarioMasCercanoAlActual > horarioPeliculaEnPresentacion:
                    horarioPeliculaEnPresentacion = horarioMasCercanoAlActual
                    peliculaEnPresentacion = pelicula

        if peliculaEnPresentacion is not None:
            self._peliculaEnPresentacion = peliculaEnPresentacion
            self._horarioPeliculaEnPresentacion = horarioPeliculaEnPresentacion

            for i in range (0, len(self._asientos)):
                for j in range (0, len(self._asientos[i])):
                    
                    self._cambiarDisponibilidadAsientoALibre(i, j)

                    if (not self._peliculaEnPresentacion.isDisponibilidadAsientoSalaVirtual(horarioPeliculaEnPresentacion, i+1, j+1)):
                        self._actualizarDisponibilidadAOcupado(i, j)

    def isDisponibilidadAsientoReserva(self, fila, columna):

        """
        :Description: Este método se encarga de retornar la disponibilidad de un asiento dada su fila y su columna.
	    
        :param fila: Este método recibe la fila del asiento a consultar (De tipo int).
	    :param columna: Este método recibe la columna del asiento a consultar (De tipo int).
	    
        :return boolean: Este método retorna la disponibilidad del asiento consultado.
        """
        
        return self._asientos[fila - 1][columna - 1].isDisponibilidad()
    
    def isDisponibilidadAlgunAsientoReserva(self):

        """
        :Description: Este método se encarga de evaluar si la sala de cine tiene algún asiento disponible.
	    
        :return boolean: Este método retorna un boolean que representa si tiene asientos disponibles.
        """

        for filaAsientos in self._asientos:
            for asiento in filaAsientos:
                if asiento.isDisponibilidad(): return True
        
        return False
    
    #def mostrarAsientosParaPantalla

    #def mostrarPantallaSalaCine

    def tieneHorariosPresentacionHoy(self):

        """
        :Description: Este método se encarga de revisar si una sala de cine tendrá durante ese día más películas en presentación.
	    :return boolean: retorna el estado de la validación.
        """

        for pelicula in self._sucursalUbicacion.getCartelera():

            if pelicula.getSalaCinePresentacion() is self:

                for horario in pelicula.filtrarHorariosPeliculaParaSalaCine():

                    if horario + pelicula.getDuracion() > self._sucursalUbicacion.getFechaActual():
                        return True
                    
        return False


#Getters and Setters
################################################

    def getSalaCineId(self):
        return self._salaCineId
    
    def setSalaCineId(self, salaCineId):
        self._salaCineId = salaCineId

    @classmethod    
    def getCantidadSalasDeCineCreadas(cls):
        return SalaCine._cantidadSalasDeCineCreadas
    
    @classmethod
    def setCantidadSalasDeCineCreadas(cls, cantidadSalasDeCineCreadas):
        SalaCine._cantidadSalasDeCineCreadas = cantidadSalasDeCineCreadas

    def getNumeroSala(self):
        return self._numeroSala
    
    def setNumeroSala(self, numeroSala):
        self._numeroSala = numeroSala
    
    def  getTipoSala(self):
        return self._tipoSala
    
    def setTipoSala(self, tipoSala):
        self._tipoSala = tipoSala

    def getAsientos(self):
        return self._asientos
    
    def setAsientos(self, asientos):
        self._asientos = asientos

    def getHorarioPeliculaEnPresentacion(self):
        return self._horarioPeliculaEnPresentacion

    def setHorarioPeliculaEnPresentacion(self, horarioPeliculaEnPresentacion):
        self._horarioPeliculaEnPresentacion = horarioPeliculaEnPresentacion

    def getPeliculaEnPresentacion(self):
        return self._peliculaEnPresentacion
    
    def setPeliculaEnPresentacion(self, peliculaEnPresentacion):
        self._peliculaEnPresentacion = peliculaEnPresentacion

    def getSucursalUbicacion(self):
        return self._sucursalUbicacion
    
    def setSucursalUbicacion(self, sucursalUbicacion):
        self._sucursalUbicacion = sucursalUbicacion