import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import mainFile

CONFIG_PATH = ROOT / "src" / "laberintos" / "Lab2Hab.json"


class DummyObserver:
    def __init__(self):
        self.messages = []

    def update(self, mensaje):
        self.messages.append(mensaje)


@pytest.fixture(scope="session")
def director_configurado():
    mainFile.cargarLogging()
    director = mainFile.Director()
    director.cargarConf(str(CONFIG_PATH))
    director.iniBuilder()
    director.construirLaberinto()
    return director


@pytest.fixture(scope="session")
def juego(director_configurado):
    return director_configurado.builder.juego


def test_director_loads_configuration(director_configurado):
    assert hasattr(director_configurado, "data")
    assert director_configurado.data["forma"] == "poligono4"
    assert len(director_configurado.data["laberinto"]) == 4


def test_builder_creates_laberinto_and_juego(director_configurado):
    assert director_configurado.builder is not None
    assert director_configurado.builder.laberinto is not None
    assert director_configurado.builder.juego is not None


def test_laberinto_contains_expected_rooms(director_configurado):
    laberinto = director_configurado.builder.laberinto
    assert len(laberinto.hijos) == 4
    habitacion1 = laberinto.obetenerHabitacion(1)
    assert habitacion1 is not None
    assert habitacion1.forma.obtenerOrientacionesDisponiblesLista() == ["Norte", "Sur", "Este", "Oeste"]


def test_personaje_is_added_to_first_room(juego):
    personaje = juego.personaje
    assert personaje is not None
    assert personaje.nombre == "Heroe"
    assert personaje.ubicadoEn.id == 1


def test_bichos_are_created_with_expected_modos(juego):
    assert len(juego.bichos) == 3
    assert isinstance(juego.bichos[0].modo, mainFile.Agresivo)
    assert isinstance(juego.bichos[1].modo, mainFile.Perezoso)
    assert isinstance(juego.bichos[2].modo, mainFile.Perezoso)


def test_obtener_orientaciones_disponibles_returns_four(juego):
    orientaciones = juego.obtenerOrientacionesDisponibles()
    assert set(orientaciones) == {"Norte", "Sur", "Este", "Oeste"}


def test_obtener_acciones_disponibles_for_norte_returns_explorar(juego):
    acciones = juego.obtenerAccionesDisponibles("Norte")
    assert acciones == ["Explorar"]


def test_ejecutar_accion_explorar_norte_detonates_bomba_and_notifies_observer(juego):
    personaje = juego.personaje
    original_vida = personaje.vida
    observer = DummyObserver()
    juego.attachObserver(observer)

    juego.ejecutarAccion("Norte", "Explorar")

    assert personaje.vida == original_vida - 5
    assert observer.messages[-1]["commando"] == "resultadoAccion"
    assert "BOOM" in observer.messages[-1]["mensaje"] or "Has perdido" in observer.messages[-1]["mensaje"]


def test_obtener_vista_notifies_observer_for_bomba(juego):
    observer = DummyObserver()
    juego.attachObserver(observer)
    juego.obtenerVista("Norte")

    assert observer.messages[-1]["commando"] == "dibujarBomba"
    assert isinstance(observer.messages[-1]["elemento"], mainFile.Bomba)


def test_abrir_puertas_can_open_all_doors(juego):
    laberinto = juego.laberinto
    puertas = []
    for elemento in laberinto.hijos:
        for nombre, orientacion in elemento.forma.orientaciones.items():
            item = orientacion.getElemento(elemento.forma)
            if isinstance(item, mainFile.Puerta):
                puertas.append(item)

    for puerta in puertas:
        puerta.cerrar()
        assert not puerta.abierta

    juego.abrirPuertas()

    assert all(puerta.abierta for puerta in puertas)


def test_atacar_bicho_reduces_health_and_notifies_observer(juego):
    observer = DummyObserver()
    juego.attachObserver(observer)
    vida_inicial = juego.bichos[0].vida

    resultado = juego.atacarBicho(1)

    assert resultado == vida_inicial - juego.personaje.poder
    assert observer.messages[-1]["commando"] == "resultadoAccion"
    assert "Has atacado a un bicho" in observer.messages[-1]["mensaje"]


def test_armario_contains_espada_and_coger_objecto_removes_it(juego):
    habitacion2 = juego.obtenerHabitacion(2)
    armario = habitacion2.forma.orientaciones["Sur"].getElemento(habitacion2.forma)
    assert isinstance(armario, mainFile.Armario)

    espada = armario.forma.orientaciones["Sur"].getElemento(armario.forma)
    assert isinstance(espada, mainFile.Espada)

    comando_coger = armario.listaComandos()[0]
    objeto_recogido = comando_coger.ejecutar(juego.personaje, "Sur")
    assert isinstance(objeto_recogido, mainFile.Espada)
    assert armario.forma.orientaciones["Sur"].getElemento(armario.forma) is None


def test_coger_objeto_equipar_y_desequipar_actualiza_estado_correctamente(juego):
    espada = mainFile.Espada()
    equipar = mainFile.equiparArma(espada)
    desequipar = mainFile.desEquiparArma(espada)

    resultado_equipar = equipar.ejecutar(espada)
    assert resultado_equipar == "Te has equipado el arma"
    assert espada.equipada is True

    resultado_desequipar = desequipar.ejecutar(espada)
    assert resultado_desequipar == "Te has desequipado el arma"
    assert espada.equipada is False


