from abc import ABC, abstractmethod
import json
import random

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

#Singleton para las orientaciones, ya que cada orientación es única en el mapa.
class Orientacion(ABC):
    elemento = None
    @abstractmethod
    def getOrientacion(self):
        pass

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
    def ponerElemento(contenedor, elemento):
        if contenedor.norte:
            print(f"Sustituyendo un elemento {contenedor.norte} por {elemento} en la orientación Norte")
            contenedor.norte = elemento
        else:
            contenedor.norte = elemento
    @staticmethod
    def quitarElemento(contenedor):
        if contenedor.norte:
            contenedor.norte = None
    @staticmethod
    def getElemento(contenedor):
        return contenedor.norte
    @staticmethod
    def recorrer(contenedor, unBloque):
        if contenedor.norte:
            contenedor.norte.recorrer(unBloque)

class Sur(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Sur"
    @staticmethod
    def ponerElemento(contenedor, elemento):
        if contenedor.sur:
            print(f"Sustituyendo un elemento {contenedor.sur} por {elemento} en la orientación Sur")
            contenedor.sur = elemento
        else:
            contenedor.sur = elemento
    @staticmethod
    def quitarElemento(contenedor):
        if contenedor.sur:
            contenedor.sur = None
    @staticmethod
    def getElemento(contenedor):
        return contenedor.sur
    @staticmethod
    def recorrer(contenedor, unBloque):
        if contenedor.sur:
            contenedor.sur.recorrer(unBloque)

class Este(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Este"
    @staticmethod
    def ponerElemento(contenedor, elemento):
        if contenedor.este:
            print(f"Sustituyendo un elemento {contenedor.este} por {elemento} en la orientación Este")
            contenedor.este = elemento
        else:
            contenedor.este = elemento
    @staticmethod
    def quitarElemento(contenedor):
        if contenedor.este:
            contenedor.este = None
    @staticmethod
    def getElemento(contenedor):
        return contenedor.este
    @staticmethod
    def recorrer(contenedor, unBloque):
        if contenedor.este:
            contenedor.este.recorrer(unBloque)
    
class Oeste(Orientacion):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Esta clase no se puede instanciar")
    @staticmethod
    def getOrientacion():
        return "Oeste"
    @staticmethod
    def ponerElemento(contenedor, elemento):
        if contenedor.oeste:
            print(f"Sustituyendo un elemento {contenedor.oeste} por {elemento} en la orientación Oeste")
            contenedor.oeste = elemento
        else:
            contenedor.oeste = elemento
    @staticmethod
    def quitarElemento(contenedor):
        if contenedor.oeste:
            contenedor.oeste = None
    @staticmethod
    def getElemento(contenedor):
        return contenedor.oeste
    @staticmethod
    def recorrer(contenedor, unBloque):
        if contenedor.oeste:
            contenedor.oeste.recorrer(unBloque)

#Patrón Bridge para las formas de las habitaciones, ya que cada forma puede tener diferentes implementaciones de las orientaciones.
class Forma(ABC):
    @abstractmethod
    def __init__(self, orientaciones):
        self.orientaciones = orientaciones
        pass
    @abstractmethod
    def __str__(self):
        pass

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
    def __str__(self):
        return "Cuadrado"

#Contenedor sigue el patrón Composite, siendo el composite.
class Contenedor(ElementoMapa):

    def __init__(self, id, forma):
        super().__init__(id)
        self.hijos = []
        self.forma = forma

    def obtenerOrientacionAleatoria(self):
        self.forma.obtenerOrientacionAleatoria()

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

class Armario(Contenedor):
    def __init__(self, id,forma=Cuadrado({})):
        super().__init__(id, forma)
    def entrar(self, unEnte):
        print("Has entrado al armario: ", self.id)
        return self
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)
    def __str__(self):
        cadena = f"Armario {self.id} con forma {self.forma}"
        return cadena

#Habitación es un composite también.
class Habitacion(Contenedor):
    def __init__(self, id, forma=Cuadrado({})):
        super().__init__(id, forma)
    def entrar(self, unEnte):
        print("Has entrado a la habitación: ", self.id)
    
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        self.forma.recorrer(self, unBloque)

    def __str__(self):
        cadena = f"Habitación {self.id} con forma {self.forma}"
        return cadena
        

#Hoja sigue el patrón Composite, siendo la hoja
class Hoja(ElementoMapa):
    @abstractmethod
    def __init__(self):
        pass
    def recorrer(self, unBloque):
        unBloque(self)
        

class Pared(Hoja):
    def __init__(self):
        super().__init__()
    def entrar(self, unEnte):
        print("Has chocado contra una pared")
    def __str__(self):
        return "Pared"

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
                print(f"Has pasado por la puerta hacia la habitación {self.lado2.id}")
                self.lado2.entrar(unEnte)
                unEnte.ubicadoEn = self.lado2
            elif unEnte.ubicadoEn == self.lado2:
                print(f"Has pasado por la puerta hacia la habitación {self.lado1}")
                self.lado1.entrar(unEnte)
                unEnte.ubicadoEn = self.lado1
            else:
                raise ValueError("El origen no es válido para esta puerta")
        else:
            print("La puerta está cerrada")
    def abrir(self):
        self.abierta = True
    def cerrar(self):
        self.abierta = False
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
            print(f"un bicho se mueve perezosamente hacia la orientación {destino.getOrientacion()}")
            bicho.ubicadoEn = destino.getElemento(bicho.ubicadoEn).entrar(bicho)
        else:
            print(f"el bicho perezoso decide no moverse esta vez")
    def atacar(self, bicho):
        print(f"un bicho ataca con poder {bicho.poder // 2}")
    def dormir(self, bicho):
        print(f"un bicho duerme mucho, recuperando vida")
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
        self.personaje = None
    
    def agregarPersonaje(self, personaje):
        self.personaje = personaje
        self.personaje.ubicadoEn = self.obtenerHabitacion(1).entrar()
        
    
    def agregarBicho(self, bicho, habitacion_id):
        bicho.ubicadoEn = self.obtenerHabitacion(habitacion_id)
        self.bichos.append(bicho)

    def obtenerHabitacion(self, id):
        return self.laberinto.obetenerHabitacion(id)

    def fabricarLab2HabCuadradas(self):

        habitacion1 = self.fabricarHabitacion(1)
        habitacion2 = self.fabricarHabitacion(2)
        puerta = self.fabricarPuertaAbierta(habitacion1.id, habitacion2.id)
        #Deprecated, ahora se agregan las orientaciones directamente en la forma de la habitación.
        #for habitacion in [habitacion1, habitacion2]:
        #    habitacion.agregarOrientacion(Norte)
        #    habitacion.agregarOrientacion(Sur)
        #    habitacion.agregarOrientacion(Este)
        #    habitacion.agregarOrientacion(Oeste)
        #
        #habitacion1.setSur(puerta)
        #habitacion2.setNorte(puerta)

        #habitacion1.setNorte(self.fabricarPared())
        #habitacion1.setEste(self.fabricarPared())
        #habitacion1.setOeste(self.fabricarPared())

        #habitacion2.setSur(self.fabricarPared())
        #habitacion2.setEste(self.fabricarPared())
        #habitacion2.setOeste(self.fabricarPared())

        self.laberinto.agregarHijo(habitacion1.id,habitacion1)
        self.laberinto.agregarHijo(habitacion2.id,habitacion2)
    
    def fabricarLab4HabCuadradas(self):
        habitacion1 = self.fabricarHabitacion(1)
        habitacion2 = self.fabricarHabitacion(2)
        habitacion3 = self.fabricarHabitacion(3)
        habitacion4 = self.fabricarHabitacion(4)

        puerta12 = self.fabricarPuertaAbierta(habitacion1.id, habitacion2.id) 
        puerta13 = self.fabricarPuertaCerrada(habitacion1.id, habitacion3.id)
        puerta24 = self.fabricarPuertaCerrada(habitacion2.id, habitacion4.id)
        puerta34 = self.fabricarPuertaAbierta(habitacion3.id, habitacion4.id)

        #for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
        #    habitacion.agregarOrientacion(Norte)
        #    habitacion.agregarOrientacion(Sur)
        #    habitacion.agregarOrientacion(Este)
        #    habitacion.agregarOrientacion(Oeste)

        # habitacion1.setSur(puerta12)
        # habitacion2.setNorte(puerta12)

        # habitacion1.setEste(puerta13)
        # habitacion3.setOeste(puerta13)

        # habitacion2.setEste(puerta24)
        # habitacion4.setOeste(puerta24)

        # habitacion3.setSur(puerta34)
        # habitacion4.setNorte(puerta34)

        # for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
        #     for orientacion in habitacion.orientaciones:
        #         habitacion.orientaciones[orientacion].ponerElemento(habitacion, self.fabricarPared())

        

        self.laberinto.agregarHijo(habitacion1.id,habitacion1)
        self.laberinto.agregarHijo(habitacion2.id,habitacion2)
        self.laberinto.agregarHijo(habitacion3.id,habitacion3)
        self.laberinto.agregarHijo(habitacion4.id,habitacion4)
    
    def fabricarPared(self):
        return Pared()
    
    def fabricarHabitacion(self, id):
        return Habitacion(id)
    
    def fabricarPuertaCerrada(self, lado1, lado2):
        return Puerta(lado1, lado2, abierta=False)
    
    def fabricarPuertaAbierta(self, lado1, lado2):
        return Puerta(lado1, lado2, abierta=True)
    
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
    def entrar(self):
        if self.activada:
            print("BOOM! Has activado una bomba")
        self.elemento.entrar()
    def __str__(self):
        return self.elemento.__str__() + " con una bomba"


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