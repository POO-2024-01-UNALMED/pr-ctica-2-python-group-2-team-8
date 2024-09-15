import sys
import os

# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from gestionAplicacion.servicios.bono import *
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
from excepciones.iuExceptions import iuExceptions, iuEmptyValues, iuDefaultValues
from gestionAplicacion.usuario.tarjetaCinemar import TarjetaCinemar
from gestionAplicacion.servicios.arkade import Arkade
from gestionAplicacion.usuario.ticket import Ticket

class FieldFrame(tk.Frame):

    _clienteProceso = None
    _frameMenuPrincipal = None
    _framePasarelaDePagos = None
    _framesFuncionalidades = []

    def __init__(self, tituloProceso='', descripcionProceso='', tituloCriterios = "", textEtiquetas = "", tituloValores = "", infoElementosInteractuables = None, habilitado = None, botonVolver = False, desplazarBotonesFila = 0, frameAnterior = None):
        super().__init__(ventanaLogicaProyecto)
        self._tituloCriterios = tituloCriterios
        self._infoEtiquetas = textEtiquetas
        self._tituloValores = tituloValores
        self._infoElementosInteractuables = infoElementosInteractuables
        self._habilitado = habilitado

        self._elementosInteractivos = []
        self._frameAnterior = frameAnterior
        
        tituloFrame = tk.Label(self, text=tituloProceso, font= ("Verdana bold",30), anchor="center")
        tituloFrame.grid(row=0, column=0, columnspan=4, sticky='we')

        descripcionFrame = tk.Label(self, text=descripcionProceso, font= ("Verdana",10), anchor="center", wraplength=500)
        descripcionFrame.grid(row=1, column=0, columnspan=4, sticky='we')

        tituloCrit = tk.Label(self, text = tituloCriterios, font= ("Verdana bold",20), anchor="center")
        tituloCrit.grid(column=0, row=2, padx = (10,10), pady = (10,10))

        tituloVal = tk.Label(self, text = tituloValores, font= ("Verdana bold",20), anchor="center")
        tituloVal.grid(column=1, row=2, padx = (10,10), pady = (10,10))

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

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


            elementoInteractivo.grid(column=1, row=i+3,columnspan=1, padx = (10,10), pady = (10,10))

            if not habilitado[i]:

                if isinstance(elementoInteractivo, ttk.Combobox):
                    elementoInteractivo.configure(state='readonly')
                else:
                    elementoInteractivo.configure(state='disabled')

            self._elementosInteractivos.append(elementoInteractivo)

        if botonVolver:
            frameBotones = tk.Frame(self)

            tk.Button(frameBotones, text="Aceptar", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.funAceptar,
            width=12,height=2).grid(pady = (10,10), padx=(20, 20), column = 0, row = len(self._infoEtiquetas)+3, sticky = 'we')
            tk.Button(frameBotones, text="Volver", font = ("Verdana", 12), fg = "white", bg = "gray", command=self.funVolver,
            width=12,height=2).grid(pady = (10,10), padx=(20, 20), column = 1, row = len(self._infoEtiquetas)+3, sticky = 'we')
            tk.Button(frameBotones, text="Borrar", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.funBorrar,
            width=12,height=2).grid(pady = (10,10), padx=(20, 20), column = 2, row = len(self._infoEtiquetas)+3, sticky = 'we')

            frameBotones.grid(column = 0, row = len(self._infoEtiquetas) + 3 + desplazarBotonesFila, columnspan=2, sticky='we')
        
        else:
            tk.Button(self, text="Borrar", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.funBorrar,
            width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 1, row = len(self._infoEtiquetas)+3 + desplazarBotonesFila)
            tk.Button(self, text="Aceptar", font = ("Verdana", 12), fg = "white", bg = "gray", command=self.funAceptar,
            width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 0, row = len(self._infoEtiquetas)+3 + desplazarBotonesFila)

    def getValue(self, criterio):
        indice = self._infoEtiquetas.index(criterio)
        return self._elementosInteractivos[indice].get()

    def setValueEntry(self, criterio, valor):
        indice = self._infoEtiquetas.index(criterio)
        self._elementosInteractivos[indice].delete("0","end")
        self._elementosInteractivos[indice].insert(0, valor)
    
    def setValueComboBox(self, criterio):
        indice = self._elementosInteractivos.index(criterio)
        criterio.set(self._infoElementosInteractuables[indice][1])

    @classmethod
    def setFrameMenuPrincipal(cls, frameMenuPrincipal):
        FieldFrame._frameMenuPrincipal = frameMenuPrincipal

    @classmethod
    def getFrameMenuPrincipal(cls):
        return FieldFrame._frameMenuPrincipal
    
    @classmethod
    def setFramePasarelaDePagos(cls, framePasarelaDePagos):
        FieldFrame._framePasarelaDePagos = framePasarelaDePagos

    @classmethod
    def getFramePasarelaDePagos(cls):
        return FieldFrame._framePasarelaDePagos

    def funBorrar(self):
        for elementoInteractivo in self._elementosInteractivos:
            if isinstance(elementoInteractivo, ttk.Combobox):
                self.setValueComboBox(elementoInteractivo)
            else:
                elementoInteractivo.delete("0","end")
    
    def evaluarExcepciones(self):
        try:
            valoresVacios = self.tieneCamposVacios()
            if len(valoresVacios) > 0:
                raise iuEmptyValues(valoresVacios)

            valoresPorDefecto = self.tieneCamposPorDefecto()
            if len(valoresPorDefecto) > 0:
                raise iuDefaultValues(valoresPorDefecto)
            
            return True
        
        except iuExceptions as e:
            messagebox.showerror('Error', e.mostrarMensaje())
            return False
    
    def funAceptar(self):
        pass

    def funVolver(self):
        self._frameAnterior.mostrarFrame()
    
    def mostrarFrame(self):

        for widget in ventanaLogicaProyecto.winfo_children():

            if isinstance(widget, tk.Frame):
                widget.pack_forget()

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
    
    def tieneCamposPorDefecto(self):

        camposPorDefecto = []

        for i in range(0, len(self._infoElementosInteractuables)):

            valorPorDefecto = '' if self._infoElementosInteractuables[i] == None else self._infoElementosInteractuables[i][0] if len(self._infoElementosInteractuables[i]) == 1 else self._infoElementosInteractuables[i][1]

            if self.getValue(self._infoEtiquetas[i]) == valorPorDefecto:
                camposPorDefecto.append(self._infoEtiquetas[i])
        
        return camposPorDefecto
    
    def tieneCamposVacios(self):

        camposVacios = []

        for elemento in self._elementosInteractivos:

            if isinstance(elemento, tk.Entry) and self._infoElementosInteractuables[self._elementosInteractivos.index(elemento)] == None:
                continue

            if elemento.get() == '':
                camposVacios.append(self._infoEtiquetas[self._elementosInteractivos.index(elemento)])
        
        return camposVacios

    def getElementosInteractivos(self):
        return self._elementosInteractivos

    def logicaInicioProcesosFuncionalidades(self, clienteProceso):

        FieldFrame.setClienteProceso(clienteProceso)

        self._frameMenuPrincipal = frameVentanaPrincipal

        self.refrescarFramesFuncionalidades()
        
        #Setteamos el frame para los pagos.
        FieldFrame.setFramePasarelaDePagos(FramePasarelaDePagos())

        #Ejecutamos la lógica de la ventana del menú principal
        frameVentanaPrincipal.construirMenu()
        frameVentanaPrincipal.mostrarFrame()
    
    def refrescarFramesFuncionalidades(self):
        #Creación Frames funcionalidades
        framesFuncionalidades = [
            FrameFuncionalidad1(), # <_ Funcionalidad 1
            FrameFuncionalidad2(), # <- Funcionalidad 2
            FrameFuncionalidad3Calificaciones(), # <- Funcionalidad 3
            FrameZonaJuegos(), # <- funcionalidad 4
            FrameFuncionalidad5() # <- Funcionalidad 5
        ]

        #Setteamos los frames de las funcionalidades al atributo de clase
        FieldFrame.setFramesFuncionalidades(framesFuncionalidades)
    
    def getFrameAnterior(self):
        return self._frameAnterior

