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

    def __init__(self, tituloProceso='', descripcionProceso='', tituloCriterios = "", textEtiquetas = None, tituloValores = "", infoElementosInteractuables = None, habilitado = None):
        super().__init__(ventanaLogicaProyecto)
        self._tituloCriterios = tituloCriterios
        self._infoEtiquetas = textEtiquetas
        self._tituloValores = tituloValores
        self._infoElementosInteractuables = infoElementosInteractuables
        self._habilitado = habilitado

        self._elementosInteractivos = []
        self._clienteProceso = None
        
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
                elementoInteractivo = tk.Entry(self, textvariable=tk.StringVar(str(infoElementosInteractuables[i][0])))

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
    
    def getClienteProceso(self):
        return self._clienteProceso
    
    def tieneValoresPorDefecto(self):
        for i in range(0, len(self._infoElementosInteractuables)):

            valorPorDefecto = '' if self._infoElementosInteractuables[i] == None else self._infoElementosInteractuables[i][0] if len(self._infoElementosInteractuables[i]) == 1 else self._infoElementosInteractuables[i][1]

            if self.getValue(self._infoEtiquetas[i]) == valorPorDefecto:
                return True
        
        return False
               
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
                clienteProceso = SucursalCine.buscarCliente(numDocumentoSeleccionado, tipoDocumentoSeleccionado)

                if clienteProceso is None:
                    FrameCrearUsuario(tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalSeleccionada).mostrarFrame(self)

                else:
                    self._clienteProceso = clienteProceso
                    frameVentanaPrincipal.construirMenu()
                    frameVentanaPrincipal.mostrarFrame(self)

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
                self._clienteProceso = Cliente(nombreCliente, edadCliente, self._numDocumentoCliente, self._tipoDocumentoCliente, SucursalCine.obtenerSucursalPorUbicacion(self._ubicacionSucursalActual))
                frameVentanaPrincipal.construirMenu()
                frameVentanaPrincipal.mostrarFrame(self)
        
        else:
            messagebox.showerror('Error', 'No pueden haber campos vacíos o con valores por defecto')
        

class FrameVentanaPrincipal(FieldFrame):

    def __init__(self):
        super().__init__( textEtiquetas = [])

        self._imagenFramePrincipal = tk.PhotoImage(file = 'src/iuMain/imagenes/fachadaCine.png')
        
        self._labelImagen = tk.Label(self, image = self._imagenFramePrincipal)
        self._labelImagen.grid(row=0, column=0)

        #Se buscan los widget que tenga FieldFrame y se eliminan para este frame.
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

    def construirMenu(self):
        barraMenuPrincipal = tk.Menu(ventanaLogicaProyecto, font=("Courier", 9))
        ventanaLogicaProyecto.config(menu=barraMenuPrincipal)
        menuOpcionesPrincipal = tk.Menu(barraMenuPrincipal, tearoff= 0, font=("Courier", 9), activebackground= "grey", activeforeground="black")
        barraMenuPrincipal.add_cascade(label="Funcionalidades", menu= menuOpcionesPrincipal, font=("Courier", 9))

        menuOpcionesPrincipal.add_command(label="Reserva de tiquetes", command = "")
        menuOpcionesPrincipal.add_command(label="Zona de juegos", command="")
        menuOpcionesPrincipal.add_command(label="Calificaciones", command="")
        menuOpcionesPrincipal.add_command(label="Servicio de comida/souvenir", command="")
        menuOpcionesPrincipal.add_command(label="Sistema de membresías", command="")    

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
    cliente3 = Cliente('Gerson', 24, 98765, TipoDocumento.CC, sucursalCine3)
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


