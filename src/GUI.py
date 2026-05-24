import pygame
import sys
import mainFile

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 30, 200)
ROJO = (255, 0, 0)
ROJO_CLARO = (255, 100, 100)
GRIS = (200, 200, 200)
MADERA = (101, 67, 33)
LATON = (218, 165, 32)
MORADO = (128, 0, 128)
VERDE = (0, 255, 0)

ANCHO, ALTO = 1000, 600

class GUI:
    
    def __init__(self):
        pygame.init()
        
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Mover Personaje 2D")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Arial", 15)
        
        self.botones = [] # Aquí guardaremos los rectángulos de colisión
        self.acciones_botones = [] # Guardaremos a qué orientación corresponde cada botón
        
        self.menux = 10
        self.menuy = 10
        self.boton_ancho = 100
        self.boton_alto = 25

        director = mainFile.load()
        self.juego = director.builder.juego
        self.juego.attachObserver(self)
        self.mirando = "Norte"
        def recorrerLaberinto(elemento):
            print(elemento)
        
        # Renderizado inicial
        self.refrescarPantalla(self.mirando)
        
        # BUCLE PRINCIPAL CORRECTO
        while True:
            # 1. Manejo de eventos (Siempre al principio del bucle)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic izquierdo
                        pos_raton = pygame.mouse.get_pos()
                        
                        # Comprobar qué botón se pulsó
                        for i, boton_rect in enumerate(self.botones):
                            if boton_rect.collidepoint(pos_raton):
                                pulsado = self.acciones_botones[i]
                                print(f"¡Botón pulsado!: {pulsado}")
                                self.offsetmensaje = 482
                                pygame.draw.rect(self.pantalla, NEGRO, (10, 480, 220, 115))


                                # Aquí deberías llamar a la acción real de tu juego, por ejemplo:
                                # self.juego.mover(orientacion_pulsada)
                                
                                if pulsado in self.juego.obtenerOrientacionesDisponibles():
                                    self.mirando = pulsado
                                    self.refrescarPantalla(self.mirando)
                                    texto_superficie = self.fuente.render(f"Vida: {self.juego.personaje.vida}", True, BLANCO)
                                    self.pantalla.blit(texto_superficie, (10, 440))
                                elif pulsado.lower().startswith("bicho"):
                                    bicho_indice = int(pulsado.split()[-1])
                                    self.dibujarOpcion("Atacar Bicho " + str(bicho_indice), self.menux, self.menuy, self.boton_ancho, self.boton_alto, LATON)
                                    self.menuy += self.boton_alto + 10
                                elif pulsado.lower().startswith("atacar bicho"):
                                    bicho_indice = int(pulsado.split()[-1])
                                    result = self.juego.atacarBicho(bicho_indice)
                                    #self.dibujarMensaje(f"Atacas al bicho {bicho_indice}, su vida es {result}!")
                                else:
                                    self.refrescarPantalla(self.mirando)
                                    self.ejecutarAccion(pulsado, self.mirando)
                                    texto_superficie = self.fuente.render(f"Vida: {self.juego.personaje.vida}", True, BLANCO)
                                    self.pantalla.blit(texto_superficie, (10, 440))
                                break # Rompemos el ciclo para evitar procesar clics fantasma

            # 2. Actualizar pantalla
            pygame.display.flip()
            
            # 3. Controlar FPS (60 estables)
            self.reloj.tick(60)

    def refrescarPantalla(self, mirando):
        # IMPORTANTÍSIMO: Limpiar la pantalla y vaciar las listas de botones antiguos
        self.pantalla.fill(AZUL)
        pygame.draw.rect(self.pantalla, GRIS, (250, 10, ANCHO-250-10, ALTO-20))
        self.pantalla.blit(self.fuente.render("Eventos:", True, BLANCO), (10, 460))
        pygame.draw.rect(self.pantalla, NEGRO, (10, 480, 220, 115))
        # Escalamos un poco el texto si es muy grande para el botón (puedes ajustar el tamaño de la fuente)
        
        self.botones = []
        self.acciones_botones = []
        self.menuy = 10

        self.juego.obtenerVista(mirando) # Nota: Esto asumo que dispara el Observer (update)
        
        # Redibujar los botones de opciones
        orientaciones = self.juego.obtenerOrientacionesDisponibles()
        for orientacion in orientaciones:
            # Dibujamos y registramos el botón
            self.dibujarOpcion(orientacion, self.menux, self.menuy, self.boton_ancho, self.boton_alto)
            self.menuy += self.boton_alto + 10
        acciones = self.juego.obtenerAccionesDisponibles(mirando)
        for accion in acciones:
            # Dibujamos y registramos el botón
            self.dibujarOpcion(accion, self.menux, self.menuy, self.boton_ancho, self.boton_alto, ROJO_CLARO)
            self.menuy += self.boton_alto + 10
        for bicho in self.juego.jugadorBuscarObjetivo():
            self.dibujarOpcion(f"Bicho {bicho}", self.menux, self.menuy, self.boton_ancho, self.boton_alto, MORADO)
            self.menuy += self.boton_alto + 10
    
    def ejecutarAccion(self, accion, mirando):
        self.juego.ejecutarAccion(mirando, accion)

    def dibujarOpcion(self, opcion, x, y, ancho, alto, color=ROJO):
        rect = pygame.Rect(x, y, ancho, alto)
        self.botones.append(rect)
        self.acciones_botones.append(opcion) # Guardamos el texto/dirección de este botón
        
        # Dibujar el botón
        pygame.draw.rect(self.pantalla, color, rect)
        
        # Opcional: Dibujar el texto de la orientación sobre el botón
        texto_superficie = self.fuente.render(opcion, True, BLANCO)
        # Escalamos un poco el texto si es muy grande para el botón (puedes ajustar el tamaño de la fuente)
        self.pantalla.blit(texto_superficie, (x + 5, y + 2))

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

    def dibujarHongo(self,boton):
        if isinstance(boton.elemento, mainFile.Puerta):
            self.dibujarPuerta()
            pygame.draw.circle(self.pantalla, ROJO, (525, 325), 25)
            pygame.draw.rect(self.pantalla, VERDE, (500, 300, 50, 50))
        if isinstance(boton.elemento, mainFile.Pared):
            self.dibujarPared()
            pygame.draw.circle(self.pantalla, ROJO, (625, 325), 25)
            pygame.draw.rect(self.pantalla, VERDE, (600, 300, 50, 50))

    def dibujarMensaje(self, mensaje):
        if len(mensaje) > 30:
            for i in range(0, len(mensaje), 35):
                texto_superficie = self.fuente.render(mensaje[i:i+35], True, BLANCO)
                print("línea")
                self.offsetmensaje = self.offsetmensaje + i//35 * 20
                self.pantalla.blit(texto_superficie, (15, self.offsetmensaje))
        else:
            texto_superficie = self.fuente.render(mensaje, True, BLANCO)
            self.pantalla.blit(texto_superficie, (15, self.offsetmensaje))
            self.offsetmensaje = self.offsetmensaje + 20

    def update(self, mensaje):
        if mensaje["commando"] == "dibujarPuerta":
            self.dibujarPuerta()
        elif mensaje["commando"] == "dibujarPared":
            self.dibujarPared()
        elif mensaje["commando"] == "dibujarBomba":
            self.dibujarBomba(mensaje["elemento"])
        elif mensaje["commando"] == "dibujarBoton":
            self.dibujarBoton(mensaje["elemento"])
        elif mensaje["commando"] == "dibujarHongo":
            self.dibujarHongo(mensaje["elemento"])
        elif mensaje["commando"] == "resultadoAccion":
            self.dibujarMensaje(mensaje["mensaje"])
            if mensaje["mensaje"].startswith("¡Un bicho te ha atacado!"):
                for bicho in self.juego.jugadorBuscarObjetivo():
                    self.dibujarOpcion(f"Bicho {bicho}", self.menux, self.menuy, self.boton_ancho, self.boton_alto, MORADO)
                    self.menuy += self.boton_alto + 10
    
GUI()