class VisualFieldFrame(tk.Frame):
        def __init__(self):
            super().__init__(ventanaLogicaProyecto)

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

class FrameReclamoDeBonos(FieldFrame):
    def __init__(self, servicio):
        servicio.actualizarBonos()
        super().__init__(
            tituloProceso = "Bonos",
            descripcionProceso = "En este apartado podras reclamar los bonos que tenes asociados",
            textEtiquetas = ['Bonos Disponibles'],
            infoElementosInteractuables = [[servicio.mostrarBonos(servicio), "Seleccione un Producto"]],
            habilitado = [False],
        )

class FrameGeneracionDeProductos(FieldFrame):
    def __init__(self, servicio):

        self._servicio = servicio
        servicio.setCliente(self._clienteProceso)
        servicio.setInventario(servicio.actualizarInventario())

        super().__init__(
            tituloProceso = "Generacion de orden",
            descripcionProceso = "En este apartado podras seleccionar los productos que deseas comprar",
            tituloCriterios = "Criterio de la orden",
            textEtiquetas = ['Producto',"Cantidad"],
            tituloValores = "Datos de compra",
            infoElementosInteractuables = [[servicio.mostrarInventario(), "Seleccione un Producto"],None],
            habilitado = [False,True,True],
        )
        tituloV = tk.Label(self, text = "Productos en tu orden:", font= ("Verdana bold",20), anchor="center")
        tituloV.grid(column=2, row=2, padx = (10,10), pady = (10,10))

        agregarb = tk.Button(self,text="Agregar Producto", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.agregar,
        width=15,height=2).grid(pady = (10,10), padx=(10,10), column = 2, row = 5,)
        
    def agregar(self):
        if not self.tieneCamposPorDefecto():
            nombreProducto = self._elementosInteractivos[0].get()
            n = 0
            for productos in self._servicio.getInventario():
                nombre = f"{productos.getNombre()} {productos.getTamaño()}"
                if nombre == nombreProducto:
                    if productos.getCantidad() >= int(self._elementosInteractivos[1].get()):
                        self._servicio.agregarOrden(self._servicio.hacerPedido(n ,int(self._elementosInteractivos[1].get()) ,self._clienteProceso.getCineUbicacionActual()))
                        self.mostrar()
                        eliminarb = tk.Button(self,text="Eliminar producto", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.agregar,
                            width=15,height=2).grid(pady = (10,10), padx=(10,10), column = 1, row = 6)
                        break
                    else:
                        messagebox.showerror("Error",f"No hay suficiente cantidad de {productos.getNombre()} {productos.getTamaño()}, solo hay: {productos.getCantidad()}")
                        break
                n+=1
            self.funBorrar()
        else:
           messagebox.showerror("Error","Por favor llenar todos los campos")

    def funAceptar(self):
        FrameReclamoDeBonos(self._servicio).mostrarFrame()

    def mostrar(self):
        labelCriterio = tk.Label(self, text = self._servicio.mostrarOrden(),anchor="w", font= ("Verdana",10))
        labelCriterio.grid(row=3, column=2,rowspan=2, sticky="w")

    
class FrameFuncionalidad2(FieldFrame):
    def __init__(self):

        self._sucursalActual = self._clienteProceso.getCineUbicacionActual()

        super().__init__(
            tituloProceso = "Generacion de orden",
            descripcionProceso = "En este apartado podras seleccionar el servicio que deseas para generar una orden",
            tituloCriterios = "Criterio servicio",
            textEtiquetas = ['Seleccione tipo de servicio'],
            tituloValores = "Dato servicio",
            infoElementosInteractuables = [[self._sucursalActual.mostrarServicios(), "Seleccione un servicio"]],
            habilitado = [False]
        )
        

    def funAceptar(self):
        if not self.tieneCamposPorDefecto():
            if len(self._sucursalActual.getServicios())>1:
                if self._elementosInteractivos[0].get() == "Servicio comida":
                    FrameGeneracionDeProductos(self._sucursalActual.getServicios()[0]).mostrarFrame()
                else:
                    FrameGeneracionDeProductos(self._sucursalActual.getServicios()[1]).mostrarFrame()
            else:
                FrameGeneracionDeProductos(self._sucursalActual.getServicios()[0]).mostrarFrame()
        else:
           messagebox.showerror("Error","Por favor seleccione un servicio")

class FrameInicioSesion(FieldFrame):

    #Construimos el frame usando FieldFrame
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

        #Evaluamos las excepciones de UI
        if self.evaluarExcepciones():

            #Obtenemos el tipo de documento ingresado
            tipoDocumentoSeleccionado = self.getValue('Seleccionar Tipo D.I. :')

            #obtenemos el numero de documento ingresado y evaluamos si es de tipo int
            try:
                numDocumentoSeleccionado = int(self.getValue('Número D.I. :'))
            except ValueError:
                messagebox.showerror('Error', f'El campo {self._infoEtiquetas[1].strip(':')}debe ser numérico')
                return

            #Obtenemos la sucursal seleciconada
            sucursalSeleccionada = self.getValue('Seleccionar Sucursal :')
            
            #Confirmamos las elecciones hechas por el usuario
            confirmacionUsuario = messagebox.askokcancel('Confirmación de datos', f'Los datos ingresados son:\nTipo de documento: {tipoDocumentoSeleccionado}\nNúmero de documento: {numDocumentoSeleccionado}\nSucursal seleccionada: {sucursalSeleccionada}')
            
            if confirmacionUsuario:
                #Evaluamos si es la primera vez que visita nuestro cine
                clienteProceso = SucursalCine.buscarCliente(numDocumentoSeleccionado, tipoDocumentoSeleccionado)

                if clienteProceso is None:
                    #Si es la primera vez, nos dirigimos al frame de crear usuario para crearlo
                    FrameCrearUsuario(tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalSeleccionada).mostrarFrame()
                elif type(clienteProceso) == str:
                    #Detectamos que el número de documento ya se encuentra asignado a otro cliente
                    messagebox.showerror('Error', 'Hemos detectado que este número de documento se encuentra asociado a otro cliente, por favor verifica el tipo o número de documento digitado.')
                else:
                    #En caso de que no, ingresamos al menú principal de nuestro cine
                    messagebox.showinfo('Inicio de sesión exitoso', f'{clienteProceso.getNombre()}, Bienvenid@ a cinemar sede {sucursalSeleccionada}')
                    self.logicaInicioProcesosFuncionalidades(clienteProceso)

