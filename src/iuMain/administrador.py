import tkinter as tk

if __name__ == '__main__':

    #Creacion de la ventana de inicio 
    ventanaInicio = tk.Tk()
    ventanaInicio.title("Ventana de Incio Cinemar")
    ventanaInicio.geometry("500x450")
    ventanaInicio.config(bg = "light gray")

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
        ventanaInicio.destroy()
        #Creacion de la ventana Principal
        ventanaPrincipal = tk.Tk()
        ventanaPrincipal.title("Ventana Principal Cinemar")
        ventanaPrincipal.geometry("500x450")
        ventanaPrincipal.mainloop

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



    ventanaInicio.mainloop()

