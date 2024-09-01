from datetime import datetime, time, timedelta

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

        self._salasDeCine = []
        self._cartelera = []
        self._cantidadTicketsCreados = 1
    
#Methods
################################################

    #def mostrarSucursalesCine(cls)

    @classmethod
    def actualizarPeliculasSalasDeCine(cls):
        for sede in SucursalCine._sucursalesCine:
            for salaDeCine in sede._salasDeCine:

                try:
                    if salaDeCine.getHorarioPeliculaEnPresentacion() + salaDeCine.getPeliculaEnPresentacion().getDuracion() <= SucursalCine._fechaActual:
                        salaDeCine.actualizarPeliculaEnPresentacion()
                except AttributeError:
                    salaDeCine.actualizarPeliculaEnPresntacion()
    
    @classmethod
    def _dropHorariosVencidos(cls):
        
        for sede in SucursalCine._sucursalesCine:

            for pelicula in sede._cartelera:

                horariosAEliminar = []

                for horario in pelicula.getHorariosPresentacion():

                    if horario.date() < SucursalCine._fechaActual:
                        horariosAEliminar.append(horario)
                
                for horario in horariosAEliminar:

                    pelicula.getAsientosSalasVirtuales().pop(pelicula.getHorariosPresentacion().indexOf(horario))
                    pelicula.getHorariosPresentacion().remove(horario)

    def _crearHorariosPeliculasPorSala(self):
        
        peliculasDeSalaDeCine = []

        LIMITE_CREACION_HORARIOS_PRESENTACION = (SucursalCine._fechaActual + timedelta(weeks = 1)).date()

        for salaDeCine in self._salasDeCine:

            horarioParaPresentar = SucursalCine._fechaActual.replace(minute = 0, second = 0, microsecond = 0)

            for pelicula in self._cartelera:

                if pelicula.getSalaDeCine() is salaDeCine:
                    peliculasDeSalaDeCine.append(pelicula)

            for i in range (0,20):

                if horarioParaPresentar.date() >= LIMITE_CREACION_HORARIOS_PRESENTACION:
                    break

                for pelicula in peliculasDeSalaDeCine:
                    
                    condicionCreacionEnJornadaLaboral = horarioParaPresentar.time() < SucursalCine._FIN_HORARIO_LABORAL and horarioParaPresentar.time() >= SucursalCine._INICIO_HORARIO_LABORAL
                    condicionCreacionDuranteJornadaLaboral = (horarioParaPresentar + pelicula._getDuracion()).time() <= SucursalCine._FIN_HORARIO_LABORAL and (horarioParaPresentar + pelicula.getDuracion()).date() == horarioParaPresentar.date()
                    
                    if  condicionCreacionEnJornadaLaboral and condicionCreacionDuranteJornadaLaboral:
                            pelicula.crearSalaVirtual(horarioParaPresentar)
                            horarioParaPresentar += pelicula.getDuracion() + SucursalCine._TIEMPO_LIMPIEZA_SALA_DE_CINE
                    else: 
                        if horarioParaPresentar.time() > SucursalCine._INICIO_HORARIO_LABORAL:
                            horarioParaPresentar += timedelta(days = 1)
                        
                        if horarioParaPresentar.date() >= LIMITE_CREACION_HORARIOS_PRESENTACION:
                            break
                    
                        horarioParaPresentar = horarioParaPresentar.replace(hour = SucursalCine._INICIO_HORARIO_LABORAL.hour, minute = SucursalCine._INICIO_HORARIO_LABORAL.minute)
                        pelicula.crearSalaVirtual(horarioParaPresentar)
                        horarioParaPresentar += pelicula.getDuracion() + SucursalCine._TIEMPO_LIMPIEZA_SALA_DE_CINE
        
            peliculasDeSalaDeCine.clear()

    def _distribuirPeliculasPorSala(self):
        
        formatos = ["2D", "3D", "4D"]

        grupoSalasPorFormato = []
        grupoPeliculasPorFormato = []

        cantidadMaxPeliculaPorSala = 0
        indiceSalaDeCine = 0
        contador = 0

        for formato in formatos:

            for salaDeCine in self._salasDeCine:
                if salaDeCine.getTipoDeSala() == formato:
                    grupoSalasPorFormato.append(salaDeCine)

            for pelicula in self._cartelera:
                if pelicula.getTIpoDeFormato() == formato:
                    grupoPeliculasPorFormato.append(pelicula)
            
            if len(grupoPeliculasPorFormato) > grupoSalasPorFormato:

                cantidadMaxPeliculaPorSala = len(grupoPeliculasPorFormato) % len(grupoSalasPorFormato) == 0 if len(grupoPeliculasPorFormato) / len(grupoSalasPorFormato) else int(len(grupoPeliculasPorFormato) / len(grupoSalasPorFormato)) + 1

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
        
        #SucursalCine._ticketsDisponibles.clear()

        for sede in SucursalCine._sucursalesCine:
            
            sede._distribuirPeliculasPorSala()
            sede._crearHorariosPeliculasPorSala()


    
    @classmethod
    def logicaInicioSIstemaReservarTicket(cls):

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

            #sede.ticketsParaDescuento.clear()

            for ticket in sede._ticketsDisponibles:
                
                if ticket.getSucursalCompra() == sede._ubicacion and ticket.getHorario().date() == SucursalCine._fechaActual:
                    #sede.ticketsParaDescuento.append(ticket)
                    pass

                if (ticket.getHorario() + ticket.getPelicula().getDuracion) < SucursalCine._fechaActual:
                    ticketsAEliminar.append(ticket)
                
        SucursalCine._dropHorariosVencidos()

        for ticket in ticketsAEliminar:
            SucursalCine._ticketsDisponibles.remove(ticket)
        
        #for cliente in SucursalCine._clientes:
            #cliente.dropTicketsCaducados()

    #def obtenerSucursalPorId(cls):

    #def obetenerSalaDeCinePorId(self):

    #def obtenerPeliculaPorId(self):

    @classmethod
    def notificarFechaLimiteMembresia(cls):
        pass

    def eliminar_producto(self, productos_eliminar):
        for producto in productos_eliminar:
            if producto in self.inventario_cine:
                self.inventario_cine.remove(producto)

    def filtrar_por_nombre_de_producto(nombre_producto, inventario):
     productos_encontrados = []

     for producto in inventario:
        if producto.get_nombre() == nombre_producto:
            productos_encontrados.append(producto)

     return productos_encontrados 

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
    
    def logica_semanal_producto(sucursales_cine):
     for sede in sucursales_cine:
        for producto in sede.get_inventario_cine():
            if producto.get_tipo_producto() == "comida" or producto.get_tipo_producto() == "souvenir":
                sede.logica_calificacion_productos(producto)                 

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

    def seleccionar_sucursal_aleatoriamente(self,sucursal_cine):
     if len(sucursales_cine) <= 1:
        raise ValueError("No hay suficientes sucursales para seleccionar una diferente.")
    
     while True:
        numero_aleatorio = random.randint(0, len(sucursales_cine) - 1)
        sucursal_seleccionada = sucursales_cine[numero_aleatorio]
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
    
    @classmethod
    def getFechaActual(self):
        return SucursalCine._fechaActual
    
    @classmethod
    def setFechaActual(cls, fechaActual):
        SucursalCine._fechaActual = fechaActual
    
    @classmethod
    def getTiempoLimpiezaSalaDeCine(cls):
        return SucursalCine._TIEMPO_LIMPIEZA_SALA_DE_CINE
    
    @classmethod
    def getTiempoLimiteReservaTicket(cls):
        return SucursalCine._TIEMPO_LIMITE_RESERVA_TICKET
    
    @classmethod
    def getTicketsDisponibles(cls):
        return SucursalCine._ticketsDisponibles
    
    @classmethod
    def setTicketsDisponibles(cls, ticketsDisponibles):
        SucursalCine._ticketsDisponibles = ticketsDisponibles
