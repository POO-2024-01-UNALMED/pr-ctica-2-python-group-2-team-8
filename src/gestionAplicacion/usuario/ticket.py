from metodoPago import MetodoPago

class Ticket:
    
#Attributes
################################################

    _cantidadTicketsCreados = 0

    def __init__(self, pelicula, horario, numeroAsiento, sucursalCompra):
        self._pelicula = pelicula
        self._horario = horario
        self._numeroAsiento = numeroAsiento
        self._sucursalCompra = sucursalCompra
        self._precio = self._clienteSuertudo()
        self._salaDeCine = pelicula.getSalaCinePresentacion()

        self._idTicket = 0
        self._dueno = None
        #self._descuento = True

#Methods
################################################

    def _clienteSuertudo(self):
        
        if (self._sucursalCompra.getCantidadTicketsGenerados() ** 1/2 ) % 1 == 0:
            if self._pelicula.getTipoDeFormato() == "4D" or self._pelicula.getTipoDeFormato() == "3D":
                return self._pelicula.getPrecio() * 0.5
            else:
                return self._pelicula.getPrecio() * 0.2
        else:
            return self._pelicula.getPrecio()
            
    def procesarPagoRealizado(self, cliente):
        
        MetodoPago.asignarMetodosDePago(cliente)

        cliente.getTickets().append(self)
        self._dueno = cliente

        self._sucursalCompra.setCantidadTicketsCreados(self._sucursalCompra.getCantidadTicketsCreados() + 1)

        Ticket._cantidadTicketsCreados += 1
        self._idTicket = Ticket._cantidadTicketsCreados

        #Añadir ticket a tickets disponibles para calificar en caso de tener problemas con serialización

        #Añadir lógica descuento (Rusbel)

        #Añadir lógica código juegos (Juan)



    #def factura(self):

    #def generarCodigoTicket(self):

    #def encontrarGeneroCodigoPelicula(self, codigo):

#Getters and Setters
################################################

    def getIdTicket(self):
        return self._idTicket
    
    def setIdTicket(self, idTicket):
        self._idTicket = idTicket

    @classmethod
    def getCantidadTicketsCreados(cls):
        return Ticket._cantidadTicketsCreados
    
    @classmethod
    def setCantidadTicketsCreados(cls, cantidadTicketsCreados):
        Ticket._cantidadTicketsCreados = cantidadTicketsCreados

    def getDueno(self):
        return self._dueno
    
    def setDueno(self, dueno):
        self._dueno = dueno

    def getPelicula(self):
        return self._pelicula
    
    def setPelicula(self, pelicula):
        self._pelicula = pelicula

    def getSalaDeCine(self):
        return self._salaDeCine
    
    def setSalaDeCine(self, salaDeCine):
        self._salaDeCine = salaDeCine

    def getHorario(self):
        return self._horario
    
    def setHorario(self, horario):
        self._horario = horario

    def getNumeroAsiento(self):
        return self._numeroAsiento
    
    def setNumeroAsiento(self, numeroAsiento):
        self._numeroAsiento = numeroAsiento

    def getPrecio(self):
        return self._precio
    
    def setPrecio(self, precio):
        self._precio = precio
    
    def getSucursalCompra(self):
        return self._sucursalCompra
    
    def setSucursalCompra(self, sucursalCompra):
        self._sucursalCompra = sucursalCompra
        