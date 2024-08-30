class Pelicula:

#Attributes
################################################

    _cantidadPeliculasGeneradas = 0

    def __init___(self, nombre, precio, genero, duracion, clasificacion, tipoDeFormato, sucursalCine):
        self._nombre = nombre
        self._precio = precio
        self._genero = genero
        self._duracion = duracion
        self._clasificacion = clasificacion
        self._tipoDeFormato = tipoDeFormato

        Pelicula._cantidadPeliculasGeneradas += 1
        self._idPelicula = Pelicula._cantidadPeliculasGeneradas
        self._horariosPresentacion = None
        self._AsientosSalasVirtuales = None
        self._salaCinePresentacion = None
        
        #self._valoracion = 4.0
        #self._totalEncuestasRealizadas = 25
        #self._sucursalCartelera = sucursalCine
        #self._strikeCambio = True

        #sucursalCine.getCartelera().add(self)
        #this.crearPelicula(sucursalCine)

#Methods
################################################

    def crearSalaVirtual(self, fecha):
        pass
    
    @classmethod
    def filtrarCarteleraPorCliente(cls, cliente, sucursalCine):
        pass

    @classmethod
    def filtarCarteleraPorGenero(cls, filtroPeliculasPorCliente, genero):
        pass

    #def showNombrePeliculas(cls, filtroNombrePeliculas, clienteProceso, nombrePeliculasRecomendadas):

    @classmethod
    def filtrarCarteleraPorNombre(cls, nombrePelicula, peliculasDisponiblesCliente):
        pass

    #def showTiposFormatoPeliculaSeleccionada(cls, peliculasFiltradasPorNombre):

    #def mostrarAsientosSalaVirtual(self, fecha):

    def modificarSalaVIrtual(self, fecha, fila, columna):
        pass

    def isDisponibilidadAsientoSalaVirtual(self, fecha, fila, columna):
        pass

    def isDisponibilidadAlgunAsientoSalaVirtual(self, horario):
        pass

    def filtrarHorariosPelicula(self):
        pass

    def filtrarHorariosPeliculaParaSalaCine(self):
        pass

    #def mostrarHorarioPelicula(self, horarioPelicula):

    def isPeliculaEnPresentacion(self, sucursalCine):
        pass

    def whereIsPeliculaEnPresentacion(self, sucursalCine):
        pass

    def _crearPelicula(self, sucursalCine):
        pass

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
    
    def setHorarioPresentacion(self, horariosPresentacion):
        self._horariosPresentacion = horariosPresentacion
    
    def getAsientosSalasVirtuales(self):
        return self._AsientosSalasVirtuales
    
    def setAsientosSalasVirtuales(self, asientosSalasVirtuales):
        self._AsientosSalasVirtuales = asientosSalasVirtuales
    
    def getSalaCinePresentacion(self):
        return self._salaCinePresentacion
    
    def setSalaCinePresentacion(self, salaCinePresentacion):
        self._salaCinePresentacion = salaCinePresentacion
    