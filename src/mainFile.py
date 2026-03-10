from abc import ABC, abstractmethod
import json

#
class ElementoMapa(ABC):
    def __init__(self, id):
        self.id = id
    @abstractmethod
    def entrar(self):
        pass
    @abstractmethod
    def recorrer(self):
        pass

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
            print(f"Sustituyendo elemento en la orientación Norte")
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
            print(f"Sustituyendo elemento en la orientación Sur")
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
            print(f"Sustituyendo elemento en la orientación Este")
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
            print(f"Sustituyendo elemento en la orientación Oeste")
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

#Contenedor sigue el patrón Composite, siendo el composite.
class Contenedor(ElementoMapa):

    def __init__(self, id):
        super().__init__(id)
        self.hijos = []
        self.orientaciones = {}
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None

    def agregarOrientacion(self, orientacion):
        self.orientaciones[orientacion.getOrientacion()] = orientacion
    def setNorte(self, elemento):
        self.orientaciones["Norte"].ponerElemento(self, elemento)
    def setSur(self, elemento):
        self.orientaciones["Sur"].ponerElemento(self, elemento)
    def setEste(self, elemento):
        self.orientaciones["Este"].ponerElemento(self, elemento)
    def setOeste(self, elemento):
        self.orientaciones["Oeste"].ponerElemento(self, elemento)
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
        print("Recorriendo este contenedor: ", self.id)
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)

class Armario(Contenedor):
    def __init__(self, id):
        super().__init__(id)
    def entrar(self):
        print("Has entrado al armario: ", self.id)
        return self
    def recorrer(self, unBloque):
        print("Recorriendo este contenedor: ", self.id)
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)

#Habitación es un composite también.
class Habitacion(Contenedor):
    def __init__(self, id):
        super().__init__(id)
    def entrar(self):
        print("Has entrado a la habitación: ", self.id)
        return self
    
    def recorrer(self, unBloque):
        print("Recorriendo la habitación: ", self.id)
        unBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(unBloque)
        for orientacion in self.orientaciones:
            self.orientaciones[orientacion].recorrer(self, unBloque)

    def __str__(self):
        cadena = f"Habitación {self.id} con las siguientes orientaciones:\n"
        for orientacion in self.orientaciones:
            if self.orientaciones[orientacion].getElemento(self):
                cadena += f"En la orientación {orientacion} hay un elemento: {self.orientaciones[orientacion].getElemento(self)}\n"
            else:
                cadena += f"En la orientación {orientacion} no hay ningún elemento\n"
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
    def entrar(self):
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
    def entrar(self, origen):
        if self.abierta:
            print("Has pasado por la puerta")
            if origen == self.lado1:
                return self.lado2
            elif origen == self.lado2:
                return self.lado1
            raise ValueError("El origen no es válido para esta puerta")
        else:
            print("La puerta está cerrada")
    def abrir(self):
        self.abierta = True
    def cerrar(self):
        self.abierta = False
    def __str__(self):
        estado = "abierta" if self.abierta else "cerrada"
        return f"Puerta {estado} entre {self.lado1} y {self.lado2}"

class Laberinto(Contenedor):
    def __init__(self, id):
        super().__init__(id)
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


class Bicho():
    def __init__(self, tipo, vida, poder, modo):
        self.tipo = tipo
        self.vida = vida
        self.poder = poder
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
        print(f"{bicho.tipo} se mueve agresivamente")
    def atacar(self, bicho):
        print(f"{bicho.tipo} ataca con poder {bicho.poder}")
    def dormir(self, bicho):
        print(f"{bicho.tipo} no duerme, siempre está listo para atacar")

class Perezoso(Modo):
    def caminar(self, bicho):
        print(f"{bicho.tipo} se mueve perezosamente")
    def atacar(self, bicho):
        print(f"{bicho.tipo} ataca con poder {bicho.poder // 2}")
    def dormir(self, bicho):
        print(f"{bicho.tipo} duerme mucho, recuperando vida")
        bicho.vida += 10

class Director:
    def __init__(self):
        self.builder = None

    def iniBuilder(self):
        if self.data["forma"] == "poligono4":
            self.builder = LaberintoBuilder()
    def construirLaberinto(self):
        if self.builder:
            self.builder.fabricarLaberinto()
            for hijo in self.data["laberinto"]:
                self.fabricarLaberintoRecursivo(0,hijo)
            self.builder.fabricarPuertas(self.data["puertas"])
    
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
            self.builder.fabricarHabitacion(elemento["id"])
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

    def fabricarHabitacion(self, id):
        habitacion = Habitacion(id)
        self.fabricarForma(habitacion)
        for orientacion in habitacion.orientaciones:
            habitacion.orientaciones[orientacion].ponerElemento(habitacion, self.fabricarPared())
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
        habitacion.orientaciones[orientacion].ponerElemento(habitacion, bomba)

    def fabricarPuertas(self, puertas):
        for puerta_info in puertas:
            habitacion1 = self.laberinto.obetenerHabitacion(puerta_info[0])
            habitacion2 = self.laberinto.obetenerHabitacion(puerta_info[2])
            puerta = Puerta(habitacion1.id, habitacion2.id, abierta=True)
            habitacion1.orientaciones[puerta_info[1]].ponerElemento(habitacion1, puerta)
            habitacion2.orientaciones[puerta_info[3]].ponerElemento(habitacion2, puerta)
    def fabricarArmario(self, idp, orientacion):
        armario = Armario(0)
        habitacion = self.laberinto.obetenerHabitacion(idp)
        habitacion.orientaciones[orientacion].ponerElemento(habitacion, armario)

#Juego sigue el patrón Factory Method, siendo el creador
class Juego:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.bichos = []

    def obtenerHabitacion(self, id):
        return self.laberinto.obetenerHabitacion(id)

    def fabricarLab2HabCuadradas(self):

        habitacion1 = self.fabricarHabitacion(1)
        habitacion2 = self.fabricarHabitacion(2)
        puerta = self.fabricarPuertaAbierta(habitacion1.id, habitacion2.id)

        for habitacion in [habitacion1, habitacion2]:
            habitacion.agregarOrientacion(Norte)
            habitacion.agregarOrientacion(Sur)
            habitacion.agregarOrientacion(Este)
            habitacion.agregarOrientacion(Oeste)

        habitacion1.setSur(puerta)
        habitacion2.setNorte(puerta)

        habitacion1.setNorte(self.fabricarPared())
        habitacion1.setEste(self.fabricarPared())
        habitacion1.setOeste(self.fabricarPared())

        habitacion2.setSur(self.fabricarPared())
        habitacion2.setEste(self.fabricarPared())
        habitacion2.setOeste(self.fabricarPared())

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

        for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
            habitacion.agregarOrientacion(Norte)
            habitacion.agregarOrientacion(Sur)
            habitacion.agregarOrientacion(Este)
            habitacion.agregarOrientacion(Oeste)

        habitacion1.setSur(puerta12)
        habitacion2.setNorte(puerta12)

        habitacion1.setEste(puerta13)
        habitacion3.setOeste(puerta13)

        habitacion2.setEste(puerta24)
        habitacion4.setOeste(puerta24)

        habitacion3.setSur(puerta34)
        habitacion4.setNorte(puerta34)

        for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
            for orientacion in habitacion.orientaciones:
                habitacion.orientaciones[orientacion].ponerElemento(habitacion, self.fabricarPared())

        

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
Director.builder.laberinto.recorrer(imprimirElemento)