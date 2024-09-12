import sys
import os

# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, time, timedelta
from gestionAplicacion.usuario.tipoDocumento import TipoDocumento
from gestionAplicacion.sucursalCine import SucursalCine
from gestionAplicacion.usuario.cliente import Cliente
from gestionAplicacion.servicios.herencia.servicioComida import ServicioComida
from gestionAplicacion.servicios.herencia.servicioSouvenirs import ServicioSouvenir
from gestionAplicacion.servicios.herencia.servicio import Servicio 
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.proyecciones.pelicula import Pelicula
from gestionAplicacion.proyecciones.salaCine import SalaCine
from gestionAplicacion.usuario.membresia import Membresia
from gestionAplicacion.usuario.metodoPago import MetodoPago

class FieldFrame(tk.Frame):

    _clienteProceso = None
    _frameMenuPrincipal = None
    _framesFuncionalidades = []

    def __init__(self, tituloProceso='', descripcionProceso='', tituloCriterios = "", textEtiquetas = None, tituloValores = "", infoElementosInteractuables = None, habilitado = None):
        super().__init__(ventanaLogicaProyecto)
        self._tituloCriterios = tituloCriterios
        self._infoEtiquetas = textEtiquetas
        self._tituloValores = tituloValores
        self._infoElementosInteractuables = infoElementosInteractuables
        self._habilitado = habilitado

        self._elementosInteractivos = []
        
        tituloFrame = tk.Label(self, text=tituloProceso, font= ("Verdana bold",30), anchor="center")
        tituloFrame.grid(row=0, column=0, columnspan=4, sticky='we')

        descripcionFrame = tk.Label(self, text=descripcionProceso, font= ("Verdana",10), anchor="center", wraplength=300)
        descripcionFrame.grid(row=1, column=0, columnspan=4, sticky='we')

        tituloCrit = tk.Label(self, text = tituloCriterios, font= ("Verdana bold",20), anchor="center")
        tituloCrit.grid(column=0, row=2, padx = (10,10), pady = (10,10))

        tituloVal = tk.Label(self, text = tituloValores, font= ("Verdana bold",20), anchor="center")
        tituloVal.grid(column=1, row=2, padx = (10,10), pady = (10,10))

        for i in range(len(textEtiquetas)):

            labelCriterio = tk.Label(self, text = textEtiquetas[i], font= ("Verdana",12), anchor="center")
            labelCriterio.grid(column=0, row=i+3, padx = (10,10), pady = (10,10))

            elementoInteractivo = None

            if infoElementosInteractuables[i] is None:
                elementoInteractivo = tk.Entry(self)
            
            elif len(infoElementosInteractuables[i]) == 1:
                elementoInteractivo = tk.Entry(self)
                elementoInteractivo.insert(0, infoElementosInteractuables[i][0])

            else:
                elementoInteractivo = ttk.Combobox(self, values=infoElementosInteractuables[i][0])
                elementoInteractivo.set(infoElementosInteractuables[i][1])


            elementoInteractivo.grid(column=1, row=i+3,columnspan=3, padx = (10,10), pady = (10,10))

            if not habilitado[i]:

                if isinstance(elementoInteractivo, ttk.Combobox):
                    elementoInteractivo.configure(state='readonly')
                else:
                    elementoInteractivo.configure(state='disabled')

            self._elementosInteractivos.append(elementoInteractivo)

        tk.Button(self, text="Borrar", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.funBorrar,
        width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 1, row = len(self._infoEtiquetas)+3, columnspan=3)
        tk.Button(self, text="Aceptar", font = ("Verdana", 12), fg = "white", bg = "gray", command=self.funAceptar,
        width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 0, row = len(self._infoEtiquetas)+3)

    def getValue(self, criterio):
        indice = self._infoEtiquetas.index(criterio)
        return self._elementosInteractivos[indice].get()

    def setValueEntry(self, criterio, valor):
        indice = self._infoEtiquetas.index(criterio)
        self._elementosInteractivos[indice].delete("0","end")
        self._elementosInteractivos[indice].insert(0, valor)
    
    def setValueComoboBox(self, criterio):
        indice = self._elementosInteractivos.index(criterio)
        criterio.set(self._infoElementosInteractuables[indice][1])

    @classmethod
    def setFrameMenuPrincipal(cls, frameMenuPrincipal):
        FieldFrame._frameMenuPrincipal = frameMenuPrincipal

    @classmethod
    def getFrameMenuPrincipal(cls):
        return FieldFrame._frameMenuPrincipal

    def funBorrar(self):
        for elementoInteractivo in self._elementosInteractivos:
            if isinstance(elementoInteractivo, ttk.Combobox):
                self.setValueComoboBox(elementoInteractivo)
            else:
                elementoInteractivo.delete("0","end")
    
    def funAceptar(self):
        pass
    
    def mostrarFrame(self, frameAnterior = None):
        if frameAnterior is not None:
            frameAnterior.pack_forget()
        self.pack(expand=True)
    
    @classmethod
    def getClienteProceso(cls):
        return FieldFrame._clienteProceso
    
    @classmethod
    def setClienteProceso(cls, clienteProceso):
        FieldFrame._clienteProceso = clienteProceso

    @classmethod
    def getFramesFuncionalidades(cls):
        return FieldFrame._framesFuncionalidades
    
    @classmethod
    def setFramesFuncionalidades(cls, framesFuncionalidades):
        FieldFrame._framesFuncionalidades = framesFuncionalidades
    
    def tieneValoresPorDefecto(self):
        for i in range(0, len(self._infoElementosInteractuables)):

            valorPorDefecto = '' if self._infoElementosInteractuables[i] == None else self._infoElementosInteractuables[i][0] if len(self._infoElementosInteractuables[i]) == 1 else self._infoElementosInteractuables[i][1]

            if self.getValue(self._infoEtiquetas[i]) == valorPorDefecto:
                return True
        
        return False
    
    def getElementosInteractivos(self):
        return self._elementosInteractivos

    def logicaInicioProcesosFuncionalidades(self, clienteProceso):

        FieldFrame.setClienteProceso(clienteProceso)

        #Creación Frames funcionalidades
        framesFuncionalidades = [
            FrameReservarTicket(), # <_ Funcionalidad 1
            FrameReservarTicket(), # <- Funcionalidad 2
            FrameReservarTicket(), # <- Funcionalidad 3
            FrameReservarTicket(), # <- funcionalidad 4
            FrameFuncionalidad5() # <- Funcionalidad 5
        ]

        #Setteamos los frames de las funcionalidades al atributo de clase
        FieldFrame.setFramesFuncionalidades(framesFuncionalidades)

        #Ejecutamos la lógica de la ventana del menú principal
        frameVentanaPrincipal.construirMenu()
        frameVentanaPrincipal.mostrarFrame(self)

