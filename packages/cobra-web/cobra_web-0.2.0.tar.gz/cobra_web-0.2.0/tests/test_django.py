import os
import shutil

from generador.django import crear_proyecto


def test_crear_proyecto():
    """
    Prueba la creación de un proyecto Django.
    """
    nombre = "test_proyecto"
    try:
        crear_proyecto(nombre)
        assert os.path.isdir(nombre)
        assert os.path.isfile(os.path.join(nombre, "manage.py"))
    finally:
        # Limpieza del entorno de pruebas
        if os.path.isdir(nombre):
            shutil.rmtree(nombre)
