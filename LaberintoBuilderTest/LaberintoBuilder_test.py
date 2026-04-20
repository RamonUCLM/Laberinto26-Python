import subprocess

import pytest
import mainFile

def abrir_monitor_logs():
    mainFile.cargarLogging()
    # Usamos powershell para hacer un "tail" del archivo log
    comando = 'Get-Content -Path "juego.log" -Wait'
    # Abrimos una ventana nueva de PowerShell
    subprocess.Popen(['start', 'powershell', '-NoExit', '-Command', comando], shell=True)

@pytest.fixture(scope="session")
def director_configurado():
    abrir_monitor_logs()
    mainFile.cargarLogging()
    director = mainFile.Director()
    director.cargarConf("laberintos/Lab2Hab.json")
    director.iniBuilder()
    director.construirLaberinto()
    yield director

def test_JuegoNull(director_configurado):
    assert director_configurado.builder.juego is not None

def test_LaberintoNull(director_configurado):
    assert director_configurado.builder.laberinto is not None