class FrameInicioSesion(FieldFrame):

    def __init__(self):
        super().__init__(
            tituloProceso = 'Iniciar Sesión',
            descripcionProceso = 'En este apartado gestionamos la lógica de inicio de sesión',
            tituloCriterios = "Criterios Ingreso", 
            textEtiquetas = ['Seleccionar Tipo D.I. :', 'Número D.I. :', 'Seleccionar Sucursal :'], 
            tituloValores = "Datos Ingreso", 
            infoElementosInteractuables = [[TipoDocumento.listadoTiposDeDocumentos(), 'Seleccionar D.I.'], None, [[sede.getUbicacion() for sede in SucursalCine.getSucursalesCine()], 'Seleccionar Sucursal']], 
            habilitado = [False, True, False]
        )
    
    def funAceptar(self):

        if not self.tieneValoresPorDefecto():
            tipoDocumentoSeleccionado = self.getValue('Seleccionar Tipo D.I. :')

            try:
                numDocumentoSeleccionado = int(self.getValue('Número D.I. :'))
            except ValueError:
                messagebox.showerror('Error', f'El campo {self._infoEtiquetas[1].strip(':')}debe ser numérico')
                return

            sucursalSeleccionada = self.getValue('Seleccionar Sucursal :')
            
            confirmacionUsuario = messagebox.askokcancel('Confirmación de datos', f'Los datos ingresados son:\nTipo de documento: {tipoDocumentoSeleccionado}\nNúmero de documento: {numDocumentoSeleccionado}\nSucursal seleccionada: {sucursalSeleccionada}')
            
            if confirmacionUsuario:
                clienteProceso = SucursalCine.buscarCliente(numDocumentoSeleccionado)

                if clienteProceso is None:
                    FrameCrearUsuario(tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalSeleccionada).mostrarFrame(self)

                else:
                    self.logicaInicioProcesosFuncionalidades(clienteProceso)              

        else:
            messagebox.showerror('Error', 'No pueden haber campos vacíos o con valores por defecto')

