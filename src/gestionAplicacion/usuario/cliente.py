#Metodos

#Description: Este metodo se encarga de mostrar el historial de peliculas que cada cliente ha visto hasta el momento para poder 
#hacer una calificacion en concreto de las peliculas que el cliente se vio, evitando que el cliente pueda calificar 
#una pelicula que no haya visto.

def mostrar_pelicula_para_calificar(peliculas_disponibles_para_calificar):
    peliculas = ""
    for i, pelicula in enumerate(peliculas_disponibles_para_calificar, start=1):
        if peliculas:
            peliculas += "\n"
        peliculas += f"{i}. {pelicula.nombre} {pelicula.tipo_de_formato}"
    return peliculas
    
#Description:Este metodo se encarga de mostrar el historial de comida que cada cliente ha consumido hasta el momento
# para poder  hacer una calificacion en concreto de los productos que el cliente cosnumio, evitando que el cliente pueda calificar 
#un producto que no haya consumido.

def mostrar_productos_para_calificar(productos_disponibles_para_calificar):
    pedidos = ""
    for i, producto in enumerate(productos_disponibles_para_calificar, start=1):
        if pedidos:
            pedidos += "\n"
        pedidos += f"{i}. {producto.nombre} {producto.tamaño}"
    return pedidos