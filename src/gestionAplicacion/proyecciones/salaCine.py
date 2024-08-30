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
        if self._asientos[fila][columna].isDisponibilidad():
            self._asientos[fila][columna].setDisponibilidad(True)

    #def filtrarSalasDeCine

    #def mostrarSalaCine

    #def verificarTicket

    #def actualaizarPeliculasEnPresentacion

    def isDisponibilidadAsientoReserva(self, fila, columna):
        return self._asientos[fila - 1][columna - 1].isDisponibilidad()
    
    #def mostrarAsientosParaPantalla

    #def mostrarPantallaSalaCine

    #def tieneHorariosPresentacionHoy

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