class FrameCrearUsuario(FieldFrame):

    def __init__(self, tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalSeleccionada):
        super().__init__(
            tituloProceso = 'Crear Usuario', 
            descripcionProceso = 'Hemos detectado que es la primera vez que visitas nuestras sucursales, te invitamos a diligenciar el siguiente formulario de registro',
            tituloCriterios = 'Criterios registro',
            textEtiquetas = ['Nombre :', 'Edad :'],
            tituloValores = 'Datos registro',
            infoElementosInteractuables = [None, None],
            habilitado = [True, True]
            )
        
        self._tipoDocumentoCliente = tipoDocumentoSeleccionado
        self._numDocumentoCliente = numDocumentoSeleccionado
        self._ubicacionSucursalActual = sucursalSeleccionada
        
    def funAceptar(self):

        if not self.tieneValoresPorDefecto():
            nombreCliente = self.getValue('Nombre :')

            try:
                edadCliente = int(self.getValue('Edad :'))
            except ValueError:
                messagebox.showerror('Error', f'El campo {self._infoEtiquetas[1].strip(':')}debe ser numérico')
                return
            
            confirmacionCliente = messagebox.askokcancel('Confirmación datos', f'Los datos ingresados son:\nNombre: {nombreCliente}\nEdad: {edadCliente}')

            if confirmacionCliente:
                self.logicaInicioProcesosFuncionalidades(Cliente(nombreCliente, edadCliente, self._numDocumentoCliente, self._tipoDocumentoCliente, SucursalCine.obtenerSucursalPorUbicacion(self._ubicacionSucursalActual)))
        
        else:
            messagebox.showerror('Error', 'No pueden haber campos vacíos o con valores por defecto')
        

class FrameVentanaPrincipal(FieldFrame):

    def __init__(self):
        super().__init__( textEtiquetas = [] )

        self._imagenFramePrincipal = tk.PhotoImage(file = 'src/iuMain/imagenes/fachadaCine.png')
        
        self._labelImagen = tk.Label(self, image = self._imagenFramePrincipal)
        self._labelImagen.grid(row=0, column=0)

        FieldFrame.setFrameMenuPrincipal(self)

        #Se buscan los widget que tenga FieldFrame y se eliminan para este frame.
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

    def construirMenu(self):
        barraMenuPrincipal = tk.Menu(ventanaLogicaProyecto, font=("Courier", 9))
        ventanaLogicaProyecto.config(menu=barraMenuPrincipal)
        menuOpcionesPrincipal = tk.Menu(barraMenuPrincipal, tearoff= 0, font=("Courier", 9), activebackground= "grey", activeforeground="black")
        barraMenuPrincipal.add_cascade(label="Funcionalidades", menu= menuOpcionesPrincipal, font=("Courier", 9))

        menuOpcionesPrincipal.add_command(label="Reserva de tiquetes", command = self.ingresarFuncionalidad1)
        menuOpcionesPrincipal.add_command(label="Zona de juegos", command="")
        menuOpcionesPrincipal.add_command(label="Calificaciones", command="")
        menuOpcionesPrincipal.add_command(label="Servicio de comida/souvenir", command="")
        menuOpcionesPrincipal.add_command(label="Sistema de membresías", command=self.ingresarFuncionalidad5)
    
    def ingresarFuncionalidad1(evento):
        FieldFrame.getFramesFuncionalidades()[0].mostrarFrame(FieldFrame.getFrameMenuPrincipal())

    def ingresarFuncionalidad5(evento):
        FieldFrame.getFramesFuncionalidades()[4].mostrarFrame(FieldFrame.getFrameMenuPrincipal())
        FieldFrame.getFramesFuncionalidades()[4].crearBotonesMembresia()

