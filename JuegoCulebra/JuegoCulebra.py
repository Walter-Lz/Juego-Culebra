import random
from tkinter import  Tk, Frame, Canvas, Button,Label,ALL
import time
'''
   
    Walter Lazo González
   
    
'''
def obtener_vecinos_validos(posicion, obstaculos):
    x, y = posicion
    max_filas = 18
    max_columnas = 20
    vecinos = []
    # Arriba
    if x - 1 >= 0 and (x - 1, y) not in obstaculos:
        vecinos.append((x - 1, y))
    # Abajo
    if x + 1 < max_filas and (x + 1, y) not in obstaculos:
        vecinos.append((x + 1, y))
    # Izquierda
    if y - 1 >= 0 and (x, y - 1) not in obstaculos:
        vecinos.append((x, y - 1))
    # Derecha
    if y + 1 < max_columnas and (x, y + 1) not in obstaculos:
        vecinos.append((x, y + 1))
    return vecinos

def obtener_vecinos_ordenados(posicion, objetivo, obstaculos):
    x_objetivo, y_objetivo = objetivo
    vecinos = obtener_vecinos_validos(posicion, obstaculos)
    return sorted(vecinos, key=lambda vecino: abs(vecino[0] - x_objetivo) + abs(vecino[1] - y_objetivo))

def buscar_camino(posicion_actual, objetivo, obstaculos, ruta_actual):
    if posicion_actual == objetivo:
        return ruta_actual

    def sin_vecino_en_ruta(vecino):
        return vecino not in ruta_actual

    vecinos_ordenados = obtener_vecinos_ordenados(posicion_actual, objetivo, obstaculos)
    nuevos_vecinos = filter(sin_vecino_en_ruta, vecinos_ordenados)  

    nuevas_rutas = map(lambda vecino: buscar_camino(vecino, objetivo, obstaculos, ruta_actual + [vecino]), nuevos_vecinos)
    nueva_ruta = next(filter(None, nuevas_rutas), None)
    return nueva_ruta if nueva_ruta is not None else None

def busquedaProfundidad(posicion_inicial, objetivo, obstaculos):
    return buscar_camino(posicion_inicial, objetivo, obstaculos, [posicion_inicial])

