import os
import shutil

from estilos.personalizacion import editar_variables


def test_editar_variables():
    """
    Prueba la generación de un archivo de variables SCSS.
    """
    proyecto = "test_proyecto_scss"
    scss_path = os.path.join(proyecto, 'static/scss')
    variables_file = os.path.join(scss_path, 'variables.scss')
    try:
        editar_variables(proyecto)
        assert os.path.isfile(variables_file)
    finally:
        # Limpieza del entorno de pruebas
        if os.path.isdir(proyecto):
            shutil.rmtree(proyecto)
