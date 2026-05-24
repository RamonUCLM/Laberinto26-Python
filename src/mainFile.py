from abc import ABC, abstractmethod
import json
import random
import copy
import threading
import time
import logging
import subprocess
import Visitor as visitors
import time
import sys
import os
import platform

#Cambiar este parámetro si quieres jugar en la consola o en la GUI
consola = True

def escribir_lento(texto, velocidad=0.03):
    if isinstance(texto, list):
        textoini = texto
        texto = ""
        for linea in textoini:
            texto += str(linea) + "\n"
    for letra in texto:
        # sys.stdout.write no añade un salto de línea automático como print
        sys.stdout.write(letra)
        sys.stdout.flush() # Fuerza a la terminal a mostrar la letra YA
        time.sleep(velocidad) # Pausa en segundos (0.05 = 50 milisegundos)
    print() # Al terminar, hace el salto de línea

def limpiar_pantalla():
    # platform.system() devuelve 'Windows', 'Linux' o 'Darwin' (macOS)
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def imprimirElemento(elemento):
    escribir_lento(elemento.__str__(), velocidad=0.03)

def cargarLogging():
    logging.basicConfig(level=logging.INFO, filename='juego.log', filemode='w')


class Comando(ABC):
    def __init__(self, receptor):
        self.receptor = receptor
    @abstractmethod
    def ejecutar(self, unEnte):
        pass

class Abrir(Comando):
    def ejecutar(self, unEnte):
        self.receptor.setAbierta(True)
        return "Puerta abierta"
    def __str__(self):
        return f"Abrir"
class Cerrar(Comando):
    def ejecutar(self, unEnte):
        self.receptor.setAbierta(False)
        return "Puerta cerrada"
    def __str__(self):
        return f"Cerrar"
class entrar(Comando):
    def ejecutar(self, unEnte):
        self.result = self.receptor.entrar(unEnte)
        return self.result
    def __str__(self):
        return f"Entrar"
class explorar(Comando):
    def ejecutar(self, unEnte):
        self.result = self.receptor.entrar(unEnte)
        return self.result
    def __str__(self):
        return f"Explorar"
class pulsar(Comando):
    def ejecutar(self, unEnte):
        self.result = self.receptor.entrar(unEnte)
        return self.result
    def __str__(self):
        return f"Pulsar"

class equiparArma(Comando):
    def ejecutar(self, arma):
        if arma.equipada == False:
            arma.equipada = True
            self.receptor.poder += arma.poder
            return "Te has equipado el arma"
        return "Ya está equipada"
    def __str__(self):
        return "Equipar"

class desEquiparArma(Comando):
    def ejecutar(self, arma):
        if arma.equipada == True:
            arma.equipada = False
            self.receptor.poder -= arma.poder
            return "Te has desequipado el arma"
        return "Ya está desequipada"
    def __str__(self):
        return "Desequipar"

class cogerObjeto(Comando):
    def ejecutar(self, unEnte, orientacion):
        objeto = self.receptor.forma.orientaciones[orientacion].getElemento(self.receptor.forma)
        self.receptor.ponerEnOrientacion(orientacion, None)
        return objeto
    def __str__(self):
        return "Coger un Objeto"
#
class ElementoMapa(ABC):
    def __init__(self, id):
        self.id = id
        self.comandos = []
    def agregarComando(self, comando):
        self.comandos.append(comando)
    def ejecutarComando(self, comando):
        if comando in self.comandos:
            comando.ejecutar()
        else:
            print("El comando no está asociado a este elemento del mapa")     
    def eliminarComando(self, comando):
        if comando in self.comandos:
            self.comandos.remove(comando)
    def listarComandos(self):
        return self.comandos
    @abstractmethod
    def entrar(self, unEnte):
        pass
    @abstractmethod
    def recorrer(self, unBloque):
        unBloque(self)
    @abstractmethod
    def aceptar(self, visitor):
        pass

#Singleton para las orientaciones, ya que cada orientación es única en el mapa.
class Orientacion(ABC):
    elemento = None
    @staticmethod
    def getOrientacion():
        print("No implementada: esta función debe devolver el nombre de esta orientación")
    @staticmethod
    def ponerElemento(contenedor, elemento):
        print("No implementada: esta función debe colocar un elemento en esta orientación del contenedor")
    @staticmethod
    def quitarElemento(contenedor):
        print("No implementada: esta función debe quitar el elemento de esta orientación del contenedor")
    @staticmethod
    def getElemento(contenedor):
        print("No implementada: esta función debe devolver el elemento de esta orientación del contenedor")
    @staticmethod
    def recorrer(contenedor, unBloque):
        print("No implementada: esta función debe recorrer los elementos de esta orientación del contenedor siguiendo el pratrón Iterator")
    @staticmethod   
    def aceptar(visitor, forma):
        print("No implementada: esta función debe aceptar un visitor para esta orientación del contenedor")