def generarOBjetivo_clic(event):
    global posicion_objetivo, idObjetivo,cantidadObjetivos, Culebra_Movimiento
    if(Juego_Iniciado!=False):
        # coordenadas del clic
        xEV = event.x
        yEV = event.y
        #ajustar dentro de la ventana del juego
        xVentana = ((xEV + 15) // 30) * 30 + 15
        yVentana = ((yEV + 15) // 30) * 30 + 15
        #ajustar los valores en la lista 
        y = ((xEV + 15) // 30) 
        x = ((yEV + 15) // 30)
        if x < 0 or x >= 18 or y < 0 or y >= 20:
            print("Coordenadas fuera de los límites de la matriz.")
            return
        if (x,y) not in posicion_objetivo and (x,y) not in posicion_Obstaculos: # si se repite las coordenadas eliminamos 
            if idObjetivo<cantidadObjetivos: 
                posicion_objetivo.append((x,y)) # agregando a la lista de objetivos
                idObjetivo += 1
                tag_name = f"Objetivo_{idObjetivo}"
                canvas.create_text((xVentana, yVentana), text='❤', fill='aqua', 
                                        font=('Arial', 18), tag=tag_name) # Agregar una etiqueta para cada objetivo
                print("Se ha agregado un nuevo objetivo---->", (x,y))
            else:
                print("Maxima capacidad de objetivos alcanzados: ", idObjetivo)
        else:
            print("No se puede colocar en la coordenada",(x,y))       
             
def generarObstaculos():
    global posicion_Obstaculos
    #Funcion para generar obstaculos en la  matriz
    cantidadObstaculos= random.randint(6,10)  
    for i in range(cantidadObstaculos):
        Coordenada_ObstaculoX= (random.randint(0,560)) 
        Coordenada_ObstaculoY= (random.randint(0,460))
        xVentanaObstaculo = ((Coordenada_ObstaculoX + 15) // 30) * 30 + 15  # coordenadas para la ventana
        yVentanaObstaculo = ((Coordenada_ObstaculoY + 15) // 30) * 30 + 15
        paresOrdenados= (xVentanaObstaculo,yVentanaObstaculo)
        tag_nameObstaculo = f"Obstaculo{i}"
        if canvas.find_withtag(tag_nameObstaculo):
            print("Las Coordenadas coinciden con un Obstaculo ya agregado.")
        else:
            x=((Coordenada_ObstaculoY + 15) // 30)  #coordenadas para la lista
            y= ((Coordenada_ObstaculoX + 15) // 30)
            if(x,y) == (0,0)or (x,y)==(1,0):
                x+=1
            canvas.create_text(*paresOrdenados, text='💥', fill='red', 
                            font=('Arial', 18), tag=tag_nameObstaculo) # Agregar una etiqueta para cada obstaculo
            posicion_Obstaculos.append((x,y))
    print("Cantidad de obstaculos definidos. ", cantidadObstaculos)
    print("Lista obstaculos: ",posicion_Obstaculos)
    
def dibujar_ruta_Culebra(ruta, objetivoCulebra, index=0):
    global posicion_culebra, objetivosCompletados, Culebra_Movimiento, posicion_objetivo
    if index < len(ruta):   
        x, y = ruta[index]
        x_pixel = ((y * 30) + 15)
        y_pixel = ((x * 30) + 15)
        # Mover la cabeza de la culebra a la nueva posición
        canvas.coords('cabeza', x_pixel, y_pixel)
        posicion_culebra = (x, y)
        tag_name = canvas.find_closest(x_pixel, y_pixel)  # Buscamos el objeto más cercano a las coordenadas
        tags = canvas.itemcget(tag_name, 'tags')
        for tag in tags.split():
            if tag.startswith('Objetivo_'):
                canvas.delete(tag_name)   # Elimina el objetivo del canvas
                objetivosCompletados += 1
                cantidad['text'] = 'Objetivos ❤ : {}'.format(objetivosCompletados)
                if (x,y) in posicion_objetivo:
                    posicion_objetivo.remove((x,y))
                Culebra_Movimiento = False
                break  # Salir del bucle una vez que se ha encontrado y eliminado el objetivo
    ventana.after(200, dibujar_ruta_Culebra, ruta, objetivoCulebra, index + 1)

def movimientos():
    global posicion_objetivo, posicion_culebra,posicion_Obstaculos, inicio_tiempo, Juego_Iniciado,Culebra_Movimiento,cantidadObjetivos,movimientosEjecutados
    if inicio_tiempo is None:
        xCulebra,yCulebra= posicion_culebra
        canvas.create_text(((xCulebra * 30) + 15),((yCulebra * 30) + 15) ,text= '▀', fill='white', 
            font = ('Arial',20), tag ='cabeza')
        Juego_Iniciado= True
        generarObstaculos()
        inicio_tiempo = time.time()
        
    if Juego_Iniciado == True:
        actualizar_temporizador()
        if posicion_objetivo != [] and Culebra_Movimiento == False:    # Siempre que haya un objetivo y la culebra no este ya en movimiento se hace busqueda.
            nuevoObjetivo= posicion_objetivo[0]
            posicion_objetivo.pop(0)
            Ruta_Culebra =busquedaProfundidad(posicion_culebra,nuevoObjetivo,posicion_Obstaculos)
            if Ruta_Culebra != None:  
                Culebra_Movimiento= True
                print("Objetivo----> ", nuevoObjetivo)
                print("Ruta elejida----> ", Ruta_Culebra)
                movimientosEjecutados =len(Ruta_Culebra)-1
                MovimientosRealizados_Culebra['text'] = 'Movimiento: {}'.format(movimientosEjecutados)
                dibujar_ruta_Culebra(Ruta_Culebra,nuevoObjetivo)
            else:
                print("No se puede  llegar al Objetivo: ",nuevoObjetivo)
                cantidadObjetivos -= 1
                
        if objetivosCompletados==cantidadObjetivos:
            FinalJuego()  
        ventana.after(200,movimientos)   
    
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    x_ventana = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_ventana = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry('{}x{}+{}+{}'.format(ancho_ventana, alto_ventana, x_ventana, y_ventana))   
        
def actualizar_temporizador():
    tiempo_transcurrido = int(time.time() - inicio_tiempo)
    temporizador.config(text=f'Tiempo: {tiempo_transcurrido} sg')
    if Juego_Iniciado == True:
        ventana.after(1000, actualizar_temporizador) 

def FinalJuego():
    global Juego_Iniciado
    Juego_Iniciado=False
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 
        text=f"-> Fin del Juego <- \n\n        🔶🔸🔷🔹",fill='aqua',
        font=('Arial',35,'bold'))
  
def salir ():
    ventana.destroy()
    ventana.quit()

if __name__=='__main__':
    posicion_objetivo= []    # lista de objetivos con sus coordenadas
    posicion_Obstaculos= []
    posicion_culebra = (0,0)
    cantidadObjetivos=8     # Cantidad de objetivos  a completar para ganar el juego
    idObjetivo=0
    objetivosCompletados=0
    movimientosEjecutados=0
    Juego_Iniciado = False
    inicio_tiempo = None # Se inicializa cuando se comienza el juego
    Culebra_Movimiento= False
    ventana = Tk()
    ventana.config(bg='black')
    ventana.title('Juego Culebra')
    # Calculamos el tamaño de la ventana para que se ajuste a la matriz
    canvas_Ancho = 20 * 30  # Ancho de la matriz (20 columnas)
    canvas_Altura = 18 * 30  # Alto de la matriz (18 filas)
    window_Ancho= canvas_Ancho + 10  # Añadimos un pequeño margen 
    window_Altura = canvas_Altura + 35  # Añadimos un pequeño margen
    ventana.geometry(f"{window_Ancho}x{window_Altura}")
    ventana.resizable(0,0)

    frame_1 = Frame(ventana, width=canvas_Ancho, height=25, bg='black')
    frame_1.grid(column=0, row=0)
    frame_2 = Frame(ventana, width=canvas_Ancho, height=canvas_Altura, bg='black')
    frame_2.grid(column=0, row=1)
    canvas = Canvas(frame_2, bg='black', width=canvas_Ancho, height=canvas_Altura)
    canvas.bind("<Button-1>", generarOBjetivo_clic)
    canvas.pack()
    # Se pinta el rectangulo
    for i in range(0,canvas_Altura,30): 
        for j in range(0,canvas_Ancho,30):
            canvas.create_rectangle(j,i,j+30, i+30, fill='gray12')
            
    button1 = Button(frame_1, text='Salir', bg='white' ,
        command = salir)
    button1.grid(row=0, column=0, padx=2)
    button2 = Button(frame_1, text='Iniciar', bg='white', 
        command = movimientos)
    button2.grid(row=0, column=1, padx=2)
    temporizador= Label(frame_1,text='Tiempo :',bg='black', fg = 'white', font=('Arial',12, 'bold'))
    temporizador.grid(row=0, column=3,padx=2)
    cantidad =Label(frame_1, text='Objetivos ❤ :', bg='black', 
        fg = 'aqua', font=('Arial',12, 'bold'))
    cantidad.grid(row=0, column=2, padx=2)
    MovimientosRealizados_Culebra= Label(frame_1, text='Movimiento:',bg='black', fg='white',font=('Arial',12, 'bold'))
    MovimientosRealizados_Culebra.grid(row=0,column=5,pady=2)
    centrar_ventana(ventana=ventana)
    ventana.mainloop()