class FrameCrearUsuario(FieldFrame):

    #Construimos el frame usando FieldFrame
    def __init__(self, tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalSeleccionada):

        #self._imagenFramePrincipal = tk.PhotoImage(file = 'src/iuMain/imagenes/fachadaCine.png')
        #self._labelImagen = tk.Label(self, image = self._imagenFramePrincipal)
        #self._labelImagen.grid(row=0, column=0)

        super().__init__(
            tituloProceso = 'Crear Usuario', 
            descripcionProceso = 'Hemos detectado que es la primera vez que visitas nuestras sucursales, te invitamos a diligenciar el siguiente formulario de registro',
            tituloCriterios = 'Criterios registro',
            textEtiquetas = ['Nombre :', 'Edad :'],
            tituloValores = 'Datos registro',
            infoElementosInteractuables = [None, None],
            habilitado = [True, True]
            )
        
        #Guardamos los valores obtenidos en el inicio de sesión en vars de instancia
        self._tipoDocumentoCliente = tipoDocumentoSeleccionado
        self._numDocumentoCliente = numDocumentoSeleccionado
        self._ubicacionSucursalActual = sucursalSeleccionada
        
    def funAceptar(self):

        #Evaluamos las excepciones
        if self.evaluarExcepciones():
            #Obtenemos el nombre ingresado
            nombreCliente = self.getValue('Nombre :')

            #Obtenemos la edad ingresada y verificamos si es de tipo int
            try:
                edadCliente = int(self.getValue('Edad :'))
            except ValueError:
                messagebox.showerror('Error', f'El campo {self._infoEtiquetas[1].strip(':')}debe ser numérico')
                return
            
            #Confirmamos las elecciones hechas por el ususario
            confirmacionCliente = messagebox.askokcancel('Confirmación datos', f'Los datos ingresados son:\nNombre: {nombreCliente}\nEdad: {edadCliente}')

            if confirmacionCliente:
                #Verificamos que tenga la edad mínima para ingresar al cine
                if edadCliente > 5:
                    #Verificamos que la edad ingresada sea apropiada para el documento seleccionado
                    if (self._tipoDocumentoCliente == TipoDocumento.CC.value and edadCliente >= 18) or (self._tipoDocumentoCliente == TipoDocumento.TI.value and edadCliente < 18) or (self._tipoDocumentoCliente == TipoDocumento.CE.value and edadCliente >= 18):
                        #Creamos el cliente y nos dirigimos al menú principal de nuestro cine
                        self.logicaInicioProcesosFuncionalidades(Cliente(nombreCliente, edadCliente, self._numDocumentoCliente, self._tipoDocumentoCliente, SucursalCine.obtenerSucursalPorUbicacion(self._ubicacionSucursalActual)))
                    
                    else: 
                        messagebox.showerror('Error', 'Debes seleccionar una edad apropiada para el documento seleccionado anteriormente')
                
                else:
                    messagebox.showerror('Error', 'La edad mínima para acceder a nuestras instalaciones es de 5 años')

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
        barraMenuPrincipal = tk.Menu(ventanaLogicaProyecto, font=("Times New Roman", 10))
        ventanaLogicaProyecto.config(menu=barraMenuPrincipal)
        menuArchivo = tk.Menu(barraMenuPrincipal, tearoff= 0, font=("Times New Roman", 10), activebackground= "light blue", activeforeground="black")
        menuProcesosConsultas = tk.Menu(barraMenuPrincipal, tearoff= 0, font=("Times New Roman", 10), activebackground= "light blue", activeforeground="black")
        menuAyuda = tk.Menu(barraMenuPrincipal, tearoff= 0, font=("Times New Roman", 10), activebackground= "light blue", activeforeground="black")

        barraMenuPrincipal.add_cascade(label="Archivo", menu=menuArchivo, font=("Times New Roman", 10))
        barraMenuPrincipal.add_cascade(label="Procesos y Consultas", menu= menuProcesosConsultas, font=("Times New Roman", 10))
        barraMenuPrincipal.add_cascade(label="Ayuda", menu= menuAyuda, font=("Times New Roman", 10))
        
        menuArchivo.add_command(label="Aplicación", command=self.mostrarDescripcionSistema)
        menuArchivo.add_command(label="Salir", command=self.mostrarVentanaInicio)

        menuProcesosConsultas.add_command(label = "Sistema Proyecciones", command = self.ingresarFuncionalidad1)
        menuProcesosConsultas.add_command(label="Zona de juegos", command=self.ingresarFuncionalidad4)
        menuProcesosConsultas.add_command(label="Calificaciones", command=self.ingresarFuncionalidad3)
        menuProcesosConsultas.add_command(label="Servicio de comida/souvenir", command= self.ingresarFuncionalidad2)
        menuProcesosConsultas.add_command(label="Sistema de membresías", command=self.ingresarFuncionalidad5)

        menuAyuda.add_command(label="Acerca de", command=self.mostrarNombreAutores)
        menuAyuda.bind('<Leave>', self.avanzarDia) #Easter egg para avanzar el tiempo

    def mostrarDescripcionSistema(self):
         messagebox.showinfo("Información del Sistema", "En este programa puedes:\n•Comprar Tickets\n•Comprar comida y regalos\n•Usar la zona de juegos\n•Adquirir membresias\n•Calificar nuestros servicios")
    
    def mostrarVentanaInicio(self):
        ventanaLogicaProyecto.withdraw()
        ventanaInicio.deiconify()

    def ingresarFuncionalidad1(self):
        FieldFrame.getFramesFuncionalidades()[0].mostrarFrame()
    
    def ingresarFuncionalidad2(self):
        FieldFrame.getFramesFuncionalidades()[1].mostrarFrame()

    def ingresarFuncionalidad3(self):
        FieldFrame.getFramesFuncionalidades()[2].mostrarFrame()    

    def ingresarFuncionalidad4(self): 
        FieldFrame.getFramesFuncionalidades()[3].mostrarFrame()

    def ingresarFuncionalidad5(self):
        FieldFrame.getFramesFuncionalidades()[4].mostrarFrame()

    def mostrarNombreAutores(self):
         messagebox.showinfo("Autores de la Aplicación", "• Juan José Gonzalez Morales - Alias: El Juanjo\n• Edinson Andrés Ariza Mendoza - Alias: Pana Andy\n• Rusbel Danilo Jaramillo Hincapie - Alias: El Indigente\n• Gerson Bedoya Hinestroza - Alias: El viejo Gerson\n• Santiago Castro Herrera - Alias: EL LuisMi")

    def avanzarDia(self, evento):
        #facilitamos el acceso a la sede y creamos una boolean de validación
        sucursalCineActual = FieldFrame.getClienteProceso().getCineUbicacionActual()
        noHayHorariosPresentaciones = True

        #Iteramos sobre cada sala de cine, consultando si tiene horarios de películas en presentación
        for salaCine in sucursalCineActual.getSalasDeCine():
            if salaCine.tieneHorariosPresentacionHoy():
                noHayHorariosPresentaciones = False
                break
        
        if noHayHorariosPresentaciones:
            messagebox.showinfo('Actualización fecha y hora', 'Hemos detectado que han concluido todas las presentaciones del día de hoy, por lo tanto, se pasará al dia siguiente de forma automática. Gracias por su compresión\n')
            sucursalCineActual.setFechaActual((sucursalCineActual.getFechaActual() + timedelta( days = 1 )).replace(hours = 10, minutes = 0, seconds = 0)) #Inicio de la jornada laboral al otro día
    
        sucursalCineActual.avanzarTiempo() #Avanzamos el tiempo y ejecutamos lógica semenal o diaria según el caso
        self.logicaMembresia()
        self.refrescarFramesFuncionalidades() #Actualizamos los frames, ya que se han visto modificados por el avance de tiempo
        print(sucursalCineActual.getFechaActual())
    
    def logicaMembresia(self):
        pass


