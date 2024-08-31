from asiento import Asiento
from sucursalCine import SucursalCine

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
        asientos = []

        for i in range(0, 8):
            asientos.append([])
            for j in range(0, 8):
                asientos[i].append(Asiento(i, j))

        return asientos
    
    #def mostrarAsientos

    def cambiarDisponibilidadAsientoAOcupado(self, numeroAsiento):

        for filaAsiento in self._asientos:
            cambioRealizado = False
            for asiento in filaAsiento:
                if asiento.getNumeroAsiento() == numeroAsiento:
                    asiento.setDisponibilidad(False)
                    cambioRealizado = True
                    break
            
            if cambioRealizado : break
    
    def _actualizarDisponibilidadAOcupado(self, fila, columna):
        self._asientos[fila][columna].setDisponibilidad(False)

    def _cambiarDisponibilidadAsientoALibre(self, fila, columna):
        if not self._asientos[fila][columna].isDisponibilidad():
            self._asientos[fila][columna].setDisponibilidad(True)

    def filtrarSalasDeCine(self, sucursalCine):
        salasConPeliculasEnPresentacion = []

        for salaDeCine in sucursalCine.getSalasDeCine():
            #Implementar try catch para el caso en el que una salaDeCine no tenga películaEnPresentacion try catch AttributeError
            if salaDeCine._horarioPeliculaEnPresentacion + salaDeCine._peliculaEnPresentacion.getDuracion() > SucursalCine.getFechaActual():
                salasConPeliculasEnPresentacion.append(salaDeCine)

        return salasConPeliculasEnPresentacion

    #def mostrarSalaCine

    def verificarTicket(self, cliente):

        validacionIngresoASala = False
        ticketVerificado = None

        for ticket in cliente.getTickets():

            validacionIngresoASala = ( ticket.getSalaCine() is self ) and ( ticket.getPelicula() is self._peliculaEnPresentacion ) and ( self._horarioPeliculaEnPresentacion + self._peliculaEnPresentacion.getDuracion() > SucursalCine.getFechaActual )
            
            if validacionIngresoASala : 

                if ticket.getPelicula() not in cliente.getHistorialDePeliculas():
                    cliente.getPeliculasDisponiblesParaCalificar()

                cliente.getHistorialDePeliculas().append(ticket.getPelicula())

                ticketVerificado = ticket

                break
        
        if ticketVerificado is not None : cliente.getTickets.remove(ticketVerificado)

        return validacionIngresoASala
            

    def actualizarPeliculaEnPresentacion(self):
        
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
                    
                    if horario > horarioMasCercanoAlActual and horario <= SucursalCine.getFechaActual():
                        horarioMasCercanoAlActual = horario
                
                if horarioMasCercanoAlActual is None: continue

                #Añadir lógica try catch AttrributeError a este bloque (Puede no ser necesario)
                if horarioMasCercanoAlActual <= SucursalCine.getFechaActual() and primeraComparacionPeliculaEnPresentacion:
                    horarioPeliculaEnPresentacion = horarioMasCercanoAlActual
                    peliculaEnPresentacion = pelicula
                    primeraComparacionPeliculaEnPresentacion = False

                elif horarioMasCercanoAlActual <= SucursalCine.getFechaActual() and horarioMasCercanoAlActual > horarioPeliculaEnPresentacion:
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
        return self._asientos[fila - 1][columna - 1].isDisponibilidad()
    
    def isDisponibilidadAlgunAsientoReserva(self):
        for filaAsientos in self._asientos:
            for asiento in filaAsientos:
                if asiento.isDisponibilidad(): return True
        
        return False
    
    #def mostrarAsientosParaPantalla

    #def mostrarPantallaSalaCine

    def tieneHorariosPresentacionHoy(self):

        for pelicula in self._sucursalUbicacion.getCartelera():

            if pelicula.getSalaCinePresentacion() is self:

                for horario in pelicula.filtrarHorariosPeliculaParaSalaCine():

                    if horario + pelicula.getDuracion() > SucursalCine.getFechaActual:
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