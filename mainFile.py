from abc import ABC, abstractmethod


class ElementoMapa(ABC):
    @abstractmethod
    def entrar(self):
        pass

class Habitacion(ElementoMapa):
    def __init__(self):
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
    def setNorte(self, elemento):
        self.norte = elemento
    def setSur(self, elemento):
        self.sur = elemento
    def setEste(self, elemento):
        self.este = elemento
    def setOeste(self, elemento):
        self.oeste = elemento
    def entrar(self):
        print("Has entrado a la habitación")

class Pared(ElementoMapa):
    def entrar(self):
        print("Has chocado contra una pared")

class Puerta(ElementoMapa):
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
    def entrar(self):
        if self.abierta:
            print("Has pasado por la puerta")
        else:
            print("La puerta está cerrada")

class Laberinto(ElementoMapa):
    def __init__(self):
        self.habitaciones = []
    def agregarHabitacion(self, habitacion):
        self.habitaciones.append(habitacion)
    def entrar(self):
        print("Has entrado al laberinto")

class Juego:
    def __init__(self, laberinto):
        self.laberinto = laberinto

class Decorator(ElementoMapa):
    @abstractmethod
    def __init__(self, elemento):
        self.elemento = elemento

class Bomba(Decorator):
    def __init__(self, elemento):
        super().__init__(elemento)
    def entrar(self):
        print("BOOM! Has activado una bomba")
        self.elemento.entrar()


