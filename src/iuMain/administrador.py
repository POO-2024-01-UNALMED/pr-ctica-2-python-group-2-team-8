import tkinter as tk

#Creacion de la ventana
ventanaInicio = tk.Tk()
ventanaInicio.title("Ventana de Incio Cinemar")
ventanaInicio.geometry("500x450")

#Nota: Si desean usar pack(No recomendado, se buguea con el uso de texto dentro del frame) 
# en vez de place ponganle a los frames el fill = "both" pa que se vea melo

#Creacion y posicionamiento de P1 (237.5x432)
frameGrandeIzquierdoP1 = tk.Frame(ventanaInicio, bd = 2, relief= "solid")
frameGrandeIzquierdoP1.place(relx= 0.015, rely= 0.02, relwidth= 0.475, relheight = 0.96)
#frameGrandeIzquierdoP1.pack(side = "left", padx = 5, pady = 5, expand = True,)

#Creacion y posicionamiento de P2
frameGrandeDerechoP2 = tk.Frame(ventanaInicio, bd = 2, relief= "solid")
frameGrandeDerechoP2.place(relx= 0.51, rely= 0.02, relwidth= 0.475, relheight = 0.96)
#frameGrandeDerechoP2.pack(side = "right", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y posicionamiento de P3
frameSuperiorIzquierdoP3 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid")
frameSuperiorIzquierdoP3.place(relx= 0.02, rely= 0.011, relwidth= 0.96, relheight = 0.37)
#frameSuperiorIzquierdoP3.pack(side = "top", padx = 5, pady = 5, expand = True, fill= "both")
mensajeBienvenida = tk.Label(frameSuperiorIzquierdoP3, text= "Bienvenido a Cinemar", bd= 2, font= ("Times New Roman", 16, "bold"), fg= "red", relief= "groove", cursor="heart")
mensajeBienvenida.pack(anchor= "c", expand=True)

#Creacion y posicionamiento de P4
frameInferiorIZquierdoP4 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid", height= 100)
frameInferiorIZquierdoP4.place(relx= 0.02, rely= 0.392, relwidth= 0.96, relheight = 0.597)
#frameInferiorIZquierdoP4.pack(side = "bottom", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y posicionamineto de P5
frameSuperiorDerechoP5 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid")
frameSuperiorDerechoP5.place(relx= 0.02, rely= 0.011, relwidth= 0.96, relheight = 0.37)
#frameSuperiorDerechoP5.pack(side = "top", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y posicionamiento de P6
frameInferiorDerechoP6 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid", height= 100)
frameInferiorDerechoP6.place(relx= 0.02, rely= 0.392, relwidth= 0.96, relheight = 0.597)
#frameInferiorDerechoP6.pack(side = "bottom", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion de la barra de menu
barraMenu = tk.Menu(ventanaInicio, font=("Times New Roman", 14))
ventanaInicio.config(menu = barraMenu)

menuOpciones = tk.Menu(barraMenu, tearoff= 0, font=("Times New Roman", 12))
barraMenu.add_cascade(label= "Inicio", menu= menuOpciones, font=("Times New Roman", 12) )


#Metodos para la barra de opciones
def mostrarDescripcion(): 
    mensaje = tk.Message(frameSuperiorIzquierdoP3, text=  "En este programa puedes:\n•Comprar Tickets\n•Comprar comida y regalos\n•Usar la zona de juegos\n•Adquirir membresias\n•Calificar nuestros servicios" , font= ("Times New Roman",11))
    mensaje.pack(anchor= "s", expand= True)

def CerrarVentana():
    ventanaInicio.destroy()

#Opciones de el menu de inicio
menuOpciones.add_command(label = "Descripción del programa", command= mostrarDescripcion)
menuOpciones.add_command(label = "Salir y Guardar", command= CerrarVentana)



ventanaInicio.mainloop()
