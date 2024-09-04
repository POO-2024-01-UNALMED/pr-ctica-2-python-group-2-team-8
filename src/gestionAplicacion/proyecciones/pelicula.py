from sucursalCine import SucursalCine
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
        self._horariosPresentacion = None
        self._asientosSalasVirtuales = None
        self._salaCinePresentacion = None
        sucursalCine.getCartelera().add(self)
        
        self._valoracion = 4.0
        self._totalEncuestasRealizadas = 25
        self._sucursalCartelera = sucursalCine
        self._strikeCambio = True

        

#Methods
################################################

    def crearSalaVirtual(self, horario):

        asientosSalaVirtual = []

        for i in range(0, 8):
            asientosSalaVirtual.append([])
            for j in range (0, 8):
                asientosSalaVirtual[i].append(0)
        
        self._horariosPresentacion.append(horario)
        self._asientosSalasVirtuales.append(asientosSalaVirtual)
    
    @classmethod
    def filtrarCarteleraPorCliente(cls, cliente, sucursalCine):

        carteleraPersonalizadaCliente = []

        for pelicula in sucursalCine.getCartelera():
            if len(pelicula.filtrarHorarios()) > 0 or pelicula.isPeliculaEnPresentacion(sucursalCine):
                if int(pelicula._clasificacion) <= cliente.getEdad():
                    carteleraPersonalizadaCliente.append(pelicula)
        
        return carteleraPersonalizadaCliente
    
    @classmethod
    def filtrarCarteleraPorNombre(cls, filtroPeliculasPorCliente):

        filtroNombrePeliculas = []

        for pelicula in filtroPeliculasPorCliente:
            if pelicula._nombre not in filtroNombrePeliculas:
                filtroNombrePeliculas.append(pelicula._nombre)

        return filtroNombrePeliculas

    @classmethod
    def filtarCarteleraPorGenero(cls, filtroPeliculasPorCliente, genero):
        
        filtroNombrePeliculasPorGenero = []

        for pelicula in filtroPeliculasPorCliente:
            if pelicula._genero is genero:
                if pelicula._nombre not in filtroNombrePeliculasPorGenero:
                    filtroNombrePeliculasPorGenero.append(pelicula._nombre)
        
        return filtroNombrePeliculasPorGenero

    #def showNombrePeliculas(cls, filtroNombrePeliculas, clienteProceso, nombrePeliculasRecomendadas):

    @classmethod
    def obtenerPeliculasPorNombre(cls, nombrePelicula, peliculasDisponiblesCliente):
        
        filtroPeliculasMismoNombre = []

        for pelicula in peliculasDisponiblesCliente:
            if pelicula._nombre == nombrePelicula:
                filtroPeliculasMismoNombre.append(pelicula)
        
        return filtroPeliculasMismoNombre

    #def showTiposFormatoPeliculaSeleccionada(cls, peliculasFiltradasPorNombre):

    #def mostrarAsientosSalaVirtual(self, fecha):

    def modificarSalaVIrtual(self, horario, fila, columna):
        self._asientosSalasVirtuales[self._horariosPresentacion.indexOf(horario)][fila - 1][columna - 1] = 1

    def isDisponibilidadAsientoSalaVirtual(self, horario, fila, columna):
        return self._asientosSalasVirtuales[self._horariosPresentacion.indexOf(horario)][fila - 1][columna - 1] == 0

    def isDisponibilidadAlgunAsientoSalaVirtual(self, horario):

        for filaAsientos in self._asientosSalasVirtuales[self._horariosPresentacion.indexOf(horario)]:
            for asiento in filaAsientos:
                if asiento == 0: return True
        
        return False

    def filtrarHorariosPelicula(self):
        
        filtroHorariosProxPresentaciones = []

        for horario in self._horariosPresentacion:
            if horario > SucursalCine.getFechaActual():
                if self.isDisponibilidadAlgunAsientoSalaVirtual(horario):
                    filtroHorariosProxPresentaciones.append(horario)
            
            if len(filtroHorariosProxPresentaciones) == 7 : break
        
        return filtroHorariosProxPresentaciones

    def filtrarHorariosPeliculaParaSalaCine(self):
        
        filtrarHorariosPresentacionesHoy = []

        for horario in self._horariosPresentacion:
            if horario.date() == SucursalCine.getFechaActual().date():
                filtrarHorariosPresentacionesHoy.append(horario)
        
        return filtrarHorariosPresentacionesHoy

    #def mostrarHorarioPelicula(self, horarioPelicula):

    def isPeliculaEnPresentacion(self, sucursalCine):
        #Implementar try catch AttributeError
        for salaDeCine in sucursalCine.getSalasDeCine():
            if salaDeCine.getPeliculaEnPresntacion() is self and salaDeCine.getHorarioPeliculaEnPresentacion() + SucursalCine.getTiempoLimiteReservaTicket() < SucursalCine.getFechaActual():
                if salaDeCine.isDisponibilidadAlgunAsientoReserva(): return True
        
        return False

    def whereIsPeliculaEnPresentacion(self, sucursalCine):
        
        for salaDeCine in sucursalCine.getSalasDeCine():
            if salaDeCine.getPeliculaEnPresentacion() is self:
                return salaDeCine

    def crearPeliculas(self):
        
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
        return self._genero
    
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
    