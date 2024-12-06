import os
import shutil

from generador.sphinx import configurar_sphinx, generar_documentacion


def test_configurar_sphinx():
    """
    Prueba la configuración de Sphinx.
    """
    proyecto = "test_proyecto_sphinx"
    docs_path = os.path.join(proyecto, 'docs')
    try:
        # Crear un directorio temporal para el proyecto
        os.makedirs(proyecto, exist_ok=True)
        configurar_sphinx(proyecto)
        assert os.path.isdir(docs_path)
    finally:
        # Limpiar el entorno de prueba
        if os.path.isdir(proyecto):
            shutil.rmtree(proyecto)


def test_generar_documentacion():
    """
    Prueba la generación de documentación.
    """
    proyecto = "test_proyecto_docs"
    docs_path = os.path.join(proyecto, 'docs')
    try:
        # Configurar Sphinx y luego generar documentación
        os.makedirs(proyecto, exist_ok=True)
        configurar_sphinx(proyecto)
        generar_documentacion(proyecto)
        assert os.path.isdir(os.path.join(docs_path, '_build/html'))
    finally:
        # Limpieza
        if os.path.isdir(proyecto):
            shutil.rmtree(proyecto)
