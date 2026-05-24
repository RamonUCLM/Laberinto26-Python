class Visitor():
    def visitarArmario(self, armario):
        pass
    def visitarBomba(self, bomba):
        pass
    def visitarHabitacion(self, habitacion):
        pass
    def visitarPuerta(self, puerta):
        pass
    def visitarTunel(self, tunel):
        pass
    def visitarPared(self, pared):
        pass
    def visitarPersonaje(self, personaje):
        pass
    def visitarBoton(self, boton):
        pass
    def visitarHongo(self, hongo):
        pass
    def visitarEspada(self, espada):
        pass

class visitorAbrirPuertas(Visitor):
    def visitarPuerta(self, puerta):
        puerta.abrir()