class FrameZonaJuegos(FieldFrame):
    
    

    def __init__(self):

        self.clienteProceso = FieldFrame.getClienteProceso()
        tituloProceso = 'Zona de Juegos\n'
        descripcionProceso ='En este espacio podras hacer uso de todos nuestros juegos y conseguir recompensas pagando con tu tarjeta cinemar, la cual podras adquirir y recargar en este mismo espacio.\n'
        botonVolver = True
        fecha = f'Fecha Actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}\nHora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)}\n'

        super().__init__(
            tituloProceso = tituloProceso,
            descripcionProceso = descripcionProceso,
            botonVolver = botonVolver  
        )

        #se destruyen todos los widgets creados por el init del padre
        for widget in self.winfo_children():

            widget.destroy()
        
        #se añaden widgets con el uso de canvas para dar mas estetica
        self._imagenFondo = tk.PhotoImage(file = 'src/iuMain/imagenes/ZonaJuegos.png')

        self.canvas =tk.Canvas(self, width=self._imagenFondo.width(), height=self._imagenFondo.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self._imagenFondo)
        
        self.canvas.create_text(320, 100, text=tituloProceso, fill="black", font= ("Showcard Gothic",30))
        self.canvas.create_text(320, 200, text=descripcionProceso, fill="black", font= ("Lucida Console",15, "bold"), width=500)
        self.canvas.create_text(320, 310, text=fecha, fill="black", font= ("Lucida Console",15, "bold"))

        boton1 = tk.Button(self, text="Ingresar", font= ("Lucida Console",15, "bold"), fg = "black", bg = "light blue",command=self.funAceptar, width=12,height=2)
        boton2 = tk.Button(self, text="Volver", font= ("Lucida Console",15, "bold"), fg = "black", bg = "light blue", command=self.funVolver, width=12,height=2)
        
        self.canvas.create_window(230, 380, window=boton1, anchor="center")
        self.canvas.create_window(420, 380, window=boton2, anchor="center")
    
    #Metodo para el boton ingresar
    def funAceptar(self):
        if FieldFrame.getClienteProceso().verificarCuenta():
            FrameTarjetaCinemar().mostrarFrame()
        else: 
            self.AlertaSinCuenta()

    #Metodo para mostrar alerta cuando el cliente no tiene cuenta
    def AlertaSinCuenta(self):

        mensaje = messagebox.askyesno("Sin Cuenta", "•No tienes una Tarjeta Cinemar asociada, ¿Deseas Adquirirla?  🤔 -> 💳❔")

        if mensaje:

            label_ids = [] #lista que almacena los label_ids

            #Se añaden al canvas para simular una cuenta regresiva con el for
            for i in range(5,0,-1):

                label = tk.Label(
                        self, 
                        text="Se le restará el precio de la tarjeta($5000) al saldo de su tarjeta. Redireccionando en " + str(i), 
                        font=("Lucida Console", 11, "bold"), 
                        width=500, 
                        fg="black", 
                        bg="sky blue", 
                        bd=2, 
                        relief="solid",
                        wraplength= 500
                        
                    )
                
                #Se añaden al canvas para simular una cuenta regresiva
                self.canvas.after(1500 * (5 - i), lambda lbl=label: label_ids.append(self.canvas.create_window(320, 450, window=lbl)))


            #Metodos para eliminar los labels creados
            def eliminar_labels():
                for label_id in label_ids:
                    self.canvas.delete(label_id)
                

                Arkade.asociarTarjetaCliente(self.clienteProceso)
                FrameTarjetaCinemar().mostrarFrame(self) 
                print("hola")
            
            self.canvas.after(7500, eliminar_labels)
            
            
               

        else:
            label = tk.Label(
                        self, 
                        text="Recuerda que para Ingresar debes tener una Tarjeta Cinemar", 
                        font=("Lucida Console", 11, "bold"), 
                        width=500, 
                        fg="black", 
                        bg="sky blue", 
                        bd=2, 
                        relief="solid",
                        wraplength= 500
                        
                    )

            label_id = self.canvas.create_window(320, 450, window=label)

            # Usar lambda para eliminar el Label después de 5 segundos
            self.canvas.after(4000, lambda: self.canvas.delete(label_id))
        
class FrameTarjetaCinemar(FieldFrame):
    

    def __init__(self):

        self.clienteProceso = FieldFrame.getClienteProceso()

        super().__init__(
                tituloProceso = 'Personalización Tarjeta Cinemar',
                descripcionProceso = 'En este espacio podras personalizar tu tarjeta cinemar a tu gusto\n',
                tituloCriterios = 'Criterios',
                textEtiquetas = ['Seleccione color de la tarjeta :', 'Seleccione fuente de la tarjeta :', 'Seleccione color de la fuente :'], 
                tituloValores = 'Elecciones',
                infoElementosInteractuables = [
                    [["coral","sky blue","lime green","gold" ,"fuchsia","violet","turquoise"], 'Color de la tarjeta'], 
                    [["Helvetica", "Arial", "Courier New", "Comic Sans MS", "Verdana", "Times New Roman", "Georgia"], 'Fuente de la tarjeta'], 
                    [["salmon", "light sea green", "medium orchid", "pale turquoise", "deep pink", "dodger blue", "light goldenrod yellow"], 'Color de la fuente']
                ],
                habilitado = [False, False, False],
                botonVolver = True
            )
        
        self.widgets = []
        
        for widget in self.winfo_children():

            self.widgets.append(widget)

        self.widgets[2].grid_configure(row=5, column=0)
        self.widgets[3].grid_configure(row=5, column=2)
        self.widgets[4].grid_configure(row=6, column=0)
        self.widgets[5].grid_configure(row=6, column=1)
        self.widgets[6].grid_configure(row=7, column=0)
        self.widgets[7].grid_configure(row=7, column=1)
        self.widgets[8].grid_configure(row=8, column=0)
        self.widgets[9].grid_configure(row=8, column=1)
        self.widgets[10].grid_configure(row=9, column=0, sticky = "we", columnspan = 4)

        self.FrameTarjeta = tk.Frame(self, bg = "black", width=300, height=150)
        self.FrameTarjeta.grid(row =2, rowspan= 3, column= 0, columnspan= 4)

        self.canvas = tk.Canvas(self.FrameTarjeta, width=300, height=150)
        self.canvas.pack()

        # Crear la tarjeta con personalizaciones
        FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)


        for widget in self.widgets[-1].winfo_children():

            widget.config(font= ("Times New Roman", 16, "bold"), width = 9, height = 1, bg = "sky blue", fg = "black")

        tamaños = [24,13,15,15,12,12,12,12,12,12]

        self.widgets[-1].config(bg = "light blue")
        self.widgets.pop(-1)
        
        for i, w in enumerate(self.widgets):
            if isinstance(w, ttk.Combobox):
                pass
            else:
                w.config(font = ("Times New Roman", tamaños[i]), bg = "light blue")

        self.widgets[2].config(font = ("Times New Roman", 16, "bold"))
        self.widgets[3].config(font = ("Times New Roman", 16, "bold"))
        
        ventanaLogicaProyecto.config(bg= "light blue")
        self.config(bg= "light blue")   

    def funAceptar(self):

        valores = []
        if self.evaluarExcepciones():
            for comboBox in self.widgets:
                if isinstance(comboBox, ttk.Combobox):
                    valores.append(comboBox.get())

            if valores[0] != 'Color de la tarjeta':

                self.clienteProceso._colorFondoTarjeta = valores[0]

                FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)
                

            if valores[1] != 'Fuente de la tarjeta':

                self.clienteProceso._fuenteTarjeta = valores[1]

                FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)

            if valores[2] != 'Color de la fuente':

                self.clienteProceso._colorTextoTarjeta = valores[2]

                FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)
                

    def evaluarExcepciones(self):
        try:
            valoresPorDefecto = self.tieneCamposPorDefecto()
            if len(valoresPorDefecto) == 3:
                raise iuDefaultValues(valoresPorDefecto)
            
            return True
        
        except iuExceptions as e:
            messagebox.showerror('Error', e.mostrarMensaje())
            return False

    # Función para crear la tarjeta en un Canvas
    @classmethod
    def crear_tarjeta(cls, canvas, nombre, saldo, color_fondo, fuente_titulo, fuente_texto, color_texto):
        # Tarjeta principal (rectángulo grande)
        canvas.create_rectangle(0, 0, 300, 150, fill=color_fondo, outline="black", width=3)

        # Borde decorativo
        canvas.create_rectangle(5, 5, 295, 145, outline="white", width=2)

        # Título de la tarjeta (con fuente y color personalizados)
        canvas.create_text(150, 30, text="Tarjeta Cinemar", font=fuente_titulo, fill=color_texto)

        # Espacio para el nombre del titular (con fuente y color personalizados)
        canvas.create_text(150, 60, text=f"Nombre: {nombre}", font=fuente_texto, fill=color_texto)

        # Espacio para el saldo (con fuente y color personalizados)
        canvas.create_rectangle(50, 80, 250, 120, fill=color_fondo, outline="black", width=2)
        canvas.create_text(150, 100, text=f"Saldo: {saldo}$", font=fuente_texto, fill=color_texto)

        #Código de barras (simulado)
        for i in range(18):
            # Dibuja cada barra con un ancho de 5 píxeles y espaciado de 10 píxeles
            x1 = 20 + i * 15  # Posición horizontal inicial y espaciado
            x2 = x1 + 5  # Ancho de la barra
            canvas.create_rectangle(x1, 125, x2, 145, fill="black")