if __name__ == '__main__':

    #Creamos los objetos de la lógica del proyecto
    objetosBasePractica2()

    #Prueba de filtrado de objetos


    #Creacion de la ventana de inicio 
    ventanaInicio = tk.Tk()
    ventanaInicio.title("Ventana de Incio Cinemar")
    ventanaInicio.geometry("500x450")
    ventanaInicio.config(bg = "light gray")

    #Ventana Funcionalidad
    ventanaLogicaProyecto = tk.Toplevel(ventanaInicio)
    ventanaLogicaProyecto.title("Ventana Principal Cinemar")
    ventanaLogicaProyecto.geometry("640x480")

    #Frames de lógica proyecto
    frameIniciarSesion = FrameInicioSesion()
    frameVentanaPrincipal = FrameVentanaPrincipal()

    #Nota: Si desean usar pack(No recomendado, se buguea con el uso de texto dentro del frame) 
    # en vez de place ponganle a los frames el fill = "both" pa que se vea melo

    #Creacion y posicionamiento de P1 (237.5x432)
    frameGrandeIzquierdoP1 = tk.Frame(ventanaInicio, bd = 2, relief= "solid", cursor="heart")
    frameGrandeIzquierdoP1.place(relx= 0.015, rely= 0.02, relwidth= 0.475, relheight = 0.96)
    #frameGrandeIzquierdoP1.pack(side = "left", padx = 5, pady = 5, expand = True,)

    #Creacion y posicionamiento de P2
    frameGrandeDerechoP2 = tk.Frame(ventanaInicio, bd = 2, relief= "solid", cursor="heart")
    frameGrandeDerechoP2.place(relx= 0.51, rely= 0.02, relwidth= 0.475, relheight = 0.96)
    #frameGrandeDerechoP2.pack(side = "right", padx = 5, pady = 5, expand = True, fill= "both")

    #Creacion y posicionamiento de P3
    frameSuperiorIzquierdoP3 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid")
    frameSuperiorIzquierdoP3.place(relx= 0.02, rely= 0.011, relwidth= 0.96, relheight = 0.37)
    #frameSuperiorIzquierdoP3.pack(side = "top", padx = 5, pady = 5, expand = True, fill= "both")

    mensajeBienvenida = tk.Label(frameSuperiorIzquierdoP3, text= "☻Bienvenido a \nnuestro Cine☻", bd= 1, font= ("Courier", 12, "bold"), fg= "#FFD700", relief= "solid")
    mensajeBienvenida.pack(anchor= "c", expand=True)

    #Creacion y posicionamiento de P4
    frameInferiorIzquierdoP4 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid", height= 100)
    frameInferiorIzquierdoP4.place(relx= 0.02, rely= 0.392, relwidth= 0.96, relheight = 0.597)
    #frameInferiorIZquierdoP4.pack(side = "bottom", padx = 5, pady = 5, expand = True, fill= "both")

    #Metodo boton ingresar
    def ingresarVentanaPrincipal():
        #Escondemos la ventana de inicio
        ventanaInicio.withdraw()
        ventanaLogicaProyecto.deiconify()

        #Mostramos el frame correspondiente
        #frameVentanaPrincipal.mostrarFrame()
        frameIniciarSesion.mostrarFrame()

    botonIngreso = tk.Button(frameInferiorIzquierdoP4, text = "Ingresar", font = ("Courier", 10, "bold"), bg= "#FFD700", command= ingresarVentanaPrincipal)
    botonIngreso.place(relx = 0.3, rely = 0.8462962963, relwidth=0.4, relheight = 0.1305555556)


    # Inicializar índice de la imagen actual
    indice_imagen = 0

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

        tk.PhotoImage(file="src/iuMain/imagenes/Rusbel.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/Andy.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/Eduardo1.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/Gerson.png"),
        tk.PhotoImage(file="src/iuMain/imagenes/Luismi.png"),

    ]
    imagenLabel = tk.Label(frameInferiorIzquierdoP4, image= imagenes[indice_imagen])
    imagenLabel.place(relx = 0.05, y = 5, relheight= 0.8, relwidth=0.9)

    # Asignar evento al Label
    imagenLabel.bind("<Leave>", cambiar_imagen)

    #Creacion y posicionamineto de P5
    frameSuperiorDerechoP5 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid")
    frameSuperiorDerechoP5.place(relx= 0.02, rely= 0.011, relwidth= 0.96, relheight = 0.37)
    #frameSuperiorDerechoP5.pack(side = "top", padx = 5, pady = 5, expand = True, fill= "both")

    #Creacion y posicionamiento de P6
    frameInferiorDerechoP6 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid", height= 100)
    frameInferiorDerechoP6.place(relx= 0.02, rely= 0.392, relwidth= 0.96, relheight = 0.597)
    #frameInferiorDerechoP6.pack(side = "bottom", padx = 5, pady = 5, expand = True, fill= "both")

    #Creacion de la barra de menu
    barraMenu = tk.Menu(ventanaInicio, font=("Courier", 9))
    ventanaInicio.config(menu = barraMenu)

    menuOpciones = tk.Menu(barraMenu, tearoff= 0, font=("Courier", 9), activebackground= "#87CEEB", activeforeground= "black")
    barraMenu.add_cascade(label= "Inicio", menu= menuOpciones, font=("Courier", 9) )

    #Metodos para la barra de opciones
    def mostrarDescripcion(): 
        mensaje = tk.Message(frameSuperiorIzquierdoP3, text=  "En este programa puedes:\n•Comprar Tickets\n•Comprar comida y regalos\n•Usar la zona de juegos\n•Adquirir membresias\n•Calificar nuestros servicios" , font= ("Times New Roman",11))
        mensaje.pack(anchor= "s", expand= True)

    def CerrarVentana():
        ventanaInicio.destroy()

    #Opciones de el menu de inicio
    menuOpciones.add_command(label = "Descripción del programa", command= mostrarDescripcion)
    menuOpciones.add_command(label = "Salir y Guardar", command= CerrarVentana)

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


                 