class FrameReservarTicket(FieldFrame):

    def __init__(self):

        clienteProceso = FieldFrame.getClienteProceso()

        self._carteleraCliente = Pelicula.filtrarCarteleraPorCliente(clienteProceso)
        self._formatosPeliSeleccionada = None
        self._horariosPeliSeleccionada = None
        self._peliculaProceso = None
        self._horarioProceso = None

        filtroNombresCartelera = Pelicula.filtrarCarteleraPorNombre(self._carteleraCliente)
        filtroPelisRecomendadas = Pelicula.filtarCarteleraPorGenero(self._carteleraCliente, clienteProceso.generoMasVisto())

        super().__init__(
            tituloProceso = 'Reservar ticket',
            descripcionProceso = f'En este espacio solicitamos los datos necesarios para reservar un ticket, debe ingresar los datos de forma secuencial, es decir, en el orden en que se encuentran (Fecha Actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}; Hora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)})',
            tituloCriterios = 'Criterios reserva',
            textEtiquetas = ['Seleccionar película : ', 'Seleccionar formato : ', 'Seleccionar horario : '], 
            tituloValores = 'Valores ingresados',
            infoElementosInteractuables = [
                [Pelicula.mostrarNombrePeliculas(
                    filtroNombrePeliculas = filtroNombresCartelera, 
                    clienteProceso = clienteProceso, 
                    nombrePeliculasRecomendadas = filtroPelisRecomendadas), 'Selecionar película'], 
                [[], 'Seleccionar formato'], 
                [[], 'Seleccionar horario']
            ],
            habilitado = [False, False, False]
        )

        for elemento in self.getElementosInteractivos():
            elemento.grid_configure(sticky='we')

        self._comboBoxPeliculas = self.getElementosInteractivos()[0]
        self._comboBoxFormatos = self.getElementosInteractivos()[1]
        self._comboBoxHorarios = self.getElementosInteractivos()[2]

        self._comboBoxPeliculas.bind('<<ComboboxSelected>>', self.setFormatos)
        self._comboBoxFormatos.bind('<<ComboboxSelected>>', self.setHorarios)
        
    def setFormatos(self, event):
        nombrePeliculaSeleccionada = self.getValue('Seleccionar película : ')

        self._formatosPeliSeleccionada = Pelicula.obtenerPeliculasPorNombre(nombrePeliculaSeleccionada, self._carteleraCliente)

        self._comboBoxFormatos.configure(values = [peli.getTipoDeFormato() for peli in self._formatosPeliSeleccionada])

    def setHorarios(self, event):
        
        for pelicula in self._formatosPeliSeleccionada:
            if pelicula.getTipoDeFormato() == self.getValue('Seleccionar formato : '):
                self._peliculaProceso = pelicula 


        self._horariosPeliSeleccionada = self._peliculaProceso.filtrarHorariosPelicula()

        self._comboBoxHorarios.configure(values = self._horariosPeliSeleccionada)
    
    #Programar el borrar para que los values de los combobox queden vacíos o investigar forma de que los combobox no desplieguen el menú
    #Hacer que en el comboBox de horarios se muestre un apartado de horario de presentación en vivo, programar método en clase película
    #Crear botón de volver en el FieldFrame (Crear un frame que almacene tres o dos botones según cierto parámetro, ese parámetro dará por defecto 2)

class FrameFuncionalidad5(FieldFrame):

    def __init__(self):
        super().__init__(
            tituloProceso="Membresías",
            descripcionProceso= f"Bienvenido a nuestro sistema de membresías. (Fecha Actual: {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}; Hora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)})",
            textEtiquetas= []
        )
    

    def crearBotonesMembresia(self):
        botonBasico = tk.Button(FieldFrame.getFramesFuncionalidades()[4], text="Básico").grid(padx=10, pady=10, row= 2, column=0)
        botonHeroico = tk.Button(FieldFrame.getFramesFuncionalidades()[4], text = "Heroico").grid(padx=10, pady=10, row= 2, column=1)
        botonGlobal = tk.Button(FieldFrame.getFramesFuncionalidades()[4], text= "Global").grid(padx=10, pady=10, row= 2, column=2)
        botonChallenger = tk.Button(FieldFrame.getFramesFuncionalidades()[4], text= "Challenger").grid(padx=10, pady=10, row= 2, column=3)
        botonRadiante = tk.Button(FieldFrame.getFramesFuncionalidades()[4], text= "Radiante").grid(padx=10, pady=10, row= 2, column=4)

