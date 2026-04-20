
import pygame
import sys

# Inicialización
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mover Personaje 2D")
reloj = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 30, 200)
ROJO = (255, 0, 0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    


    pantalla.fill(AZUL)
    pygame.display.flip()
    reloj.tick(60)
