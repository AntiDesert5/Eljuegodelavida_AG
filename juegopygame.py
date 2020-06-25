# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 19:12:07 2020

@author: Valenzuela
"""

import pygame, sys
import random
import time
import math
import numpy
from pygame import gfxdraw  # biblioteca para formas


def main():
    pygame.init()
    reproduction_rate = 0.0005
    Tamaniochequeo = 10
    # se definen colores
    Black = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    fps = 60
    masviejo = 0
    mutacion = 0.2  # valor para mutacion
    steering_weights = 0.05
    rangodepercepcion = 100
    rangodevisionconmutac = 30
    max_vel = 10
    fuerzaindividuo = 0.02
    vida = 100
    Entidades = []
    anchopantalla = 1000
    altopantalla = 600
    maxenemigos = 30
    margendelimitador = 10
    comida = []
    enemigos = []
    gameDisplay = pygame.display.set_mode((anchopantalla, altopantalla))
    alimento = [20,
                -80]  # es un arreglo para facilitar las cosas , de esta manera podemos tener la vida que da al comer y lo que resta al comer alimento malo
    clock = pygame.time.Clock()

    def Vida():
        porcentajevida = bot.vidapersona / vida
        cambiocolor = (max(min((1 - porcentajevida) * 255, 255), 0), max(min(porcentajevida * 255, 255), 0), 0)
        return (cambiocolor)

    def calcularmagnitud(vector):
        x = 0
        for i in vector:
            x += i ** 2  # i^2
        magnitude = x ** 0.5  # x^0.5
        return (magnitude)

    def normalizar(vector):
        magnitude = calcularmagnitud(vector)
        if magnitude != 0:
            vector = vector / magnitude
        return (vector)

    class CrearEntidad():  # aqui va lo de los Entidades, creare vida, colores, el rango para ver y muy
        # Vamos a crear un constructor
        def __init__(self, x, y, gen=False):
            self.posicion = numpy.array([x, y], dtype='float64')
            self.velocidad = numpy.array([random.uniform(-max_vel, max_vel), random.uniform(-max_vel, max_vel)])
            self.Aceleracion = numpy.array([0, 0], dtype='float64')
            self.Color = BLUE
            self.fuerzamaxima = 0.5
            self.vidapersona = vida
            self.velocidadmax = 2
            self.edad = 1

            if gen != False:  # si gen es verdadero entonces puede haber probalilidad de mutar
                self.genindividuos = []
                for i in range(len(gen)):
                    if random.random() < mutacion:  # aqui puede haber una probabilidad de mutar, este valor puede cambiar arriba en la declaracion
                        if i < 2:
                            self.genindividuos.append(gen[i] + random.uniform(-steering_weights, steering_weights))
                            print("funciona2")
                        else:
                            self.genindividuos.append(gen[i] + random.uniform(-rangodevisionconmutac,
                                                                              rangodevisionconmutac))

                    else:
                        self.genindividuos.append(gen[i])
                        print("funciona")
            else:  # si gen es falso creamos un gennuevo con valores aleatorios
                self.genindividuos = [random.uniform(-fuerzaindividuo, fuerzaindividuo),
                                      random.uniform(-fuerzaindividuo, fuerzaindividuo),
                                      random.uniform(0, rangodepercepcion),
                                      random.uniform(0, rangodepercepcion)]
            #print(self.genindividuos)

        def apply_force(self, force):
            self.Aceleracion += force  # tuve arror con incompatibilidad de datos, uno era int y el otro float, se resolvio con dtype tipo de dato en constructor

        def ver(self, target):
            desired_vel = numpy.add(target, -self.posicion)  # suma los elementos
            desired_vel = normalizar(desired_vel) * self.velocidadmax
            direccion = numpy.add(desired_vel, -self.velocidad)
            direccion = normalizar(direccion) * self.fuerzamaxima
            return (direccion)

        def comer(self, listacosas, index):  # funcion para comer index es 1 para enemigos, 0 comida
            mascercano = None
            distanciacercania = max(anchopantalla, altopantalla)  # escoje el mas alto
            bot_x = self.posicion[0]
            bot_y = self.posicion[1]
            numerocosas = len(listacosas) - 1
            for i in listacosas[::-1]:
                item_x = i[0]  # comida
                item_y = i[1]  # enemigos
                distance = math.hypot(bot_x - item_x,
                                      bot_y - item_y)  # se saca la distancia, como me recomendo el profe
                if distance < 5:  # distancia menor que 5
                    listacosas.pop(numerocosas)
                    self.vidapersona += alimento[index]  # sumamos vida ya que index tiene valor de 0 restamos si es 1
                if distance < distanciacercania:
                    distanciacercania = distance
                    mascercano = i
                numerocosas -= 1
            # if distanciacercania < self.genindividuos[2 + index]:#
            if distanciacercania < self.genindividuos[
                3]:  # se decide si distancia cercana es menor que el rango de vision
                seek = self.ver(mascercano)  # se manda a la funcion ver
                seek *= self.genindividuos[index]
                seek = normalizar(seek) * self.fuerzamaxima
                self.apply_force(seek)

        def margenes(self):  # crea margenes, se hace un chequeo por los cuatro lados
            desired = None
            x_pos = self.posicion[0]  # eje x
            y_pos = self.posicion[1]  # eje y
            if x_pos < Tamaniochequeo:  # si el eje x es menor que 10
                desired = numpy.array([self.velocidadmax, self.velocidad[1]])
                Direccion = desired - self.velocidad
                Direccion = normalizar(Direccion) * self.fuerzamaxima
                self.apply_force(Direccion)
            elif x_pos > anchopantalla - Tamaniochequeo:  # si x es mayor que el ancho de pantalla menos 10
                desired = numpy.array([-self.velocidadmax, self.velocidad[1]])
                Direccion = desired - self.velocidad
                Direccion = normalizar(Direccion) * self.fuerzamaxima
                self.apply_force(Direccion)
            if y_pos < Tamaniochequeo:
                desired = numpy.array([self.velocidad[0], self.velocidadmax])
                Direccion = desired - self.velocidad
                Direccion = normalizar(Direccion) * self.fuerzamaxima
                self.apply_force(Direccion)
            elif y_pos > altopantalla - Tamaniochequeo:
                desired = numpy.array([self.velocidad[0], -self.velocidadmax])
                Direccion = desired - self.velocidad
                Direccion = normalizar(Direccion) * self.fuerzamaxima
                self.apply_force(Direccion)

        def reproduce(self):
            if random.random() < reproduction_rate:
                Entidades.append(CrearEntidad(self.posicion[0], self.posicion[1], self.genindividuos))

        def update(self):
            self.velocidad += self.Aceleracion
            self.velocidad = normalizar(self.velocidad) * self.velocidadmax
            self.posicion += self.velocidad
            self.Aceleracion = 0
            self.vidapersona -= 0.2
            self.colour = Vida()  # cambia de color mientras no come
            self.health = min(vida, self.vidapersona)

            self.edad += 1

        def dead(self):
            if self.vidapersona > 0:  # si vida persona es mayot que 0 entonces no hace nada
                return (False)
            else:  # si x es menor que el ancho de pantalla
                if self.posicion[0] < anchopantalla - margendelimitador and self.posicion[0] > margendelimitador and \
                        self.posicion[1] < altopantalla - margendelimitador and self.posicion[1] > margendelimitador:
                    comida.append(self.posicion)
                return (True)

        def dibujarcirculos(self):  # dibuja circulos
            pygame.gfxdraw.aacircle(gameDisplay, int(self.posicion[0]), int(self.posicion[1]), 10,
                                    self.Color)  # paso suoerficie,posicion X e Y , radio y color
            pygame.gfxdraw.filled_circle(gameDisplay, int(self.posicion[0]), int(self.posicion[1]), 10, self.Color)
            pygame.draw.circle(gameDisplay,
                               GREEN,
                               (int(self.posicion[0]), int(self.posicion[1])),
                               abs(int(self.genindividuos[2])),
                               abs(int(min(2, self.genindividuos[2]))))
            pygame.draw.line(gameDisplay, GREEN, (int(self.posicion[0]), int(self.posicion[1])), (
                int(self.posicion[0] + (self.velocidad[0] * self.genindividuos[0] * 35)),
                int(self.posicion[1] + (self.velocidad[1] * self.genindividuos[0] * 35))), 3)

    for i in range(4):
        Entidades.append(CrearEntidad(random.uniform(0, anchopantalla), random.uniform(0,
                                                                                       altopantalla)))  # le pasamos cordenadas para aparecer, no pude ser fuera de la pantalla

    running = True

    while running:
        gameDisplay.fill(Black)  # color fondo
        if len(Entidades) < 5 or random.random() < 0.0001:
            Entidades.append(CrearEntidad(random.uniform(0, anchopantalla), random.uniform(0, altopantalla)))
        if random.random() < 0.01:
            comida.append(numpy.array([random.uniform(margendelimitador, anchopantalla - margendelimitador),
                                       random.uniform(margendelimitador, altopantalla - margendelimitador)], dtype='float64'))
        if random.random() < 0.01:
            enemigos.append(numpy.array([random.uniform(margendelimitador, anchopantalla - margendelimitador),
                                         random.uniform(margendelimitador, altopantalla - margendelimitador)],
                                        dtype='float64'))
        if len(enemigos) > maxenemigos:
            enemigos.pop(0)

        for event in pygame.event.get():  # fragmento para poder cerrar pygame sin que se trabe
            if event.type == pygame.QUIT:
                running = False

        for bot in Entidades[::-1]:  # truco en python para poder regresar los elementos al reves
            bot.comer(comida, 0)
            bot.comer(enemigos, 1)
            bot.margenes()
            bot.update()

            if bot.edad > masviejo:
                masviejo = bot.edad
                genmasviejo = bot.genindividuos
                print(masviejo, genmasviejo)
            bot.dibujarcirculos()

            if bot.dead():
                Entidades.remove(bot)
                #bot.reproduce()
            else:
                bot.reproduce()
        # se crean bolas de vida y malas
        for i in comida:
            pygame.draw.circle(gameDisplay, GREEN, (int(i[0]), int(i[1])), 10)
        # pygame.draw.circle(gameDisplay, bot.colour, (int(self.position[0]), int(self.position[1])), 10)
        for i in enemigos:
            pygame.draw.circle(gameDisplay, RED, (int(i[0]), int(i[1])), 10)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


main()
