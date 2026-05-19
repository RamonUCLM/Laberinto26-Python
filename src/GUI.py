
import pygame
import sys
import mainFile

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 30, 200)
ROJO = (255, 0, 0)
GRIS = (200, 200, 200)
MADERA = (101, 67, 33)
LATON = (218, 165, 32)


ANCHO, ALTO = 1000, 600

class GUI:
    
    def __init__(self):
        pygame.init()

        
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Mover Personaje 2D")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Arial", 30)
        self.botones = []
        self.menux = 10
        self.menuy = 10
        self.boton_ancho = 100
        self.boton_alto = 25

        director =mainFile.load()
        self.juego = director.builder.juego
        self.juego.attachObserver(self)
        self.pantalla.fill(AZUL)
        pygame.draw.rect(self.pantalla, GRIS, (250, 10, ANCHO-250-10, ALTO-20))
        self.refrescarPantalla()
        while True:
            pos_raton = pygame.mouse.get_pos()
            pygame.display.flip()
            self.reloj.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # 1 es el clic izquierdo
                        for boton_rect in self.botones:
                            if boton_rect.collidepoint(pos_raton):
                                print("¡Botón pulsado!")
                                self.reloj.tick(120)
                                self.refrescarPantalla()

    def refrescarPantalla(self):
        self.juego.obtenerVista("Norte")
        for orientacion in self.juego.obtenerOrientacionesDisponibles():
            self.dibujarOpcion(orientacion, self.menux, self.menuy + self.juego.obtenerOrientacionesDisponibles().index(orientacion) * self.boton_alto, self.boton_ancho, self.boton_alto)
            self.menuy += self.boton_alto + 10
        self.menuy = 10
    def dibujarPared(self):
        pygame.draw.rect(self.pantalla, GRIS, (250, 10, ANCHO-250-10, ALTO-20))

    def dibujarPuerta(self):
        pygame.draw.rect(self.pantalla, MADERA, (500, 300, 200, 290))
        pygame.draw.circle(self.pantalla, LATON, (675, 475), 10)

    def dibujarBomba(self, bomba):
        if isinstance(bomba.elemento, mainFile.Puerta):
            self.dibujarPuerta()
        elif isinstance(bomba.elemento, mainFile.Pared):
            self.dibujarPared()
        pygame.draw.circle(self.pantalla, NEGRO, (600, 300), 50)
    
    def dibujarBoton(self, boton):
        if isinstance(boton.elemento, mainFile.Puerta):
            self.dibujarPuerta()
            pygame.draw.circle(self.pantalla, NEGRO, (500, 300), 25)
            pygame.draw.circle(self.pantalla, ROJO, (500, 300), 20)
        elif isinstance(boton.elemento, mainFile.Pared):
            self.dibujarPared()
            pygame.draw.circle(self.pantalla, NEGRO, (600, 300), 25)
            pygame.draw.circle(self.pantalla, ROJO, (600, 300), 20)

    def dibujarBicho(self):
        pygame.draw.circle(self.pantalla, ROJO, (500, 300), 25)
    def dibujarOpcion(self, opcion, x, y, ancho, alto):
        self.botones.append(pygame.Rect(x, y, ancho, alto))
        pygame.draw.rect(self.pantalla, ROJO, (x, y, ancho, alto))

    def update(self,mensaje):
        if mensaje["commando"] == "dibujarPuerta":
            self.dibujarPuerta()
        elif mensaje["commando"] == "dibujarPared":
            self.dibujarPared()
        elif mensaje["commando"] == "dibujarBomba":
            self.dibujarBomba(mensaje["elemento"])
        elif mensaje["commando"] == "dibujarBoton":
            self.dibujarBoton(mensaje["elemento"])

    
GUI()