#################################################################################################################################

class FrameFuncionalidad1(FieldFrame):
    
    def __init__(self):

        #Definimos los frames a usar durante el desarrollo de la funcionalidad 1
        self._framesFuncionalidad1 = [FrameReservarTicket(self), FrameIngresoASalaCine(self), FrameSalaDeEspera(self)]
        #Facilitamos el acceso al cliente que realiza este proceso
        self._clienteProceso = FieldFrame.getClienteProceso()

        #Usamos el constructor de FieldFrame
        super().__init__(
            tituloProceso = 'Sistema de proyecciones',
            descripcionProceso = f'(Funcionalidad 1) Desde este apartado podrás ingresar a:\n1. Sistema de reservas de ticket\n2. Salas de cine\n3. Sala de espera\n Para acceder a las salas de cine o a la sala de espera, necesitas al menos un ticket cuyo horario de presentación aún no ha sido presentado y, además, fue comprado en esta sucursal (Fecha Actual : {self._clienteProceso.getCineUbicacionActual().getFechaActual().replace(microsecond = 0)})',
            tituloCriterios = 'Criterio proceso',
            textEtiquetas = ['Seleccionar proceso :'],
            tituloValores = 'Dato proceso',
            infoElementosInteractuables = [[['Reservar ticket', 'Ingresar a sala de cine', 'Ingresar a sala de espera'], 'Seleccionar proceso']],
            habilitado = [False],
            botonVolver = True,
            frameAnterior = FieldFrame.getFrameMenuPrincipal()
        )

        #Facilitamos el acceso al elemento interactuable
        self._comoboBoxProceso = self.getElementosInteractivos()[0]
    
    def funAceptar(self):
        #Evaluamos las excepciones
        if self.evaluarExcepciones():

            #Confirmamos la elección del usuario
            confirmarEleccionUsuario = messagebox.askokcancel('Confirmación dato seleccionado', f'Has seleccionado el proceso {self._comoboBoxProceso.get()}, ¿Desea continuar?')
            if confirmarEleccionUsuario:
                
                #Obtenemos el ínidice del criterio seleccionado
                eleccionUsuario = self._comoboBoxProceso.current()
                #Eliminamos los tickets caducados
                self._clienteProceso.dropTicketsCaducados()
                #Creamos una variable que almacenará los tickets para usar según el proceso
                ticketsParaUsar = self._clienteProceso.filtrarTicketsParaSede() if eleccionUsuario == 1 else self._clienteProceso.mostrarTicketsParaSalaDeEspera()

                #En caso de que quiera ingresar a sala de cine o sala de espera
                if eleccionUsuario == 1 or eleccionUsuario == 2:
                    
                    #Verificamos si tiene tickets disponibles para usar
                    if len(ticketsParaUsar) == 0:
                        #Mostramos mensaje de error y finalizamos la ejecución
                        messagebox.showerror('Error', 'No tienes tickets reservados o estos no pertenecen a esta sucursal, para acceder a este proceso debes concluir de forma exitosa al menos un proceso de reserva de ticket')
                        return 
                
                #Ingresamos al frame seleccionado por el usuario
                self._framesFuncionalidad1[eleccionUsuario].mostrarFrame()
     
    #Crear el frame inical de mi funcionalidad (Crear estándar visual frame para ello) (Mas o menos hecho)
    #Separar por módulos la lógica de cada funcionalidad
    #Definir lógica de procesos de pago (Con Gerson)
    #Serializar
    #Hacer Testeos
    #Hacer documentación

class FrameReservarTicket(FieldFrame):
    def __init__(self, frameAnterior):

        #Definimos las variables que usaremos en nuestro proceso
        clienteProceso = FieldFrame.getClienteProceso()

        self._carteleraCliente = Pelicula.filtrarCarteleraPorCliente(clienteProceso)
        self._formatosPeliSeleccionada = None
        self._horariosPeliSeleccionada = None
        self._peliculaProceso = None
        self._horarioProceso = None

        filtroNombresCartelera = Pelicula.filtrarCarteleraPorNombre(self._carteleraCliente)
        filtroPelisRecomendadas = Pelicula.filtarCarteleraPorGenero(self._carteleraCliente, clienteProceso.generoMasVisto())

        #Construimos el frame usando FieldFrame
        super().__init__(
            tituloProceso = 'Reservar ticket',
            descripcionProceso = f'En este espacio solicitamos los datos necesarios para reservar un ticket, debe ingresar los datos de forma secuencial, es decir, en el orden en que se encuentran (Fecha Actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().replace(microsecond = 0)})',
            tituloCriterios = 'Criterios reserva',
            textEtiquetas = ['Seleccionar película :', 'Seleccionar formato :', 'Seleccionar horario :'], 
            tituloValores = 'Valores ingresados',
            infoElementosInteractuables = [
                [Pelicula.mostrarNombrePeliculas(
                    filtroNombrePeliculas = filtroNombresCartelera, 
                    clienteProceso = clienteProceso, 
                    nombrePeliculasRecomendadas = filtroPelisRecomendadas), 'Selecionar película'], 
                [[], 'Seleccionar formato'], 
                [[], 'Seleccionar horario']
            ],
            habilitado = [False, False, False],
            botonVolver = True,
            desplazarBotonesFila = 1,
            frameAnterior = frameAnterior
        )

        #Creamos un Label que almacenará información extra sobre la película seleccionada
        self._labelInfoPeliculaSeleccionada = tk.Label(self, text='', font= ("Verdana",12), anchor="center")
        self._labelInfoPeliculaSeleccionada.grid(column=0, row=len(self._infoEtiquetas) + 3, columnspan=4)

        #Expandimos los comboBox creados para visualizar mejor su contenido
        for elemento in self.getElementosInteractivos():
            elemento.grid_configure(sticky='we')

        #Creamos apuntadores a cada uno de los elementos interactivos para facilitar su acceso
        self._comboBoxPeliculas = self.getElementosInteractivos()[0]
        self._comboBoxFormatos = self.getElementosInteractivos()[1]
        self._comboBoxHorarios = self.getElementosInteractivos()[2]

        #Modificamos el estado de los comboBox para forzar a que se rellene el formulario de forma secuencial
        self._comboBoxFormatos.configure(state = 'disabled')
        self._comboBoxHorarios.configure(state = 'disabled')

        #Definimos la operación respecto al evento de seleccionar un item del comboBox
        self._comboBoxPeliculas.bind('<<ComboboxSelected>>', self.setFormatos)
        self._comboBoxFormatos.bind('<<ComboboxSelected>>', self.setHorarios)

    def setFormatos(self, event):
        #Obtenemos el nombre de la película seleccionada
        nombrePeliculaSeleccionada = self.getValue('Seleccionar película :')

        #Buscamos las películas con el mismo nombre (obtenemos los formatos disponibles de esa película)
        self._formatosPeliSeleccionada = Pelicula.obtenerPeliculasPorNombre(nombrePeliculaSeleccionada, self._carteleraCliente)

        #Configuramos el comboBox de formatos respecto a la información obtenida y lo habilitamos
        self._comboBoxFormatos.configure(values = [peli.getTipoDeFormato() for peli in self._formatosPeliSeleccionada])
        self._comboBoxFormatos.configure(state = 'readonly')
        self._comboBoxFormatos.set(self._infoElementosInteractuables[1][1])

        #Reestablecemos el comboBox de Horarios y el label de información adicional en caso de modificar la película seleccionada nuevamente
        self._comboBoxHorarios.configure(state = 'disabled')
        self._comboBoxHorarios.set(self._infoElementosInteractuables[2][1])

        self._labelInfoPeliculaSeleccionada.configure(text = '')

    def setHorarios(self, event):
        
        #Seleccionamos la película que corresponde al formato seleccionada
        for pelicula in self._formatosPeliSeleccionada:
            if pelicula.getTipoDeFormato() == self.getValue('Seleccionar formato :'):
                self._peliculaProceso = pelicula 

        #Mostramos sus horarios de presentación
        self._horariosPeliSeleccionada = self._peliculaProceso.filtrarHorariosParaMostrar()

        #Configuramos el comboBox de horarios para con la información obtenida y lo habilitamos
        self._comboBoxHorarios.configure(values = self._horariosPeliSeleccionada)
        self._comboBoxHorarios.configure(state = 'readonly')

        #Configuramos el label de información adicional con la película seleciconada
        self._labelInfoPeliculaSeleccionada.configure(text = f'Precio: {self._peliculaProceso.getPrecio()}, Género: {self._peliculaProceso.getGenero()}')
    
    def funBorrar(self):
        #Setteamos los valores por defecto de cada comboBox
        super().funBorrar()

        #Configuramos el estado de los comboBox para que sean seleccionados de forma secuencial
        self._comboBoxHorarios.configure(state = 'disabled')
        self._comboBoxFormatos.configure(state = 'disabled')
        self._labelInfoPeliculaSeleccionada.configure(text = '')
    
    def funAceptar(self):

        #Evaluamos las excepciones de UI
        if self.evaluarExcepciones():
            #Obtenemos el horario seleccionado
            horarioString = self._comboBoxHorarios.get()

            #Evaluamos si es un horario en presentación
            estaEnPresentacion = False
            if horarioString.__contains__('En vivo:'):
                horarioSplit = horarioString.split(':', 1)
                horarioString = horarioSplit[1].lstrip(' ')
                estaEnPresentacion = True

            #Convertimos el horario obtenido de str a datetime
            self._horarioProceso = datetime.strptime(horarioString, '%Y-%m-%d %H:%M:%S')

            #Confirmamos las elecciones del usuario
            confirmacionUsuario = messagebox.askokcancel('Confirmación datos', f'Has seleccionado {self._peliculaProceso.getNombre()}; con formato: {self._peliculaProceso.getTipoDeFormato()}; en el horario: {self._horarioProceso}')

            if confirmacionUsuario:
                #Construimos el frame con la información obtenida y lo mostramos
                FrameSeleccionarAsiento(self._peliculaProceso, self._horarioProceso, estaEnPresentacion, self).mostrarFrame()

