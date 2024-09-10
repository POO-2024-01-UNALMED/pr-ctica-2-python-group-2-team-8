import sys
import os

# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk
from gestionAplicacion.usuario.tipoDocumento import TipoDocumento
from gestionAplicacion.sucursalCine import SucursalCine

class FieldFrame(tk.Frame):

    def __init__(self, tituloProceso = "", tituloCriterios = "", textEtiquetas = None, tituloValores = "", elementosInteractuables = None, habilitado = None):
        super().__init__(ventanaLogicaProyecto)
        self._tituloProceso = tituloProceso
        self._tituloCriterios = tituloCriterios
        self._infoEtiquetas = textEtiquetas
        self._tituloValores = tituloValores
        self._infoElementosAñadidos = elementosInteractuables
        self._habilitado = habilitado

        self._elementosInteractivos = []
        
        tituloFrame = tk.Label(self, text=tituloProceso, font= ("Verdana bold",30), anchor="center")
        tituloFrame.grid(row=0, column=0, columnspan=4, sticky='nswe')

        tituloCrit = tk.Label(self, text = tituloCriterios, font= ("Verdana bold",15), anchor="center")
        tituloCrit.grid(column=0, row=1, padx = (10,10), pady = (10,10))

        tituloVal = tk.Label(self, text = tituloValores, font= ("Verdana bold",15), anchor="center")
        tituloVal.grid(column=1, row=1,columnspan=3, padx = (10,10), pady = (10,10))

        for i in range(len(textEtiquetas)):

            labelCriterio = tk.Label(self, text = textEtiquetas[i], font= ("Verdana",12), anchor="center")
            labelCriterio.grid(column=0, row=i+2, padx = (10,10), pady = (10,10))

            elementoInteractivo = None

            if elementosInteractuables[i] is None:
                elementoInteractivo = tk.Entry(self)
            
            elif len(elementosInteractuables[i]) == 1:
                elementoInteractivo = tk.Entry(self, textvariable=tk.StringVar(str(elementosInteractuables[i][0])))
            else:
                elementoInteractivo = ttk.Combobox(self, values=elementosInteractuables[i][0])
                elementoInteractivo.set(elementosInteractuables[i][1])


            elementoInteractivo.grid(column=1, row=i+2,columnspan=3, padx = (10,10), pady = (10,10))

            if habilitado is not None and not habilitado[i]:

                if isinstance(elementoInteractivo, ttk.Combobox):
                    elementoInteractivo.configure(state='readonly')
                else:
                    elementoInteractivo.configure(state='disabled')

            self._elementosInteractivos.append(elementoInteractivo)

        tk.Button(self, text="Borrar", font = ("Verdana", 12), fg = "white", bg = "gray",command=self.funBorrar,
        width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 1, row = len(self._infoEtiquetas)+2, columnspan=3)
        tk.Button(self, text="Aceptar", font = ("Verdana", 12), fg = "white", bg = "gray", command=self.funAceptar,
        width=12,height=2).grid(pady = (10,10),
        padx=(10,10), column = 0, row = len(self._infoEtiquetas)+2)

    def getValue(self, criterio):
        indice = self._infoEtiquetas.index(criterio)
        return self._elementosInteractivos[indice].get()

    def setValueEntry(self, criterio, valor):
        indice = self._infoEtiquetas.index(criterio)
        self._elementosInteractivos[indice].delete("0","end")
        self._elementosInteractivos[indice].insert(0, valor)
    
    def setValueComoboBox(self, criterio):
        indice = self._elementosInteractivos.index(criterio)
        criterio.set(self._infoElementosAñadidos[indice][1])

    def funBorrar(self):
        for elementoInteractivo in self._elementosInteractivos:
            if isinstance(elementoInteractivo, ttk.Combobox):
                self.setValueComoboBox(elementoInteractivo)
            else:
                elementoInteractivo.delete("0","end")
    
    def mostrarFrame(self):
        self.pack(expand=True)
                
class FrameInicioSesion(FieldFrame):

    def __init__(self):
        super().__init__(
            tituloProceso = 'Iniciar Sesión',
            tituloCriterios = "Criterios Ingreso", 
            textEtiquetas = ['Seleccionar Tipo D.I. :', 'Número D.I. :', 'Sucursal visita'], 
            tituloValores = "Datos Ingreso", 
            elementosInteractuables = [[TipoDocumento.listadoTiposDeDocumentos(), 'Seleccionar D.I.'], None, [SucursalCine.getSucursalesCine(), 'Seleccionar Sucursal']], 
            habilitado = [False, True, False]
        )
    
    def funAceptar(self):
        pass
        
       
if __name__ == '__main__':
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
        ventanaInicio.withdraw()
        ventanaLogicaProyecto.deiconify()
        frameIniciarSesion.mostrarFrame()

        #Creacion de la ventana Principal
        #ventanaPrincipal = tk.Tk()
        #ventanaPrincipal.title("Ventana Principal Cinemar")
        #ventanaPrincipal.geometry("500x450")
        #ventanaPrincipal.mainloop

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

