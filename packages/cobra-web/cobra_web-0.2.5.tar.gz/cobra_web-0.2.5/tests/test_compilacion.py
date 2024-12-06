import os
import shutil

from estilos.compilacion import compilar_scss
from estilos.personalizacion import editar_variables


def test_compilar_scss():
    """
    Prueba la compilación de SCSS a CSS.
    """
    proyecto = "test_proyecto_compilacion"
    scss_path = os.path.join(proyecto, 'static/scss')
    css_path = os.path.join(proyecto, 'static/css')
    try:
        editar_variables(proyecto)  # Genera un archivo SCSS de prueba
        compilar_scss(proyecto)
        assert os.path.isfile(os.path.join(css_path, 'variables.css'))
    finally:
        # Limpieza del entorno de pruebas
        if os.path.isdir(proyecto):
            shutil.rmtree(proyecto)
