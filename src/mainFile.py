from abc import ABC, abstractmethod

#
class ElementoMapa(ABC):
    def __init__(self, id):
        self.id = id
    @abstractmethod
    def entrar(self):
        pass

#Contenedor sigue el patrón Composite, siendo el composite
class Contenedor(ElementoMapa):
    def __init__(self, id):
        super().__init__(id)
        self.hijos = []
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
    def agregarHijo(self, posicion,elemento):
        self.hijos.insert(posicion, elemento)
    def eliminarHijo(self, posicion):
        try:
            self.hijos.pop(posicion)
        except IndexError:
            print("La posición no existe en la lista de hijos")

#Habitación es un composite también.
class Habitacion(Contenedor):
    def __init__(self, id):
        super().__init__(id)
    def setNorte(self, elemento):
        self.norte = elemento
    def setSur(self, elemento):
        self.sur = elemento
    def setEste(self, elemento):
        self.este = elemento
    def setOeste(self, elemento):
        self.oeste = elemento
    def entrar(self):
        print("Has entrado a la habitación: ", self.id)
    
    def __str__(self):
        return f"La habitación {self.id} contiene: Norte: {self.norte}, Sur: {self.sur}, Este: {self.este}, Oeste: {self.oeste}"

#Hoja sigue el patrón Composite, siendo la hoja
class Hoja(ElementoMapa):
    @abstractmethod
    def __init__(self):
        pass

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
    def entrar(self):
        if self.abierta:
            print("Has pasado por la puerta")
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
    def obetenerHabitacion(self, id):
        for hijo in self.hijos:
            if isinstance(hijo, Habitacion) and hijo.id == id:
                return hijo
        print("No se encontró la habitación con id: ", id)
        return None




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

#Juego sigue el patrón Factory Method, siendo el creador
class Juego:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.bichos = []

    def obtenerHabitacion(self, id):
        return self.laberinto.obetenerHabitacion(id)

    def fabricarLab2Hab(self):

        habitacion1 = self.fabricarHabitacion(1)
        habitacion2 = self.fabricarHabitacion(2)
        puerta = self.fabricarPuertaAbierta(habitacion1.id, habitacion2.id)

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
    
    def fabricarLab4Hab(self):
        habitacion1 = self.fabricarHabitacion(1)
        habitacion2 = self.fabricarHabitacion(2)
        habitacion3 = self.fabricarHabitacion(3)
        habitacion4 = self.fabricarHabitacion(4)

        puerta12 = self.fabricarPuertaAbierta(habitacion1.id, habitacion2.id) 
        puerta13 = self.fabricarPuertaCerrada(habitacion1.id, habitacion3.id)
        puerta24 = self.fabricarPuertaCerrada(habitacion2.id, habitacion4.id)
        puerta34 = self.fabricarPuertaAbierta(habitacion3.id, habitacion4.id)

        habitacion1.setSur(puerta12)
        habitacion2.setNorte(puerta12)

        habitacion1.setEste(puerta13)
        habitacion3.setOeste(puerta13)

        habitacion2.setEste(puerta24)
        habitacion4.setOeste(puerta24)

        habitacion3.setSur(puerta34)
        habitacion4.setNorte(puerta34)

        for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
            for direccion in ['Norte', 'Sur', 'Este', 'Oeste']:
                if getattr(habitacion, direccion.lower()) is None:
                    setattr(habitacion, direccion.lower(), self.fabricarPared())

        

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


juego = Juego(Laberinto(0))

juego.fabricarLab2Hab()

for habitacion in juego.laberinto.hijos:
    print(habitacion)

juego.obtenerHabitacion(1).sur.entrar()

bicho = Bicho("Gusano", 100, 20, Agresivo())
bicho.actua()