class FrameSeleccionarAsiento(FieldFrame):
    def __init__(self, peliculaProceso, horarioProceso, estaEnPresentacion, frameAnterior):
        
        #Guardamos la información obtenida del FrameDeReserva
        self._peliculaProceso = peliculaProceso
        self._horarioProceso = horarioProceso
        self._estaEnPresentacion = estaEnPresentacion

        #Creamos los atributos de instancia que usaremos durante el desarrollo de este frame
        self._asientosPelicula = peliculaProceso.getAsientosSalasVirtuales()[peliculaProceso.getHorariosPresentacion().index(horarioProceso)]
        self._filaSeleccionada = 100
        self._columnaSeleccionada = 100

        super().__init__(
            tituloProceso = 'Selección de asiento',
            descripcionProceso = f'En este apartado seleccionaremos uno de los asientos disponibles para hacer efectivo el proceso de reserva de ticket.\nConsideraciones: \n1. La pantalla se encuentra frente a la fila 1. \n2. Una vez seleccionada una fila (solo se muestran los números de fila con algún asiento disponible) se examinará cuáles son los asientos disponibles en ella, es decir, se debe elegir de forma secuencial, primero fila y luego columna (Fecha actual {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().replace(microsecond = 0)}).',
            tituloCriterios = 'Criterios asiento',
            textEtiquetas = ['Seleccionar fila :', 'Seleccionar columna :'],
            tituloValores = 'Datos asiento',
            infoElementosInteractuables = [[Pelicula.filasConAsientosDisponibles(self._asientosPelicula), 'Selecciona la fila' ], [[], 'Selecciona la columna']],
            habilitado = [False, False],
            botonVolver = True,
            frameAnterior = frameAnterior
        )

        #Asociamos los elementos interactivos a variables para facilitar su acceso
        self._comboBoxFilas = self.getElementosInteractivos()[0]
        self._comboBoxCols = self.getElementosInteractivos()[1]

        #Asignamos sus respectivo estado y eventos
        self._comboBoxCols.configure(state = 'disabled')
        self._comboBoxFilas.bind('<<ComboboxSelected>>', self.setColumnas)

    def setColumnas(self, evento):
        self._filaSeleccionada = int(self._comboBoxFilas.get())

        self._comboBoxCols.configure(values = Pelicula.asientosDisponibles(self._filaSeleccionada, self._asientosPelicula), state = 'readonly')

    def funBorrar(self):
        #Setteamos los valores por defecto de cada comboBox
        super().funBorrar()

        #Configuramos el estado del comboBox de columnas
        self._comboBoxCols.configure(state = 'disabled')
    
    def funAceptar(self):
        #Evaluamos las excepciones de UI
        if self.evaluarExcepciones():
            #Creamos un apuntador al cliente para facilitar su acceso
            clienteProceso = FieldFrame.getClienteProceso()

            #Obtenemos la columna seleccionada
            self._columnaSeleccionada = int(self._comboBoxCols.get())
            
            #Confirmamos la elecicón de datos
            confirmacionUsuario = messagebox.askokcancel('Confirmación datos', f'Has seleccionado el asiento en la fila: {self._filaSeleccionada}; con la columna: {self._columnaSeleccionada}')

            if confirmacionUsuario:
                #Confirmamos ingreso a la pasarela de pagos
                cofirmacionParaPasarelaDePago = messagebox.askokcancel('Confirmación elección datos de reserva', 'Ya hemos concluido la selección de datos necesarios para la reserva de ticket, ahora procederemos a realizar el pago, ¿Desea Continuar?')

                if cofirmacionParaPasarelaDePago:
                    #Construimos el ticket en cuestión
                    ticketProceso = Ticket(self._peliculaProceso, self._horarioProceso, f'{self._filaSeleccionada}-{self._columnaSeleccionada}', clienteProceso.getCineUbicacionActual())

                    #Notificamos al cliente en caso de recibir el descuento
                    if ticketProceso.getPrecio() != self._peliculaProceso.getPrecio():
                        messagebox.showinfo('¡FELICITACIONES!', f'Por ser el cliente número: {clienteProceso.getCineUbicacionActual().getCantidadTicketsGenerados()} has recibido un descuento del {'80%' if self._peliculaProceso.getTipoDeFormato() == '2D' else '50%'}')

                    #Ingresamos a la pasarela de pago
                    pass

