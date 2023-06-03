import pygame
import math
from sys import exit

# COLORES:
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BLANCO_SUAVE = (200, 200, 200)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 0
LONGITUD_COLA = 500  # Cantidad de puntos de trayectoria se almacenan
VALOR_DISPERSION = 15  # Cada cuantos n_frames almacenar un punto de trayectoria

# Variables:

g = 9.8 / (60 * 60)
# g = 1

m1 = 50
m2 = 70  # kg
l1 = 125
l2 = 125  # metros

ang1 = math.pi * 1.1
ang2 = math.pi * 1
vel1 = 0
vel2 = 0
ace1 = 0
ace2 = 0

CENTRO_X = WINDOW_WIDTH / 2
CENTRO_Y = WINDOW_HEIGHT / 2

x = 0
y = 0
n_frame = 0

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pendulo doble")
clock = pygame.time.Clock()

punto_origen = [CENTRO_X + l1 * math.sin(ang1) + l2 * math.sin(ang2),
                CENTRO_Y + l1 * math.cos(ang1) + l2 * math.cos(ang2)]

puntos_trazo = [punto_origen, punto_origen]


def almacenar_trazo():
    if n_frame % VALOR_DISPERSION == 0:
        puntos_trazo.append([x2, y2])
        if len(puntos_trazo) > LONGITUD_COLA:
            puntos_trazo.pop(0)


def dibujar_trazo_segmentos():
    pygame.draw.aalines(WINDOW, ROJO, False, list(puntos_trazo[i] for i in range(len(puntos_trazo))))


def dibujar_trazo_puntos():
    for i in range(len(puntos_trazo)):
        pygame.draw.circle(WINDOW, ROJO, puntos_trazo[i], 2)


def dibujar_pendulos():
    pygame.draw.aaline(WINDOW, AZUL, (CENTRO_X, CENTRO_Y), (x1, y1))  # Línea azul 1
    pygame.draw.aaline(WINDOW, AZUL, (x1, y1), (x2, y2))  # Línea azul 2
    pygame.draw.circle(WINDOW, ROJO, (CENTRO_X, CENTRO_Y), 5)  # Punto centró
    pygame.draw.circle(WINDOW, BLANCO, (x1, y1), 5)  # Punta 1
    pygame.draw.circle(WINDOW, BLANCO, (x2, y2), 5)  # Punta 2


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    WINDOW.fill(NEGRO)

    x1 = CENTRO_X + l1 * math.sin(ang1)
    y1 = CENTRO_Y + l1 * math.cos(ang1)
    x2 = x1 + l2 * math.sin(ang2)
    y2 = y1 + l2 * math.cos(ang2)

    # Calculo 1
    num1 = - g * (2 * m1 + m2) * math.sin(ang1)
    num2 = - m2 * g * math.sin(ang1 - 2 * ang2)
    num3 = - 2 * math.sin(ang1 - ang2) * m2
    num4 = (vel2 * vel2 * l2 + vel1 * vel1 * l1 * math.cos(ang1 - ang2))
    den = l1 * (2 * m1 + m2 - m2 * math.cos(2 * ang1 - 2 * ang2))

    ace1 = (num1 + num2 + num3 * num4) / den

    # Calculo 2
    num1 = 2 * math.sin(ang1 - ang2)
    num2 = vel1 * vel1 * l1 * (m1 + m2)
    num3 = g * (m1 + m2) * math.cos(ang1)
    num4 = vel2 * vel2 * l2 * m2 * math.cos(ang1 - ang2)

    ace2 = (num1 * (num2 + num3 + num4)) / den

    # Actualizar variables
    vel1 += ace1
    vel2 += ace2
    # Perdida de energía
    # vel1 *= 0.9999
    # vel2 *= 0.9999
    ang1 += vel1
    ang2 += vel2

    # Dibujar trazo
    n_frame += 1
    almacenar_trazo()
    dibujar_trazo_segmentos()
    # dibujar_trazo_puntos()

    # Dibujar pendulo
    dibujar_pendulos()

    # Dibujar circunferencias
    # pygame.draw.circle(WINDOW, BLANCO_SUAVE, (CENTRO_X, CENTRO_Y), l1+l2+1, 1) # Circunferencia general
    # pygame.draw.circle(WINDOW, BLANCO_SUAVE, (CENTRO_X, CENTRO_Y), l1, 1)  # Circunferencia 1
    # pygame.draw.circle(WINDOW, BLANCO_SUAVE, (x1, y1), l2, 1) # Circunferencia 2

    pygame.display.update()
    clock.tick(FPS)