class Norte(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Norte"
    @staticmethod
    def default():
        pass
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.norte:
            print(f"Sustituyendo un elemento {forma.norte} por {elemento} en la orientación Norte")
            forma.norte = elemento
        else:
            forma.norte = elemento
    @staticmethod
    def quitarElemento(forma):
        if forma.norte:
            forma.norte = None
    @staticmethod
    def getElemento(forma):
        return forma.norte
    @staticmethod
    def recorrer(forma, unBloque):
        if forma.norte:
            print("En el norte hay:")
            forma.norte.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        if forma.norte:
            forma.norte.aceptar(visitor)

class Sur(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Sur"
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.sur:
            print(f"Sustituyendo un elemento {forma.sur} por {elemento} en la orientación Sur")
            forma.sur = elemento
        else:
            forma.sur = elemento
    @staticmethod
    def quitarElemento(forma):
        if forma.sur:
            forma.sur = None
    @staticmethod
    def getElemento(forma):
        return forma.sur
    @staticmethod
    def recorrer(forma, unBloque):
        print("En el sur hay:")
        if forma.sur:
            forma.sur.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        if forma.sur:
            forma.sur.aceptar(visitor)

class Este(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Este"
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.este:
            print(f"Sustituyendo un elemento {forma.este} por {elemento} en la orientación Este")
            forma.este = elemento
        else:
            forma.este = elemento
    @staticmethod
    def quitarElemento(forma):
        if forma.este:
            forma.este = None
    @staticmethod
    def getElemento(forma):
        return forma.este
    @staticmethod
    def recorrer(forma, unBloque):
        print("En el este hay:")
        if forma.este:
            forma.este.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        if forma.este:
            forma.este.aceptar(visitor)

class Oeste(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Oeste"
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.oeste:
            print(f"Sustituyendo un elemento {forma.oeste} por {elemento} en la orientación Oeste")
            forma.oeste = elemento
        else:
            forma.oeste = elemento
    @staticmethod
    def quitarElemento(forma):
        if forma.oeste:
            forma.oeste = None
    @staticmethod
    def getElemento(forma):
        return forma.oeste
    @staticmethod
    def recorrer(forma, unBloque):
        print("En el oeste hay:")
        if forma.oeste:
            forma.oeste.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        if forma.oeste:
            forma.oeste.aceptar(visitor)

class Noreste(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Noreste"
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.noreste:
            print(f"Sustituyendo un elemento {forma.noreste} por {elemento} en la orientación Noreste")
            forma.noreste = elemento
        elif isinstance(forma, Rombo):
            forma.noreste = elemento
        else:
            print("No se pueden colocar elementos en esta orientación para esta forma")
    @staticmethod
    def quitarElemento(forma):
        if forma.noreste:
            forma.noreste = None
    @staticmethod
    def getElemento(forma):
        return forma.noreste
    @staticmethod
    def recorrer(forma, unBloque):
        if forma.noreste:
            forma.noreste.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        forma.noreste.aceptar(visitor)

class Noroeste(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Noroeste"
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.noroeste:
            print(f"Sustituyendo un elemento {forma.noroeste} por {elemento} en la orientación Noroeste")
            forma.noroeste = elemento
        elif isinstance(forma, Rombo):
            forma.noreste = elemento
        else:
            print("No se pueden colocar elementos en esta orientación para esta forma")
    @staticmethod
    def quitarElemento(forma):
        if forma.noroeste:
            forma.noroeste = None
    @staticmethod
    def getElemento(forma):
        return forma.noreste
    @staticmethod
    def recorrer(forma, unBloque):
        if forma.noreste:
            forma.noreste.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        forma.noroeste.aceptar(visitor)

class Sureste(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Sureste"
    @staticmethod
    def ponerElemento(self,forma, elemento):
        if forma.sureste:
            print(f"Sustituyendo un elemento {forma.sureste} por {elemento} en la orientación Sureste")
            forma.sureste = elemento
        elif isinstance(forma, Rombo):
            forma.sureste = elemento
        else:
            print("No se pueden colocar elementos en esta orientación para esta forma")
    @staticmethod
    def quitarElemento(forma):
        if forma.sureste:
            forma.sureste = None
    @staticmethod
    def getElemento(forma):
        return forma.sureste
    @staticmethod
    def recorrer(forma, unBloque):
        if forma.sureste:
            forma.sureste.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        forma.sureste.aceptar(visitor)

class Suroeste(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Sureste"
    @staticmethod
    def ponerElemento(forma, elemento):
        if forma.suroeste:
            print(f"Sustituyendo un elemento {forma.suroeste} por {elemento} en la orientación Suroeste")
            forma.suroeste = elemento
        elif isinstance(forma, Rombo):
            forma.suroeste = elemento
        else:
            print("No se pueden colocar elementos en esta orientación para esta forma")
    @staticmethod
    def quitarElemento(forma):
        if forma.suroeste:
            forma.suroeste = None
    @staticmethod
    def getElemento(forma):
        return forma.suroeste
    @staticmethod
    def recorrer(forma, unBloque):
        if forma.suroeste:
            forma.suroeste.recorrer(unBloque)
    @staticmethod
    def aceptar(visitor, forma):
        forma.suroeste.aceptar(visitor)


#Patrón Bridge para las formas de las habitaciones, ya que cada forma puede tener diferentes implementaciones de las orientaciones.
class Forma(ABC):
    @abstractmethod
    def __init__(self, orientaciones):
        self.orientaciones = orientaciones
        pass
    @abstractmethod
    def __str__(self):
        pass

    def obtenerOrientacionAleatoria(self):
        return random.choice(list(self.orientaciones.values()))
    def obtenerOrientacionesDisponiblesLista(self):
        disponibles = []
        for orientacion in self.orientaciones:
            disponibles.append(orientacion)
        return disponibles
    def recorrer(self, contenedor, unBloque):
        for orientacion in self.orientaciones:
            self.orientaciones[orientacion].recorrer(self, unBloque)
    def agregarOrientacion(self, orientacion):
        self.orientaciones[orientacion.getOrientacion()] = orientacion
    def ponerElemento(self, contenedor, orientacion, elemento):
        if orientacion in self.orientaciones:
            self.orientaciones[orientacion].ponerElemento(self, elemento)
        else:
            print(f"La orientación {orientacion} no es válida para esta forma")

class Cuadrado(Forma):
    def __init__(self, orientaciones):
        super().__init__(orientaciones)
        self.agregarOrientacion(Norte)
        self.agregarOrientacion(Sur)
        self.agregarOrientacion(Este)
        self.agregarOrientacion(Oeste)
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None

    def __str__(self):
        return "Cuadrado"
    
class Rombo(Forma):
    def __init__(self, orientaciones):
        super().__init__(orientaciones)
        self.agregarOrientacion(Norte)
        self.agregarOrientacion(Sur)
        self.agregarOrientacion(Este)
        self.agregarOrientacion(Oeste)
        self.agregarOrientacion(Noreste)
        self.agregarOrientacion(Noroeste)
        self.agregarOrientacion(Sureste)
        self.agregarOrientacion(Suroeste)
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
        self.noreste = None
        self.noroeste = None
        self.sureste = None
        self.suroeste = None

    def __str__(self):
        return "Rombo"

#Contenedor sigue el patrón Composite, siendo el composite.
class Contenedor(ElementoMapa):

    def __init__(self, id, forma):
        super().__init__(id)
        self.hijos = []
        self.forma = forma

    def obtenerOrientacionAleatoria(self):
        return self.forma.obtenerOrientacionAleatoria()

    def ponerEnOrientacion(self, orientacion, elemento):
        self.forma.ponerElemento(self, orientacion,elemento)

    def obtenerHijo(self, posicion):
        try:
            return self.hijos[posicion]
        except IndexError:
            print("La posición no existe en la lista de hijos")
            return None
    def agregarHijo(self, posicion,elemento):
        self.hijos.insert(posicion, elemento)
    def eliminarHijo(self, posicion):
        try:
            self.hijos.pop(posicion)
        except IndexError:
            print("La posición no existe en la lista de hijos")
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)
    def aceptar(self, visitor):
        visitor.visitarContenedor(self)
        for hijo in self.hijos:
            hijo.aceptar(visitor)
        for orientacion in self.forma.orientaciones:
            self.forma.orientaciones[orientacion].aceptar(visitor, self.forma)
    

class Armario(Contenedor):
    def __init__(self, id,forma=Cuadrado({})):
        super().__init__(id, forma)
        self.comandos = []
        self.abierto = True
    def entrar(self, unEnte):
        if isinstance(unEnte, Personaje):
            print("Has entrado al armario: ", self.id)
            logging.info(f"Un {unEnte} entra en el armario: {self.id}")
        else:
            logging.info(f"Un {unEnte} entra en el armario: {self.id}")
        return self
    def setAbierta(self, abierta):
        self.abierto = abierta
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)
    def __str__(self):
        cadena = f"Un armario"
        return cadena
    def aceptar(self, visitor):
        visitor.visitarArmario(self)
        for hijo in self.hijos:
            hijo.aceptar(visitor)
        for orientacion in self.forma.orientaciones:
            self.forma.orientaciones[orientacion].aceptar(visitor, self.forma)
    def listaComandos(self):
        return self.comandos

#Habitación es un composite también.
class Habitacion(Contenedor):
    def __init__(self, id, forma=Cuadrado({})):
        super().__init__(id, forma)
    def entrar(self, unEnte):
        if isinstance(unEnte, Personaje):
            logging.info(f"Un {unEnte} entra en la habitación: {self.id}")
        else:
            logging.info(f"Un {unEnte} entra en la habitación: {self.id}")
        return self
    
    def recorrer(self, unBloque):
        unBloque(self)
        #for hijo in self.hijos:
        #    hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)

    def __str__(self):
        cadena = f"Una habitación"
        return cadena
    def aceptar(self, visitor):
        visitor.visitarHabitacion(self)
        for hijo in self.hijos:
            hijo.aceptar(visitor)
        for orientacion in self.forma.orientaciones:
            self.forma.orientaciones[orientacion].aceptar(visitor, self.forma)
        

#Hoja sigue el patrón Composite, siendo la hoja
class Hoja(ElementoMapa):
    def __init__(self):
        self.comandos = []
    def recorrer(self, unBloque):
        unBloque(self)
    def listaComandos(self):
        return self.comandos

class Espada(Hoja):
    def __init__(self):
        super().__init__()
        self.poder = 20
        self.equipada = False
    def __str__(self):
        return "Espada"
    def entrar(self):
        return self
    def aceptar(self, visitor):
        visitor.visitarEspada(self)

        
class Tunel(Hoja):
    def __init__(self):
        self.laberinto = None
    def setLaberinto(self, laberinto):
        self.laberinto = laberinto
    def getLaberinto(self):
        return self.laberinto
    def entrar(self, unEnte):
        self.laberinto = copy.deepcopy(unEnte.juego.laberintoPrototipo)
        self.laberinto.entrar(unEnte)
    def aceptar(self, visitor):
        visitor.visitarTunel(self)
    def __str__(self):
        return "Túnel"

class Pared(Hoja):
    def __init__(self):
        super().__init__()
    def entrar(self, unEnte):
        if isinstance(unEnte, Personaje):
            print("Has chocado contra una pared en la habitación: ", unEnte.ubicadoEn.id)
            return "Has chocado contra una pared"
            logging.info(f"Un {unEnte} choca contra una pared en la habitación: {unEnte.ubicadoEn.id}")
        else:
            logging.info(f"Un {unEnte} choca contra una pared en la habitación: {unEnte.ubicadoEn.id}")
    def __str__(self):
        return "Pared"
    def aceptar(self, visitor):
        visitor.visitarPared(self)

class Puerta(Hoja):
    def __init__(self, lado1, lado2, abierta=False):
        super().__init__()
        self.lado1 = lado1
        self.lado2 = lado2
        self.abierta = abierta
    def setAbierta(self, abierta):
        self.abierta = abierta
    def setLado1(self, lado):
        self.lado1 = lado
    def setLado2(self, lado):
        self.lado2 = lado
    def entrar(self, unEnte):
        if self.abierta:
            if  unEnte.ubicadoEn == self.lado1:
                if isinstance(unEnte, Personaje):
                    logging.info(f"Un {unEnte} pasa por la puerta hacia la habitación {self.lado2.id}")
                else:
                    logging.info(f"Un {unEnte} pasa por la puerta hacia la habitación {self.lado2.id}")
                self.lado2.entrar(unEnte)
                unEnte.ubicadoEn = self.lado2
                return "Has pasado por la puerta"
            elif unEnte.ubicadoEn == self.lado2:
                if isinstance(unEnte, Personaje):
                    logging.info(f"Un {unEnte} pasa por la puerta hacia la habitación {self.lado1.id}")
                else:                    
                    logging.info(f"Un {unEnte} pasa por la puerta hacia la habitación {self.lado1.id}")
                self.lado1.entrar(unEnte)
                unEnte.ubicadoEn = self.lado1
                return "Has pasado por la puerta"
            else:
                raise ValueError("El origen no es válido para esta puerta")
        else:
            if isinstance(unEnte, Personaje):
                print("La puerta está cerrada, no puedes pasar")
                logging.info(f"Un {unEnte} intenta pasar por una puerta cerrada entre {self.lado1.id} y {self.lado2.id}")
            else:
                logging.info(f"Un {unEnte} intenta pasar por una puerta cerrada entre {self.lado1.id} y {self.lado2.id}")
            return "La puerta está cerrada, no puedes pasar"
    def abrir(self):
        self.abierta = True
    def cerrar(self):
        self.abierta = False
    def aceptar(self, visitor):
        visitor.visitarPuerta(self)
    def __str__(self):
        estado = "abierta" if self.abierta else "cerrada"
        return f"Una puerta"

class Laberinto(Contenedor):
    def __init__(self, id, forma=None):
        super().__init__(id, forma)
    def entrar(self):
        print("Has entrado al laberinto")
        return self
    def obetenerHabitacion(self, id):
        for hijo in self.hijos:
            if isinstance(hijo, Habitacion) and hijo.id == id:
                return hijo
        print("No se encontró la habitación con id: ", id)
        return None
    def recorrer(self, unBloque):
        print("Recorriendo el laberinto: ", self.id)
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
    def aceptar(self, visitor):
        for hijo in self.hijos:
            hijo.aceptar(visitor)

class Ente(ABC):
    @abstractmethod
    def __init__(self, vida, poder, juego):
        self.vida = vida
        self.poder = poder
        self.juego = juego
        self.ubicadoEn = None

    def estaVivo(self):
        return self.vida > 0

class Bicho(Ente):
    def __init__(self, vida, poder, modo, juego):
        super().__init__(vida, poder, juego)
        self.modo = modo
    def actua(self):
        self.modo.actua(self)
    def __str__(self):
        return f"Bicho"

#Modo sigue el patrón Strategy, siendo la estrategia, además sigue el patrón Template Method, 
# siendo el método plantilla para las acciones de los bichos
class Modo(ABC):
    def actua(self, bicho):
        self.caminar(bicho)
        self.atacar(bicho)
        self.dormir(bicho)
    @abstractmethod
    def caminar(self, bicho):
        pass
    @abstractmethod
    def atacar(self, bicho):
        pass
    @abstractmethod
    def dormir(self, bicho):
        pass

class Agresivo(Modo):
    def caminar(self, bicho):
        destino = bicho.ubicadoEn.obtenerOrientacionAleatoria()
        logging.info(f"un bicho se mueve agresivamente hacia la orientación {destino.getOrientacion()}")
        destino.getElemento(bicho.ubicadoEn.forma).entrar(bicho)

    def atacar(self, bicho):
        logging.info(f"un bicho busca objetivo")
        objetivo = bicho.juego.bichoBuscarObjetivo(bicho)
        if objetivo:
            objetivo.vida -= bicho.poder
            logging.info(f"un bicho ataca al personaje, reduciendo su vida a {objetivo.vida}")
            mensaje = "¡Un bicho te ha atacado!"
            bicho.juego.notifyObservers({"commando": "resultadoAccion", "mensaje": mensaje})
            if bicho.juego.console:
                escribir_lento("¡Un bicho te ha atacado! Tu vida se ha reducido a " + str(objetivo.vida) + "\n")
        else:
            logging.info(f"un bicho no encuentra objetivo para atacar")
    def dormir(self, bicho):
        logging.info(f"un bicho no duerme, siempre está listo para atacar")

class Perezoso(Modo):
    def caminar(self, bicho):
        if random.random() < 0.5:
            destino = bicho.ubicadoEn.obtenerOrientacionAleatoria()
            logging.info(f"un bicho se mueve perezosamente hacia la orientación {destino.getOrientacion()}")
            destino.getElemento(bicho.ubicadoEn.forma).entrar(bicho)
        else:
            logging.info("El bicho perezoso decidió no moverse esta vez")
    def atacar(self, bicho):
        logging.info(f"un bicho busca objetivo")
        objetivo = bicho.juego.bichoBuscarObjetivo(bicho)
        if objetivo:
            objetivo.vida -= bicho.poder/2
            logging.info(f"un bicho ataca al personaje, reduciendo su vida a {objetivo.vida}")
            mensaje = "¡Un bicho te ha atacado!"
            bicho.juego.notifyObservers({"commando": "resultadoAccion", "mensaje": mensaje})
            if bicho.juego.console:
                escribir_lento("¡Un bicho te ha atacado! Tu vida se ha reducido a " + str(objetivo.vida) + "\n")
        else:
            logging.info(f"un bicho no encuentra objetivo para atacar")
    def dormir(self, bicho):
        logging.info(f"un bicho duerme mucho, recuperando vida")
        if bicho.vida < 10:
            bicho.vida += 1

class Personaje(Ente):
    def __init__(self, vida, poder, nombre, juego):
        super().__init__(vida, poder, juego)
        self.nombre = nombre
        self.inventario = []
    def __str__(self):
        return f"Personaje {self.nombre}"
class Director():
    def __init__(self):
        self.builder = None

    def iniBuilder(self):
        if self.data["forma"] == "poligono4":
            self.builder = LaberintoBuilder()
    def construirLaberinto(self):
        if self.builder:
            self.builder.fabricarLaberinto()
            self.builder.fabricarJuego()
            for hijo in self.data["laberinto"]:
                self.fabricarLaberintoRecursivo(0,hijo)
            self.builder.fabricarPuertas(self.data["puertas"])
            self.builder.fabricarBichos(self.data["bichos"])
            self.builder.fabricarPersonaje(self.data["personaje"])

    def construirJuego(self):
        if self.builder:
            self.builder.fabricarJuego()
        else:
            print("No se ha inicializado el builder")
            return None
        
    def obtenerJuego(self):
        if self.builder:
            self.builder.juego
        else:
            print("No se ha inicializado el builder")
            return None

    def fabricarLaberintoRecursivo(self,idp,elemento):
        if elemento["tipo"] == "habitacion":
            self.builder.fabricarHabitacion(elemento["id"],Cuadrado({}))
            for hijos in elemento["hijos"]:
                self.fabricarLaberintoRecursivo(elemento["id"],hijos)
        if elemento["tipo"] == "bomba":
            self.builder.fabricarBomba(idp, elemento["posicion"])
        if elemento["tipo"] == "armario":
            self.builder.fabricarArmario(idp, elemento["posicion"], elemento["objetos"])
        if elemento["tipo"] == "tunel":
            self.builder.fabricarTunel(idp, elemento["posicion"])
        if elemento["tipo"] == "hongo":
            self.builder.fabricarHongo(idp, elemento["posicion"])
        if elemento["tipo"] == "boton":
            self.builder.fabricarBoton(idp, elemento["posicion"])

    def cargarConf(self, path):
        with open(path) as file:
            self.data = json.load(file)

#Es el concreteBuilder del patrón Builder, encargado de construir el laberinto a partir de la información dada por el director.
class LaberintoBuilder:
    def __init__(self):
        self.laberinto = None
        self.juego = None

    def fabricarLaberinto(self):
        self.laberinto = Laberinto(0)
    
    def fabricarJuego(self):
        self.juego = Juego(self.laberinto)
        self.juego.crearPrototipoLaberinto()

    def fabricarHabitacion(self, id, forma=Cuadrado({})):
        habitacion = Habitacion(id, forma)
        for orientacion in habitacion.forma.obtenerOrientacionesDisponiblesLista():
            habitacion.ponerEnOrientacion(orientacion, self.fabricarPared())
        self.laberinto.agregarHijo(id, habitacion)

    def fabricarForma(self, habitacion):
        habitacion.agregarOrientacion(Norte)
        habitacion.agregarOrientacion(Sur)
        habitacion.agregarOrientacion(Este)
        habitacion.agregarOrientacion(Oeste)
    
    def fabricarPared(self):
        pared = Pared()
        pared.comandos.append(explorar(pared))
        return pared
    
    def fabricarBomba(self, idp, orientacion):
        bomba = Bomba(self.fabricarPared())
        bomba.comandos.append(explorar(bomba))
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, bomba)

    def fabricarPuertas(self, puertas):
        for puerta_info in puertas:
            habitacion1 = self.laberinto.obetenerHabitacion(puerta_info[0])
            habitacion2 = self.laberinto.obetenerHabitacion(puerta_info[2])
            puerta = Puerta(habitacion1, habitacion2, abierta=True)
            puerta.comandos.append(Abrir(puerta))
            puerta.comandos.append(Cerrar(puerta))
            puerta.comandos.append(entrar(puerta))
            habitacion1.forma.ponerElemento(habitacion1, puerta_info[1], puerta)
            habitacion2.forma.ponerElemento(habitacion2, puerta_info[3], puerta)
    def fabricarHongo(self, idp, orientacion):
        hongo = Hongo(self.fabricarPared())
        hongo.comandos.append(explorar(hongo))
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, hongo)
    def fabricarBoton(self, idp, orientacion):
        boton = Boton(self.fabricarPared(),self.laberinto)
        boton.comandos.append(pulsar(boton))
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, boton)
    def fabricarArmario(self, idp, orientacion, objetos):
        armario = Armario(0)
        armario.comandos.append(cogerObjeto(armario))
        for objeto in objetos:
            if objeto["tipo"] == "Espada":
                espada = self.fabricarEspada()
                armario.ponerEnOrientacion(objeto["posicion"], espada)
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, armario)
    def fabricarEspada(self):
        espada  = Espada()
        espada.comandos.append(equiparArma(espada))
        espada.comandos.append(desEquiparArma(espada))
        return espada
    
    def fabricarTunel(self, idp, orientacion):
        tunel = Tunel()
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, tunel)

    def fabricarBichos(self, bichos):
        for bicho_info in bichos:
            bicho = Bicho(bicho_info["vida"], bicho_info["poder"], self.fabricarModo(bicho_info["modo"]), self.juego)
            self.juego.agregarBicho(bicho, bicho_info["habitacion"])

    def fabricarModo(self, modo):
        if modo == "agresivo":
            return Agresivo()
        elif modo == "perezoso":
            return Perezoso()
        else:
            print("Modo no reconocido, se asignará el modo perezoso por defecto")
            return Perezoso()
    
    def fabricarPersonaje(self, personaje_info):
        personaje = Personaje(personaje_info["vida"], personaje_info["poder"], personaje_info["nombre"], self.juego)
        self.juego.agregarPersonaje(personaje, personaje_info["habitacion"])

#Juego sigue el patrón Factory Method, siendo el creador
class Juego:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.bichos = []
        self.bichosHilos = []
        self.stopBichos_event = threading.Event()
        self.personaje = None
        self.laberintoPrototipo = None
        self.observers = []
        self.console = False
    
    def attachObserver(self, observer):
        self.observers.append(observer)

    def jugarConsola(self):
        self.console = True
        opcion = ""
        while opcion != "Salir":
            print("----------------------------------------------------------")
            print(self.personaje.ubicadoEn.recorrer(imprimirElemento))

            print("")
            escribir_lento("A donde quieres ir? o escribe Inventario para ver tu inventario",velocidad=0.03)
            opcion = input("")
            opcion = opcion[0].capitalize() + opcion[1:].lower()
            print("")
            if opcion in self.personaje.ubicadoEn.forma.orientaciones or opcion == "Inventario":
                if opcion == "Inventario":
                    escribir_lento("Nombre: " + self.personaje.nombre)
                    escribir_lento("Vida: " + str(self.personaje.vida))
                    inventario = ""
                    for invent in self.personaje.inventario:
                        inventario += str(invent) + " "
                    escribir_lento("Inventario: " + inventario)
                    escribir_lento("Deseas equiparte o desequiparte un Objeto? (Sí - No)")
                    response = input("")
                    response = response[0].capitalize() + response[1:].lower()
                    if response == "Sí":
                        escribir_lento("Que objeto deseas equiparte?")
                        response = input("")
                        response = response[0].capitalize() + response[1:].lower()
                        self.objetoSelec = None
                        self.flagObjeto = False
                        for objeto in self.personaje.inventario:
                            if objeto.__str__() == response:
                                self.objetoSelec = objeto
                                self.flagObjeto = True
                        if not self.flagObjeto:
                            escribir_lento("Objeto no encontrado", velocidad=0.03)
                        else:
                            escribir_lento("¿Qué quieres hacer?", velocidad=0.03)
                            escribir_lento(objeto.listarComandos(), velocidad=0.03)
                            escribir_lento("Selecciona una acción (1..{})".format(len(objeto.listaComandos())), velocidad=0.03)
                            accion = input("")
                            try:   
                                comando = objeto.comandos[int(accion)-1]
                                comando.ejecutar(objeto)
                            except (ValueError, IndexError, KeyError):
                                escribir_lento("Acción no válida", velocidad=0.03)
                                print("")
                                
                else:
                    orientacion = self.personaje.ubicadoEn.forma.orientaciones[opcion]
                    elemento = orientacion.getElemento(self.personaje.ubicadoEn.forma)
                    flagCommando = True
                    while flagCommando:
                        escribir_lento("Te encuentras con " + str(elemento), velocidad=0.03)
                        print("")
                        escribir_lento("¿Qué quieres hacer?", velocidad=0.03)
                        escribir_lento(elemento.listarComandos(), velocidad=0.03)
                        escribir_lento("Selecciona una acción (1..{})".format(len(elemento.listaComandos())), velocidad=0.03)
                        accion = input("")
                        try:   
                            comando = elemento.comandos[int(accion)-1]
                            if isinstance(elemento,Armario):
                                escribir_lento("De donde quieres coger el objeto? (Orientacion)", velocidad=0.03)
                                ori = input("")
                                ori = ori[0].capitalize() + ori[1:].lower()
                                objeto = comando.ejecutar(self.personaje, ori)
                                self.personaje.inventario.append(objeto)
                                escribir_lento("Objeto recogido")
                            else:
                                comando.ejecutar(self.personaje)
                            flagCommando = False
                        except (ValueError, IndexError, KeyError):
                            escribir_lento("Acción no válida", velocidad=0.03)
                            print("")
                            flagCommando = True
                    self.step()
            else:
                escribir_lento("Opción no válida", velocidad=0.03)
            if self.jugadorBuscarObjetivo():
                escribir_lento("Pulsa Enter para continuar...", velocidad=0.03)
                input("")
                limpiar_pantalla()
                escribir_lento("¡Cuidado! Hay un bicho en la habitación, Ataca o Huye", velocidad=0.03)
                opcion = input("")
                opcion = opcion[0].capitalize() + opcion[1:].lower()
                if opcion.startswith("Ataca"):
                    bichos = self.jugadorBuscarObjetivo()
                    if len(bichos) > 1:
                        flagBicho = True
                        while flagBicho:
                            escribir_lento("Hay varios bichos, ¿a cuál quieres atacar? (1..{})".format(len(bichos)), velocidad=0.03)
                            for i in range(len(bichos)):
                                escribir_lento("Bicho {}: Vida {}".format(i+1, bichos[i].vida), velocidad=0.03)
                            opcion = input("")
                            try:
                                bicho_seleccionado = int(opcion)-1
                                if bicho_seleccionado < 0 or bicho_seleccionado >= len(bichos):
                                    escribir_lento("Opción no válida", velocidad=0.03)
                                else:
                                    escribir_lento(self.atacarBicho(bichos[bicho_seleccionado]))
                                    flagBicho = False
                            except ValueError:
                                escribir_lento("Opción no válida", velocidad=0.03)
                    else:
                        escribir_lento(self.atacarBicho(bichos[0]) + f"su vida ahora es {bichos[0].vida}")
            if not self.personaje.estaVivo():
                escribir_lento("FIN DE LA PARTIDA! el personaje ha perecido")
                break
            if self.bichosMuertos():
                limpiar_pantalla()
                print("")
                print("----------------------------------------------------")
                escribir_lento("ENHORABUENA! Has ganadado el juego!")
                print("----------------------------------------------------")
                print("")
            escribir_lento("Pulsa Enter para continuar...", velocidad=0.03)
            input("")
            limpiar_pantalla()
    
    def bichosMuertos(self):
        flagbicho = True
        for bicho in self.bichos:
            if bicho.estaVivo():
                flagbicho = False
        return flagbicho
    
    def obtenerVista(self, vista = "Norte"):
        if vista in self.personaje.ubicadoEn.forma.orientaciones:
            orientacion = self.personaje.ubicadoEn.forma.orientaciones[vista]
            elemento = orientacion.getElemento(self.personaje.ubicadoEn.forma)
        if isinstance(elemento, Puerta):
            self.notifyObservers({"commando": "dibujarPuerta", "elemento": None})
        if isinstance(elemento, Pared):
            self.notifyObservers({"commando": "dibujarPared", "elemento": None})
        if isinstance(elemento, Bomba):
            self.notifyObservers({"commando": "dibujarBomba", "elemento": elemento})
        if isinstance(elemento, Boton):
            self.notifyObservers({"commando": "dibujarBoton", "elemento": elemento})
        if isinstance(elemento, Hongo):
            self.notifyObservers({"commando": "dibujarHongo", "elemento": elemento})
    
    def obtenerOrientacionesDisponibles(self):
        return self.personaje.ubicadoEn.forma.obtenerOrientacionesDisponiblesLista()
    
    def obtenerAccionesDisponibles(self, mirando):
        if mirando in self.personaje.ubicadoEn.forma.orientaciones:
            orientacion = self.personaje.ubicadoEn.forma.orientaciones[mirando]
            elemento = orientacion.getElemento(self.personaje.ubicadoEn.forma)
            lista = []
            for comando in elemento.comandos:
                lista.append(comando.__str__())
            return lista
        else:
            print("Orientación no válida")
            return []
    
    def ejecutarAccion(self, mirando, accion):
        if mirando in self.personaje.ubicadoEn.forma.orientaciones:
            orientacion = self.personaje.ubicadoEn.forma.orientaciones[mirando]
            elemento = orientacion.getElemento(self.personaje.ubicadoEn.forma)
            for comando in elemento.comandos:
                if accion == comando.__str__():
                    resultado =comando.ejecutar(self.personaje)
            self.step()
        else:
            resultado = "Orientación no válida"
        self.notifyObservers({"commando": "resultadoAccion", "mensaje": resultado})
    
    def atacarBicho(self, bicho):
        if self.console:
            if bicho.estaVivo():
                bicho.vida -= self.personaje.poder
                logging.info(f"El personaje ataca a un bicho, reduciendo su vida a {bicho.vida}")
                return "¡Has atacado a un bicho!"
            else:
                return "El bicho ya está muerto"
        bicho = self.bichos[bicho-1]
        if bicho.estaVivo():
            bicho.vida -= self.personaje.poder
            logging.info(f"El personaje ataca a un bicho, reduciendo su vida a {bicho.vida}")
            mensaje = "¡Has atacado a un bicho!"
            mensaje += f" La vida del bicho se ha reducido a {bicho.vida}"
        else:
            mensaje = " ¡Has matado al bicho!"
        self.notifyObservers({"commando": "resultadoAccion", "mensaje": mensaje})
        self.step()
        return bicho.vida
        
    
    def notifyObservers(self, mensaje):
        for observer in self.observers:
            observer.update(mensaje)

    def lanzarBicho(self, bicho, intervalo):
        self.bichosHilos.append(threading.Thread(target=self.lanzarBichoRecursivo, args=(bicho, intervalo, self.stopBichos_event)))
        self.bichosHilos[-1].start()
    
    def detenerBichos(self):
        self.stopBichos_event.set()
        for hilo in self.bichosHilos:
            hilo.join()
    def lanzarBichoRecursivo(self, bicho, intervalo, stop_event):
        while bicho.estaVivo() and not stop_event.is_set():
            bicho.actua()
            time.sleep(intervalo)
    
    def bichoBuscarObjetivo(self, bicho):
        if self.personaje.ubicadoEn == bicho.ubicadoEn:
            return self.personaje
        return False
    def jugadorBuscarObjetivo(self):
        if self.console:
            listaBichos = []
            for bicho in self.bichos:
                if self.personaje.ubicadoEn == bicho.ubicadoEn:
                    listaBichos.append(bicho)
            return listaBichos
        listaBichos = []
        indice = 0
        for bicho in self.bichos:
            indice += 1
            if self.personaje.ubicadoEn == bicho.ubicadoEn:
                listaBichos.append(indice)
        return listaBichos
    def crearPrototipoLaberinto(self):
        self.laberintoPrototipo = copy.deepcopy(self.laberinto)
    
    def agregarPersonaje(self, personaje, habitacion_id=1):
        self.personaje = personaje
        self.personaje.ubicadoEn = self.obtenerHabitacion(habitacion_id).entrar(self.personaje)
        
    
    def agregarBicho(self, bicho, habitacion_id):
        bicho.ubicadoEn = self.obtenerHabitacion(habitacion_id)
        self.bichos.append(bicho)

    def obtenerHabitacion(self, id):
        return self.laberinto.obetenerHabitacion(id)
    
    def fabricarLaberinto(self,id):
        return Laberinto(id)
    
    def abrirPuertas(self):
        def abrirPuertasRecursivo(elemento):
            if isinstance(elemento, Puerta):
                print(f"Abriendo puerta entre {elemento.lado1} y {elemento.lado2}")
                elemento.abrir()
            else:
                print("No es una puerta")
        self.laberinto.recorrer(abrirPuertasRecursivo)
    def step(self):
        for bicho in self.bichos:
            if bicho.estaVivo():
                bicho.actua()
    def getPersonaje(self):
        return self.personaje

class JuegoBombas(Juego):
    def fabricarPared(self):
        return Bomba(super().fabricarPared())

class Decorator(Hoja):
    @abstractmethod
    def __init__(self, elemento):
        self.elemento = elemento
        self.comandos = []
    def listaComandos(self):
        return self.comandos

class Bomba(Decorator):
    def __init__(self, elemento):
        super().__init__(elemento)
        self.activada = True
    def entrar(self, unEnte):
        if self.activada:
            print(f"BOOM! Un {unEnte} ha activado una bomba y ha perdido 5 puntos de vida")
            unEnte.vida -= 5
            self.activada = False
            return "BOOM! Has perdido 5 puntos de vida"
        return self.elemento.entrar(unEnte)
    def __str__(self):
        return self.elemento.__str__()
        
    def aceptar(self, visitor):
        visitor.visitarBomba(self)
class Hongo(Decorator):
    def __init__(self, elemento):
        super().__init__(elemento)
        self.usado = False
    def entrar(self, unEnte):
        if not self.usado:
            print(f"Un {unEnte} ha encontrado un hongo y ha ganado 5 puntos de vida")
            unEnte.vida += 5
            self.usado = True
            return "Has encontrado un hongo y has ganado 5 puntos de vida"
        return self.elemento.entrar(unEnte)
    def __str__(self):
        return self.elemento.__str__()
    def aceptar(self, visitor):
        visitor.visitarHongo(self)

class Boton(Decorator):
    def __init__(self, elemento, laberinto):
        super().__init__(elemento)
        self.laberinto = laberinto
    def entrar(self, unEnte):
        print(f"Un {unEnte} ha presionado un botón y se han abierto todas las puertas del laberinto")
        visitor = visitors.visitorAbrirPuertas()
        self.laberinto.aceptar(visitor)
        return "Se han abierto todas las puertas"
    def __str__(self):
        return self.elemento.__str__() + " con un botón"
    def aceptar(self, visitor):
        visitor.visitarBoton(self)


def load():
    cargarLogging()
    director = Director()
    director.cargarConf("src\laberintos\Lab2Hab.json")
    director.iniBuilder()
    director.construirLaberinto()
    return director

if consola:
    cargarLogging()
    director = Director()
    director.cargarConf("src\laberintos\Lab2Hab.json")
    director.iniBuilder()
    director.construirLaberinto()
    director.builder.juego.jugarConsola()