class FrameIngresoASalaCine(FieldFrame):
    
    def __init__(self, frameAnterior):
        
        #Facilitamos el acceso al cliente que realiza el proceso de ingreso a la sala de cine
        self._clienteProceso = FieldFrame.getClienteProceso()

        #Creamos variables de instancia
        self._salasDeCineDisponibles = SalaCine.filtrarSalasDeCine(self._clienteProceso.getCineUbicacionActual())
        self._salaCineSelccionada = None

        #Facilitramos el acceso a la información de salas de cine
        infoSalasDeCine = SalaCine.mostrarSalasCine(self._salasDeCineDisponibles, self._clienteProceso)

        #Usamos el constructor de FieldFrame
        super().__init__(
            tituloProceso = 'Ingreso a sala de cine',
            descripcionProceso = f'En este apartado puedes acceder a alguna de nuestras salas de cine disponibles haciendo uso de algún ticket reservado previamente.\nInstrucciones de uso:\n1. Se recomendará la sala de cine a la que puedes ingresar en estos momentos.\n2. Tras seleccionar una sala de cine, podrás ver información detallada sobre ella. \n(Fecha actual: {self._clienteProceso.getCineUbicacionActual().getFechaActual().replace(microsecond = 0)})',
            tituloCriterios = 'Criterios sala cine',
            textEtiquetas = ['Seleccionar sala cine: '],
            tituloValores = 'Salas disponibles',
            infoElementosInteractuables = [[infoSalasDeCine, 'Selecciona la sala de cine']],
            habilitado = [False],
            botonVolver = True,
            desplazarBotonesFila = 1,
            frameAnterior = frameAnterior
        )

        #Creamos un label para mostrar la información de la sala de cine seleccionada
        self._labelInfoSalaCine = tk.Label(self, text='', font= ("Verdana",12), anchor="center")
        self._labelInfoSalaCine.grid(column=0, row=len(self._infoEtiquetas) + 3, columnspan=4)
        
        #Facilitamos el acceso al comboBox creado y le asignamos un evento
        self._comboBoxSalaCine = self.getElementosInteractivos()[0]
        self._comboBoxSalaCine.bind('<<ComboboxSelected>>', self._setInfoSalaCine)

    def _setInfoSalaCine(self, evento):
        #Seleccionamos la sala de cine y seteamos la información de la sala de cine en el Label
        self._salaCineSelccionada = self._seleccionarSalaCine()
        self._labelInfoSalaCine.configure(text = f'Película en presentación: {self._salaCineSelccionada.getPeliculaEnPresentacion().getNombre()}; Formato: {self._salaCineSelccionada.getPeliculaEnPresentacion().getTipoDeFormato()},\nHorario inicio presentación: {self._salaCineSelccionada.getHorarioPeliculaEnPresentacion()}')
    
    def _seleccionarSalaCine(self):
        #Obtenemos el número de sala de cine
        numeroSalaDeCine = int(self._comboBoxSalaCine.get().split('#')[1])
        
        #Iteramos sobre las salas de cine y retornamos la sala de cine coincida con el número de sala obtenido
        for salaCine in self._salasDeCineDisponibles:
            if salaCine.getNumeroSala() == numeroSalaDeCine:
                return salaCine
    
    def funBorrar(self):
        super().funBorrar()
        self._labelInfoSalaCine.configure(text = '')

    def funAceptar(self):
        #Evaluamos las excepciones
        if self.evaluarExcepciones():

            #Confirmamos la elección del usuario
            confirmarEleccion = messagebox.askokcancel('Confirmación dato seleccionado', f'Has seleccionado la sala de cine #{self._salaCineSelccionada.getNumeroSala()}, ¿Es esto correcto?')
            
            if confirmarEleccion:
                #Validamos si puede ingresar a la sala de cine
                if self._salaCineSelccionada.verificarTicket(self._clienteProceso):

                    #Avanzamos la hora respecto a la duración de la película
                    nuevaHoraActual = self._salaCineSelccionada.getHorarioPeliculaEnPresentacion() + self._salaCineSelccionada.getPeliculaEnPresentacion().getDuracion()
                    self._clienteProceso.getCineUbicacionActual().setFechaActual(nuevaHoraActual)
                    self._clienteProceso.getCineUbicacionActual().avanzarTiempo()
                    
                    #Mostramos las ventajas emergentes del proceso realizado y nos redirigimos al menú de la funcionalidad 1
                    messagebox.showinfo('Ingreso exitoso', '¡Disfruta de tu película!')
                    messagebox.showinfo('Proceso exitoso', 'La película ha finalizado, serás redireccionado al menú principal de la funcionalidad')
                    
                    #Actualizamos la lógica de los frames con el nuevo horario seleccionado
                    self.refrescarFramesFuncionalidades()

                    #Regresa al menú de la funcionalidad 1
                    self.getFramesFuncionalidades()[0].mostrarFrame()

                else:
                    messagebox.showerror('Error', 'No tienes un ticket válido para ingresar a esta sala de cine')

class FrameSalaDeEspera(FieldFrame):
    
    def __init__(self, frameAnterior):

        #Facilitamos el acceso a al cliente que está realizando el proceso
        self._clienteProceso = FieldFrame.getClienteProceso()
        #Eliminamos los tickets caducados de la lista de tickets del cliente
        self._clienteProceso.dropTicketsCaducados()

        #Creamos las variables de instancia a usar
        self._ticketsDisponiblesParaUsarEnSede = self._clienteProceso.mostrarTicketsParaSalaDeEspera()
        self._horarioAvanzarTiempo = None

        super().__init__(
            tituloProceso = 'Sala de espera',
            descripcionProceso = f'En este apartado podrás esperar (Avanzar el tiempo) hasta el horario de presentación de la película asociada a alguno de tus tickets previamente adquiridos en esta sede y cuyo horario sea estrictamente mayor a la fecha actual.\nConsideraciones de uso:\n1. Debes seleciconar un ticket para poder visualizar su información\n(Fecha actual: {self._clienteProceso.getCineUbicacionActual().getFechaActual().replace(microsecond = 0)})',
            tituloCriterios = 'Criterio Ticket',
            textEtiquetas = ['Seleccionar ticket :'],
            tituloValores = 'Dato ticket',
            infoElementosInteractuables = [ [[f'Horario: {ticket.getHorario()}' for ticket in self._ticketsDisponiblesParaUsarEnSede], 'Seleccionar ticket'] ],
            habilitado = [False],
            botonVolver = True,
            desplazarBotonesFila = 1,
            frameAnterior = frameAnterior
        )

        #Expandimos el comboBox creado para visualizar mejor su contenido
        self.getElementosInteractivos()[0].grid_configure(sticky='we')

        #Creamos y ubicamos el label que mostrará información sobre el ticket seleccionado
        self._labelInfoTicketSeleccionado = tk.Label(self, text='', font= ("Verdana",12), anchor="center")
        self._labelInfoTicketSeleccionado.grid(column=0, row=len(self._infoEtiquetas) + 3, columnspan=4)

        #Facilitamos el acceso al comboBox de tickets y le asignamos un evento
        self._comboBoxTicketsDisponibles = self.getElementosInteractivos()[0]
        self._comboBoxTicketsDisponibles.bind('<<ComboboxSelected>>', self._setInfoTicket)
    
    def _setInfoTicket(self, evento):

        #Obtenemos el horario seleccionado a partir del ticket seleccionado
        ticketSeleccionado = self._ticketsDisponiblesParaUsarEnSede[self._comboBoxTicketsDisponibles.current()]
        self._horarioAvanzarTiempo = ticketSeleccionado.getHorario()

        #Actualizamos la información del label de información de ticket seleccionado
        self._labelInfoTicketSeleccionado.configure(text = f'Película: {ticketSeleccionado.getPelicula().getNombre()}; Formato: {ticketSeleccionado.getPelicula().getTipoDeFormato()},\nSala de cine número: {ticketSeleccionado.getSalaDeCine().getNumeroSala()}')
    
    def funBorrar(self):
        #Seteamos los valores por defecto
        super().funBorrar()
        #Reestablecemos la información del label de información de ticket seleccionado
        self._labelInfoTicketSeleccionado.configure(text = '')
    
    def funAceptar(self):
        
        #Evaluamos las excepciones
        if self.evaluarExcepciones():

            #Confirmamos la elección del usuario
            confirmacionUsuario = messagebox.askquestion('Adevertencia', f'(Fecha actual: {self._clienteProceso.getCineUbicacionActual().getFechaActual().replace(microsecond = 0)}) Estas apunto de esperar (Avanzar el tiempo) hasta {self._horarioAvanzarTiempo}, en caso de tener tickets antes de la fecha y hora a esperar, estos serán eliminados, ¿Desea continuar?')

            if confirmacionUsuario:
                #Avanzamos el tiempo y notificamos al usuario
                self._clienteProceso.getCineUbicacionActual().setFechaActual(self._horarioAvanzarTiempo)
                messagebox.showinfo('Avance de tiempo exitoso', f'Fecha actual: {self._horarioAvanzarTiempo}')
                self._clienteProceso.getCineUbicacionActual().avanzarTiempo()

                #Actualizamos la lógica de los frames con el nuevo horario seleccionado
                self.refrescarFramesFuncionalidades()

                #Regresa al menú de la funcionalidad 1
                self.getFramesFuncionalidades()[0].mostrarFrame()

#################################################################################################################################