def objetosBasePractica2():

    sucursalCine1 = SucursalCine("Bucaramanga")
    sucursalCine2 = SucursalCine("Marinilla")
    sucursalCine3 = SucursalCine("Medellín")

    servicioComida = ServicioComida("comida", sucursalCine2)
    servicioSouvenirs = ServicioSouvenir("souvenir", sucursalCine2)

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

    sucursalCine2.getServicios().append(servicioComida)
    sucursalCine2.getServicios().append(servicioSouvenirs)

    cliente1 = Cliente("Rusbel", 18, 13434, TipoDocumento.CC, sucursalCine2)
    cliente2 = Cliente("Andy", 18, 14343, TipoDocumento.CC, sucursalCine1)
    cliente3 = Cliente('Gerson', 23, 98765, TipoDocumento.CC, sucursalCine3)
    cliente4 = Cliente('Juanjo', 18, 987, TipoDocumento.CC, sucursalCine1)

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

    membresia1 = Membresia("Básico", 1, 5000, 10)
    membresia2 = Membresia("Heróico", 2, 10000, 15)
    membresia3 = Membresia("Global", 3, 15000, 20)
    membresia4 = Membresia("Challenger", 4, 25000, 25)
    membresia5 = Membresia("Radiante", 5, 30000, 30)

    metodoPago1 = MetodoPago("Bancolombia", 0.10, 200000)
    metodoPago2 = MetodoPago("AV Villas", 0.05, 120000)
    metodoPago3 = MetodoPago("Banco Agrario", 0.15, 300000)
    metodoPago4 = MetodoPago("Efectivo", 0, 5000000)

    sucursalCine2.getServicios()[0].setCliente(cliente1)

    sucursalCine2.getServicios()[0].setInventario(sucursalCine2.getServicios()[0].actualizarInventario())
    print(sucursalCine2.getServicios()[0].mostrarInventario())

    SucursalCine.logicaInicioSIstemaReservarTicket()

