
import pygame
import sys
import mainFile

# Inicialización
pygame.init()

ANCHO, ALTO = 1000, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mover Personaje 2D")
reloj = pygame.time.Clock()

mainFile.Jugar(mainFile)
mirando = mainFile.director.builder.juego.personaje.ubicadoEn.forma.sur
print("Mirando:", mirando)


def dibujarPared():
    pygame.draw.rect(pantalla, GRIS, (250, 10, ANCHO-250-10, ALTO-20))

def dibujarPuerta():
    pygame.draw.rect(pantalla, MADERA, (500, 300, 200, 290))
    pygame.draw.circle(pantalla, LATON, (675, 475), 10)

def dibujarBomba(bomba):
    pygame.draw.circle(pantalla, NEGRO, (500, 300), 50)
    if isinstance(bomba.elemento, mainFile.Puerta):
        dibujarPuerta()
    elif isinstance(bomba.elemento, mainFile.Pared):
        dibujarPared()

def dibujarBicho():
    pygame.draw.circle(pantalla, ROJO, (500, 300), 25)

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 30, 200)
ROJO = (255, 0, 0)
GRIS = (200, 200, 200)
MADERA = (101, 67, 33)
LATON = (218, 165, 32)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pantalla.fill(AZUL)
    pygame.draw.rect(pantalla, GRIS, (250, 10, ANCHO-250-10, ALTO-20))
    if isinstance(mirando, mainFile.Puerta):
        dibujarPuerta()
    if isinstance(mirando, mainFile.Pared):
        dibujarPared()
    if isinstance(mirando, mainFile.Bomba):
        dibujarBomba(mirando)
    pygame.display.flip()
    reloj.tick(60)