class FrameFuncionalidad3Calificaciones(FieldFrame):
    def __init__(self):
        self._clienteProceso = FieldFrame.getClienteProceso()
        self._peliculasCalificar = self._clienteProceso.getPeliculasDisponiblesParaCalificar()
        self._productosCalificar = self._clienteProceso.getProductosDisponiblesParaCalificar()
        

        super().__init__ (
            tituloProceso="Calificaciones",
            descripcionProceso= f"Bienvenido al apartado de califcaciones de productos y peliculas, en este espacio podras calificar nuestros servicios dependiendo tus gustos y aficiones.(Fecha Actual: {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}; Hora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)})",
            tituloCriterios = 'Criterios para calificar',
            textEtiquetas= ["Que quieres calificar :","Escoge tu item :" ,  "Califica tu item :"],
            tituloValores = 'Valores ingresados',
            infoElementosInteractuables = [
                [["Producto","Pelicula"], 'Seleccionar una opcion'],
                [[], 'Escoge tu item:'],                         
                [[], 'Califica tu item:'] 
            ],

            habilitado = [False, False, False],
            botonVolver = True,
            frameAnterior = FieldFrame.getFrameMenuPrincipal()
            
        )

        self._comboBoxItems = self.getElementosInteractivos()[0]
        self._comboBoxEscogerItem = self.getElementosInteractivos()[1]
        self._comboBoxCalificarItem = self.getElementosInteractivos()[2]

        self._comboBoxEscogerItem.configure(state = 'disabled')
        self._comboBoxCalificarItem.configure(state = 'disabled')

        self._comboBoxItems.bind('<<ComboboxSelected>>', self.setMostrarItemParaCalificar)
        self._comboBoxEscogerItem.bind('<<ComboboxSelected>>', self.setCalificarItem)


    def setMostrarItemParaCalificar(self,evento):
        
        if self._comboBoxItems.current() == 0:

       
            self._comboBoxEscogerItem.configure(values = Cliente.mostrarProductosParaCalificar(self._productosCalificar))
            self._comboBoxEscogerItem.configure(state = 'readonly')
            self._comboBoxEscogerItem.set(self._infoElementosInteractuables[1][1])

        
            self._comboBoxCalificarItem.configure(state = 'disabled')
            self._comboBoxCalificarItem.set(self._infoElementosInteractuables[2][1])

            

        else:
            
            self._comboBoxEscogerItem.configure(values = Cliente.mostrarPeliculaParaCalificar(self._peliculasCalificar))
            self._comboBoxEscogerItem.configure(state = 'readonly')
            self._comboBoxEscogerItem.set(self._infoElementosInteractuables[1][1])

        
            self._comboBoxCalificarItem.configure(state = 'disabled')
            self._comboBoxCalificarItem.set(self._infoElementosInteractuables[2][1])

           

    def setCalificarItem(self,evento):

        calificacionesLista= [1,2,3,4,5]
        self._comboBoxCalificarItem.configure(values = calificacionesLista)
        self._comboBoxCalificarItem.configure(state = 'readonly')
        nombreProductoSeleccionado = self.getValue("Escoge tu item :")

    def funBorrar(self):
        #Setteamos los valores por defecto de cada comboBox
        super().funBorrar()

        #Configuramos el estado del comboBox de columnas
        self._comboBoxEscogerItem.configure(state = 'disabled')  
        self._comboBoxCalificarItem.configure(state = 'disabled')    
           

    def funAceptar(self):
         if self.evaluarExcepciones():
            #Obtenemos el horario seleccionado
            horarioString = self._comboBoxHorarios.get()

            #Evaluamos si es un horario en presentación
            estaEnPresentacion = False
            if horarioString.__contains__('En vivo:'):
                horarioSplit = horarioString.split(':', 1)
                horarioString = horarioSplit[1].lstrip(' ')
                estaEnPresentacion = True


            if self._comboBoxItems.current() == 0: 
                self._productoSeleccionado = Producto.obtenerProductosPorNombre(nombreProductoSeleccionado, self._clienteProceso.getCineUbicacionActual().getInventarioCine)
                nombrePeliculaSeleccionada = self.getValue("Escoge tu item :")

            else:
                indicePeliculaSeleccionada=  self._comboBoxEscogeritem
                self._formatosPeliSeleccionada = Pelicula.obtenerPeliculasPorNombre(nombrePeliculaSeleccionada, self._clienteProceso.getCineUbicacionActual().getCartelera())    



        
     
    #Programar el borrar para que los values de los combobox queden vacíos o investigar forma de que los combobox no desplieguen el menú
    #Hacer que en el comboBox de horarios se muestre un apartado de horario de presentación en vivo, programar método en clase película
     

class FrameFuncionalidad5(FieldFrame):

    def __init__(self):
        clienteProceso = FieldFrame.getClienteProceso()
        super().__init__(
            tituloProceso=f"Sistema de membresías.",
            descripcionProceso= f"(Fecha Actual: {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}; Hora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)}) \n {Membresia.verificarMembresiaActual(clienteProceso)}",
            textEtiquetas=[""],
            infoElementosInteractuables= [[Membresia.mostrarCategoria(clienteProceso, clienteProceso.getCineUbicacionActual()), "Seleccione membresía"]],
            habilitado= [False]
        )

    def funAceptar(self):
        FieldFrame.getFramePasarelaDePagos().mostrarFrame()

class FramePasarelaDePagos(FieldFrame):

    def __init__(self):
        
        super().__init__(
            tituloProceso=f"Métodos de pago",
            descripcionProceso=f"(Fecha Actual: {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}; Hora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)})",
            textEtiquetas=[""],
            infoElementosInteractuables=[None],
            habilitado=[False]
        )

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
    

    cliente1 = Cliente("Rusbel", 18, 13434, TipoDocumento.CC, sucursalCine2)
    cliente2 = Cliente("Andy", 18, 14343, TipoDocumento.CC, sucursalCine1)
    cliente3 = Cliente('Gerson', 23, 98765, TipoDocumento.CC, sucursalCine3)
    cliente4 = Cliente('Juanjo', 18, 987, TipoDocumento.CC, sucursalCine1)
    cliente5 = Cliente('Santiago', 18, 1125274009, TipoDocumento.CC, sucursalCine3)

    producto2b = Producto("Hamburguesa","Grande","comida",0,1,"Normal",sucursalCine2)
    bono1 = Bono(1234,producto2b,"comida",cliente1)
    producto1b = Producto("Camisa","XL","souvenir",0,1,"Normal",sucursalCine2)
    bono2 = Bono(1234,producto1b,"souvenir",cliente1)
    bono3 = Bono(1234,producto2b,"comida",cliente1)
    

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
    cliente5.getPeliculasDisponiblesParaCalificar().append(pelicula1_2)
    cliente5.getProductosDisponiblesParaCalificar().append(producto7)
    cliente5.getPeliculasDisponiblesParaCalificar().append(pelicula1_3)
    cliente5.getProductosDisponiblesParaCalificar().append(producto5)

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

    Membresia.stockMembresia(SucursalCine.getSucursalesCine())

    for sucursal in SucursalCine.getSucursalesCine():
        for i in range (10):
            sucursal.getTarjetasCinemar().append(TarjetaCinemar())
    
    #print(len(sucursalCine1.getTarjetasCinemar()), len(sucursalCine2.getTarjetasCinemar()), len(sucursalCine1.getTarjetasCinemar()) ) 

    SucursalCine.logicaInicioSIstemaReservarTicket()

    ticket = Ticket(pelicula1_2, datetime(2024, 9, 15, 12, 20, 0), '4-4', sucursalCine1)
    ticket.setSucursalCompra(sucursalCine1)
    ticket.setSalaDeCine(salaDeCine1_1)
    cliente2.getTickets().append(ticket)

    #cliente4.setCuenta(SucursalCine.getSucursalesCine()[0].getTarjetasCinemar()[0])


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


    # Función para cambiar la imagen cuando el mouse sale
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
    imagenLabel = tk.Button(frameInferiorIzquierdoP4, image= imagenes[indice_imagen], command = ingresarVentanaPrincipal, bd = 1, relief = "solid", bg = "#ADD8E6")
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




                 