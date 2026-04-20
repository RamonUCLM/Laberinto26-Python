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

class visitorAbrirPuerta(Visitor):
    def visitarPuerta(self, puerta):
        puerta.abrir()

