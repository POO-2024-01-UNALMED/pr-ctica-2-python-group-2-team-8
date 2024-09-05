import tkinter as tk

#Creacion de la ventana
ventanaInicio = tk.Tk()
ventanaInicio.title("Ventana de Incio Cinemar")
ventanaInicio.geometry("500x450")

#Creacion y empaquetacion de P1 (237.5x432)
frameGrandeIzquierdoP1 = tk.Frame(ventanaInicio, bd = 2, relief= "solid")
frameGrandeIzquierdoP1.pack(side = "left", padx = 5, pady = 5, expand = True, fill = "both")

#Creacion y empaquetacion de P2
frameGrandeDerechoP2 = tk.Frame(ventanaInicio, bd = 2, relief= "solid")
frameGrandeDerechoP2.pack(side = "right", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y empaquetacion de P3
frameSuperiorIzquierdoP3 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid")
frameSuperiorIzquierdoP3.pack(side = "top", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y empaquetacion de P4
frameInferiorIZquierdoP4 = tk.Frame(frameGrandeIzquierdoP1, bd = 2, relief= "solid", height= 100)
frameInferiorIZquierdoP4.pack(side = "bottom", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y empaquetacion de P5
frameSuperiorDerechoP5 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid")
frameSuperiorDerechoP5.pack(side = "top", padx = 5, pady = 5, expand = True, fill= "both")

#Creacion y empaquetacion de P6
frameInferiorDerechoP6 = tk.Frame(frameGrandeDerechoP2, bd = 2, relief= "solid", height= 100)
frameInferiorDerechoP6.pack(side = "bottom", padx = 5, pady = 5, expand = True, fill= "both")


#Creacion de la barra de menu
barraMenu = tk.Menu(ventanaInicio)
ventanaInicio.config(menu = barraMenu)

menuOpciones = tk.Menu(barraMenu, tearoff= 0, font=("Times New Roman", 10))
barraMenu.add_cascade(label= "Inicio", menu= menuOpciones)
    
menuOpciones.add_command(label = "Descripción del programa")
menuOpciones.add_command(label = "Salir y Guardar")

ventanaInicio.mainloop()
