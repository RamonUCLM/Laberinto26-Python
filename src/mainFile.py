from abc import ABC, abstractmethod
import json
import random
import copy
import threading
import time
import logging
import subprocess

def cargarLogging():
    logging.basicConfig(level=logging.INFO, filename='juego.log', filemode='w')

#
class ElementoMapa(ABC):
    def __init__(self, id):
        self.id = id
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
    def aceptar(visitor):
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
            forma.norte.recorrer(unBloque)
    def aceptar(self, visitor, forma):
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
        if forma.sur:
            forma.sur.recorrer(unBloque)
    def aceptar(self, visitor, forma):
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
        if forma.este:
            forma.este.recorrer(unBloque)
    def aceptar(self, visitor, forma):
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
        if forma.oeste:
            forma.oeste.recorrer(unBloque)
    def aceptar(self, visitor, forma):
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
    def aceptar(self, visitor, forma):
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
    def aceptar(self, visitor, forma):
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
    def aceptar(self, visitor, forma):
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
    def aceptar(self, visitor, forma):
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
    def visitarContenedor(self, visitor):
        visitor.visitarContenedor(self)
    def aceptar(self, visitor):
        self.visitarContenedor(visitor)
        for hijo in self.hijos:
            hijo.aceptar(visitor)
        for orientacion in self.forma.orientaciones:
            self.forma.orientaciones[orientacion].aceptar(visitor, self.forma)
    

class Armario(Contenedor):
    def __init__(self, id,forma=Cuadrado({})):
        super().__init__(id, forma)
    def entrar(self, unEnte):
        if isinstance(unEnte, Personaje):
            print("Has entrado al armario: ", self.id)
        else:
            logging.info(f"Un {unEnte} entra en el armario: {self.id}")
        return self
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)
    def __str__(self):
        cadena = f"Armario {self.id} con forma {self.forma}"
        return cadena
    def visitarContenedor(self, visitor):
        visitor.visitarArmario(self)

#Habitación es un composite también.
class Habitacion(Contenedor):
    def __init__(self, id, forma=Cuadrado({})):
        super().__init__(id, forma)
    def entrar(self, unEnte):
        if isinstance(unEnte, Personaje):
            print("Has entrado a la habitación: ", self.id)
        else:
            logging.info(f"Un {unEnte} entra en la habitación: {self.id}")
        return self
    
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)

    def __str__(self):
        cadena = f"Habitación {self.id} con forma {self.forma}"
        return cadena
    def visitarContenedor(self, visitor):
        visitor.visitarHabitacion(self)
        

#Hoja sigue el patrón Composite, siendo la hoja
class Hoja(ElementoMapa):
    @abstractmethod
    def __init__(self):
        pass
    def recorrer(self, unBloque):
        unBloque(self)
        
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
        else:
            logging.info(f"Un {unEnte} choca contra una pared en la habitación: {unEnte.ubicadoEn.id}")
    def __str__(self):
        return "Pared"
    def aceptar(self, visitor):
        visitor.visitarPared(self)

class Puerta(Hoja):
    def __init__(self, lado1, lado2, abierta=False):
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
                    print(f"Has pasado por la puerta hacia la habitación {self.lado2.id}")
                else:
                    logging.info(f"Un {unEnte} pasa por la puerta hacia la habitación {self.lado2.id}")
                self.lado2.entrar(unEnte)
                unEnte.ubicadoEn = self.lado2
            elif unEnte.ubicadoEn == self.lado2:
                if isinstance(unEnte, Personaje):
                    print(f"Has pasado por la puerta hacia la habitación {self.lado1.id}")
                else:                    
                    logging.info(f"Un {unEnte} pasa por la puerta hacia la habitación {self.lado1.id}")
                self.lado1.entrar(unEnte)
                unEnte.ubicadoEn = self.lado1
            else:
                raise ValueError("El origen no es válido para esta puerta")
        else:
            if isinstance(unEnte, Personaje):
                print("La puerta está cerrada, no puedes pasar")
            else:
                logging.info(f"Un {unEnte} intenta pasar por una puerta cerrada entre {self.lado1.id} y {self.lado2.id}")
    def abrir(self):
        self.abierta = True
    def cerrar(self):
        self.abierta = False
    def aceptar(self, visitor):
        visitor.visitarPuerta(self)
    def __str__(self):
        estado = "abierta" if self.abierta else "cerrada"
        return f"Puerta {estado} entre {self.lado1.id} y {self.lado2.id}"

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
    def __init__(self, vida, poder):
        self.vida = vida
        self.poder = poder
        self.ubicadoEn = None

    def estaVivo(self):
        return self.vida > 0

class Bicho(Ente):
    def __init__(self, vida, poder, modo):
        super().__init__(vida, poder)
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
        print(f"un bicho se mueve agresivamente hacia la orientación {destino.getOrientacion()}")
        bicho.ubicadoEn = destino.getElemento(bicho.ubicadoEn).entrar(bicho)

    def atacar(self, bicho):
        print(f"un bicho ataca con poder {bicho.poder}")
    def dormir(self, bicho):
        print(f"un bicho no duerme, siempre está listo para atacar")