def ventanaDeInicio(): 

    #Tamaño ventana Inicio = (640 x 480)

    #Creacion y posicionamiento de P1 (304 x 460.8)
    frameGrandeIzquierdoP1 = tk.Frame(ventanaInicio, bd = 2, relief= "solid", cursor="heart", bg = "black")
    frameGrandeIzquierdoP1.place(relx= 0.015, rely= 0.02, relwidth= 0.475, relheight = 0.96)

    #Creacion y posicionamiento de P2 (304 x 460.8)
    frameGrandeDerechoP2 = tk.Frame(ventanaInicio, bd = 2, relief= "solid", cursor="heart",  bg = "black")
    frameGrandeDerechoP2.place(relx= 0.51, rely= 0.02, relwidth= 0.475, relheight = 0.96)

    #Creacion y posicionamiento de P3 (291.84 x 170.496)
    frameSuperiorIzquierdoP3 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid", bg = "#ADD8E6")
    frameSuperiorIzquierdoP3.place(relx= 0.02, rely= 0.011, relwidth= 0.96, relheight = 0.37)

    mensajeBienvenida = tk.Label(frameSuperiorIzquierdoP3, text= "☻Bienvenido a \nnuestro Cine☻", font= ("Courier", 23, "bold"), fg= "#6495ED", bg =  "#ADD8E6")
    mensajeBienvenida.pack(anchor= "c", expand=True)

    #Creacion y posicionamiento de P4 (291.84 x 275.0976)
    frameInferiorIzquierdoP4 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid", height= 100, bg = "#ADD8E6")
    frameInferiorIzquierdoP4.place(relx= 0.02, rely= 0.392, relwidth= 0.96, relheight = 0.597)

    #Metodo boton ingresar
    def ingresarVentanaPrincipal():
        #Escondemos la ventana de inicio
        ventanaInicio.withdraw()
        ventanaLogicaProyecto.deiconify()

        #Mostramos el frame correspondiente
        #frameVentanaPrincipal.mostrarFrame()
        frameIniciarSesion.mostrarFrame()

    #botonIngreso = tk.Button(frameInferiorIzquierdoP4, text = "Ingresar", font = ("Courier", 10, "bold"), bg= "#FFD700", command= ingresarVentanaPrincipal)
    #botonIngreso.place(relx = 0.3, rely = 0.8462962963, relwidth=0.4, relheight = 0.1305555556)


    # Función para cambiar la imagen cuando el mouse entra
    def cambiar_imagen(event):
        global indice_imagen

        #Se verifica si estamos en el indice de la ultima imagen
        #y lo cambiamos por el indice de la primera menos 1
        if indice_imagen == 4: 
            indice_imagen = -1
        # Cambiar al siguiente índice
        imagenLabel.config(image=imagenes[indice_imagen+1])
        #Se incrementa el indice
        indice_imagen+=1

    imagenes = [
        
        tk.PhotoImage(file="src/iuMain/imagenes/P41.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/P42.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/P43.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/P44.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/P45.png"),

    ]
    imagenLabel = tk.Button(frameInferiorIzquierdoP4, image= imagenes[indice_imagen], command = ingresarVentanaPrincipal, bd = 1, relief = "solid")
    imagenLabel.place(relheight = 1, relwidth = 1)
    #imagenLabel.place(relx = 0.05, y = 5, relheight= 0.8, relwidth=0.9)

    # Asignar evento al Label
    imagenLabel.bind("<Leave>", cambiar_imagen)

    #Creacion y posicionamineto de P5 (291.84 x 170.496)
    frameSuperiorDerechoP5 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid", bg = "#ADD8E6")
    frameSuperiorDerechoP5.place(relx= 0.02, rely= 0.011, relwidth= 0.96, relheight = 0.37)

    nombres = ["Rusbel Danilo Jaramillo", "Edinson Andres Ariza", "Juan José González", "Gerson Bedoya", "Santiago Castro"]
    edades =  ["19", "18", "18", "23", "18"]
    estudios = ["Ingeniero de Sistemas"]*5
    instituciones = ["Universidad Nacional Colombia"]*5
    residencias = ["Marinilla", "Medellín", "Bello", "Medellín", "Rionegro"]
    emails = ["rjaramilloh@unal.edu.co", "edarizam@unal.edu.co","juagonzalezmo@unal.edu.co","gbedoyah@unal.edu.co", "sancastrohe@unal.edu.co"]

    nombre = tk.Label(frameSuperiorDerechoP5, text = nombres[0], font=("Times New Roman", 18, "bold"), bg= "#ADD8E6", fg = "#6495ED")
    nombre.pack(anchor="c")
    hojaDeVida = tk.Message(frameSuperiorDerechoP5, text = "\n•Edad: " + edades[0]  + "\n•Estudios: " + estudios[0] +"\n•Institución: "+ instituciones[0] +"\n•Residencia: " + residencias[0]+ "\n•Email: " + emails[0], font=("Times New Roman", 12), bg= "#ADD8E6", width = 300 )
    hojaDeVida.pack(anchor= "c")

    def cambiarHojaDeVida(event):
        global indice_hojaDeVida

        if indice_hojaDeVida==4:
            indice_hojaDeVida = -1
            
        nombre.config(text = nombres[indice_hojaDeVida + 1])
        hojaDeVida.config(text= "\n•Edad: " + edades[indice_hojaDeVida+1]  + "\n•Estudios: " + estudios[indice_hojaDeVida+1] +"\n•Institución: "+ instituciones[indice_hojaDeVida+1] +"\n•Residencia: " + residencias[indice_hojaDeVida+1]+ "\n•Email: " + emails[indice_hojaDeVida+1])
        cambioDeImagenes(event)
        indice_hojaDeVida+=1

    hojaDeVida.bind("<Button-1>", cambiarHojaDeVida)
    nombre.bind("<Button-1>", cambiarHojaDeVida)

    #Creacion y posicionamiento de P6 (291.84 x 275.0976)
    frameInferiorDerechoP6 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid", height= 100, bg = "#ADD8E6")
    frameInferiorDerechoP6.place(relx= 0.02, rely= 0.392, relwidth= 0.96, relheight = 0.597)


    imagenes1 = [
        tk.PhotoImage(file="src/iuMain/imagenes/a1.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/a2.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/a3.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/a4.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/a5.png"),
    ]

    imagenes2 = [
        tk.PhotoImage(file="src/iuMain/imagenes/b1.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/b2.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/b3.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/b4.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/b5.png"),
    ]

    imagenes3 = [
        tk.PhotoImage(file="src/iuMain/imagenes/c1.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/c2.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/c3.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/c4.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/c5.png"),
    ]

    imagenes4 = [
        tk.PhotoImage(file="src/iuMain/imagenes/d1.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/d2.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/d3.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/d4.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/d5.png"),
    ]

    label1 = tk.Label(frameInferiorDerechoP6, image=imagenes1[0], bd = 3, relief="solid")
    label1.grid(row=0, column=0, sticky="nsew")

    label2 = tk.Label(frameInferiorDerechoP6, image=imagenes2[0], bd = 3, relief="solid")
    label2.grid(row=0, column=1, sticky="nsew")

    label3 = tk.Label(frameInferiorDerechoP6, image=imagenes3[0], bd = 3, relief="solid")
    label3.grid(row=1, column=0, sticky="nsew")

    label4 = tk.Label(frameInferiorDerechoP6, image=imagenes4[0], bd = 3, relief="solid")
    label4.grid(row=1, column=1, sticky="nsew")

    def cambioDeImagenes(event):
        label1.config(image = imagenes1[indice_hojaDeVida + 1])
        label2.config(image = imagenes2[indice_hojaDeVida + 1])
        label3.config(image = imagenes3[indice_hojaDeVida + 1])
        label4.config(image = imagenes4[indice_hojaDeVida + 1])

    #Creacion de la barra de menu
    barraMenu = tk.Menu(ventanaInicio, font=("Courier", 9))
    ventanaInicio.config(menu = barraMenu)

    menuOpciones = tk.Menu(barraMenu, tearoff= 0, font=("Courier", 9), activebackground= "#87CEEB", activeforeground= "black")
    barraMenu.add_cascade(label= "Inicio", menu= menuOpciones, font=("Courier", 9) )

    mensaje = tk.Message(frameSuperiorIzquierdoP3, text=  "En este programa puedes:\n•Comprar Tickets\n•Comprar comida y regalos\n•Usar la zona de juegos\n•Adquirir membresias\n•Calificar nuestros servicios" , font= ("Times New Roman",11), bg="#ADD8E6")
    #Metodos para la barra de opciones
    def mostrarDescripcion():
        #mensaje = tk.Message()
        if int(mensajeBienvenida.cget("font").split()[1]) == 15:
            mensaje.pack_forget()
            mensajeBienvenida.config(font= ("Courier", 23, "bold")) 
        else:
            mensajeBienvenida.config(font= ("Courier", 15, "bold")) 
            mensaje.pack(anchor= "s", expand= True)

    def CerrarVentana():
        ventanaInicio.destroy()

    #Opciones de el menu de inicio
    menuOpciones.add_command(label = "Descripción del programa", command= mostrarDescripcion)
    menuOpciones.add_command(label = "Salir y Guardar", command= CerrarVentana)


