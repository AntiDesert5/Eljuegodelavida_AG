import turtle
import time
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
posponer=0.1

#parte de red neuronal cambiar por funcones o otro archivo despues
# cargamos entradas
training_data = np.array([[],[],[],[]], "float32")

 


#configuacion ventana 
wn = turtle.Screen()
wn.title("Ecosistema")
wn.bgcolor("black")
wn.setup(width = 600,height=600)
wn.tracer(0)


#
personaje = turtle.Turtle()
personaje.speed(0)
personaje.shape("square")
personaje.color("white")
personaje.fillcolor("black")
personaje.penup();
personaje.goto(0,0)
personaje.direction = "up"

#comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup();
comida.goto(0,100)


#funciones
def genobj():
    
    return 0
    
def mov():
    if personaje.direction=="up":#el personaje se muevo hacia arriba
        y=personaje.ycor()
        personaje.sety(y+5)

while True:
    wn.update()
    if personaje.distance(comida)<20:#mide la distancia entre los prefabs, el tamaño predeterminado de cada uno es 20
        x = np.random.randint(-280,280)#crear comida random parte x
        y = np.random.randint(-280,280)#crear comida random parte y
        comida.goto(x,y)
        
    mov()
    time.sleep(posponer)