class Perezoso(Modo):
    def caminar(self, bicho):
        if random.random() < 0.5:
            destino = bicho.ubicadoEn.obtenerOrientacionAleatoria()
            logging.info(f"un bicho se mueve perezosamente hacia la orientación {destino.getOrientacion()}")
            destino.getElemento(bicho.ubicadoEn.forma).entrar(bicho)
        else:
            logging.info("El bicho perezoso decidió no moverse esta vez")
    def atacar(self, bicho):
        logging.info(f"un bicho ataca con poder {bicho.poder // 2}")
    def dormir(self, bicho):
        logging.info(f"un bicho duerme mucho, recuperando vida")
        if bicho.vida < 10:
            bicho.vida += 1

class Personaje(Ente):
    def __init__(self, vida, poder, nombre):
        super().__init__(vida, poder)
        self.nombre = nombre

class Director:
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
            self.builder.fabricarArmario(idp, elemento["posicion"])
        if elemento["tipo"] == "tunel":
            self.builder.fabricarTunel(idp, elemento["posicion"])

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
        return Pared()
    
    def fabricarBomba(self, idp, orientacion):
        bomba = Bomba(self.fabricarPared())
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, bomba)

    def fabricarPuertas(self, puertas):
        for puerta_info in puertas:
            habitacion1 = self.laberinto.obetenerHabitacion(puerta_info[0])
            habitacion2 = self.laberinto.obetenerHabitacion(puerta_info[2])
            puerta = Puerta(habitacion1, habitacion2, abierta=True)
            habitacion1.forma.ponerElemento(habitacion1, puerta_info[1], puerta)
            habitacion2.forma.ponerElemento(habitacion2, puerta_info[3], puerta)
    def fabricarArmario(self, idp, orientacion):
        armario = Armario(0)
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, armario)
    
    def fabricarTunel(self, idp, orientacion):
        tunel = Tunel()
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.forma.ponerElemento(habitacion, orientacion, tunel)

    def fabricarBichos(self, bichos):
        for bicho_info in bichos:
            bicho = Bicho(bicho_info["vida"], bicho_info["poder"], self.fabricarModo(bicho_info["modo"]))
            self.juego.agregarBicho(bicho, bicho_info["habitacion"])

    def fabricarModo(self, modo):
        if modo == "agresivo":
            return Agresivo()
        elif modo == "perezoso":
            return Perezoso()
        else:
            print("Modo no reconocido, se asignará el modo perezoso por defecto")
            return Perezoso()

#Juego sigue el patrón Factory Method, siendo el creador
class Juego:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.bichos = []
        self.bichosHilos = []
        self.stopBichos_event = threading.Event()
        self.personaje = None
        self.laberintoPrototipo = None

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
    def crearPrototipoLaberinto(self):
        self.laberintoPrototipo = copy.deepcopy(self.laberinto)
    
    def agregarPersonaje(self, personaje):
        self.personaje = personaje
        self.personaje.ubicadoEn = self.obtenerHabitacion(1).entrar()
        
    
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

class JuegoBombas(Juego):
    def fabricarPared(self):
        return Bomba(super().fabricarPared())

class Decorator(Hoja):
    @abstractmethod
    def __init__(self, elemento):
        self.elemento = elemento

class Bomba(Decorator):
    def __init__(self, elemento):
        super().__init__(elemento)
        self.activada = False
    def entrar(self, unEnte):
        if self.activada:
            print(f"BOOM! Un {unEnte} ha activado una bomba y ha perdido 5 puntos de vida")
            unEnte.vida -= 5
        self.elemento.entrar(unEnte)
    def __str__(self):
        return self.elemento.__str__() + " con una bomba"
    def aceptar(self, visitor):
        visitor.visitarBomba(self)

#def Jugar():
cargarLogging()
Director = Director()
Director.cargarConf("laberintos/Lab2Hab.json")
Director.iniBuilder()
Director.construirLaberinto()

def imprimirElemento(elemento):
    print(elemento)
def funcionVacia(elemento):
    pass
Director.builder.laberinto.recorrer(imprimirElemento)
Director.builder.juego.bichos[1].actua()

print("Lanzado bichos...")
Director.builder.juego.lanzarBicho(Director.builder.juego.bichos[1], 2)

def abrir_monitor_logs():
    # Usamos powershell para hacer un "tail" del archivo log
    comando = 'Get-Content -Path "juego.log" -Wait'
    # Abrimos una ventana nueva de PowerShell
    subprocess.Popen(['start', 'powershell', '-NoExit', '-Command', comando], shell=True)

abrir_monitor_logs()

input("Presiona Enter para detener los bichos...")
Director.builder.juego.detenerBichos()