if __name__ == '__main__':

    #Creamos los objetos de la lógica del proyecto
    objetosBasePractica2()

    #Creacion de la ventana de inicio 
    ventanaInicio = tk.Tk()
    ventanaInicio.title("Ventana de Incio Cinemar")
    ventanaInicio.geometry("640x480")
    ventanaInicio.config(bg = "#ADD8E6")

    # Inicializar índice de la imagen para p4 y p5
    indice_imagen = 0
    indice_hojaDeVida = 0
    ventanaDeInicio()

    #Ventana Funcionalidad
    ventanaLogicaProyecto = tk.Toplevel(ventanaInicio)
    ventanaLogicaProyecto.title("Ventana Principal Cinemar")
    ventanaLogicaProyecto.geometry("640x480")

    #Frames de lógica proyecto
    frameIniciarSesion = FrameInicioSesion()
    frameVentanaPrincipal = FrameVentanaPrincipal()


    ventanaLogicaProyecto.withdraw()
    ventanaInicio.mainloop()

def calificacion ():
    
    #Description: Esta funcionalidad 3 se va a encargar de hacer la respectiva calificacion de peliculas y productos dependiendo
	#de los gustos del cliente, ya que con estas calificaciones vamos a hacer un proceso interno de logica de negocio 
	#dentro del cine, para poder saber que peliculas o productos estan funcionando bien o por consecuencia, cuales 
	#estan funcionando mal
    
    #Le damos la bienvenida al cliente
    print("********Bienvenido a la calificacion de productos*********")
    
	
	
    while verificar:
        try:
            eleccion = int(input("\n1. Calificar Comida.\n2. Calificar Pelicula\n3. Volver al menu.\nSeleccione una opcion: "))
        except ValueError:
            print("\nError, debes ingresar un dato numérico\n")
            continue
        
        if eleccion == 3:
            #volveralmenu()
            break
        elif eleccion == 1 and eleccion==2:
            verificar = False
            continue
        
        else:
            print("\nOpción no válida, por favor ingrese una opción correcta.\n")

    if eleccion == 1:        
             print (("\n********Bienvenido al apartado de calificacion de comida********"))
             #if clienteProceso.get


                 