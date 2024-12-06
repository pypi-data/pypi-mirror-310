import os
import shutil

from estilos.temas import aplicar_tema, listar_temas


def test_listar_temas():
    """
    Prueba la lista de temas disponibles.
    """
    temas = listar_temas()
    assert len(temas) > 0
    assert "bootstrap" in temas


def test_aplicar_tema():
    """
    Prueba la aplicación de un tema CSS.
    """
    proyecto = "test_proyecto_tema"
    tema = "bootstrap"
    static_path = os.path.join(proyecto, 'static/css')
    try:
        os.makedirs(proyecto, exist_ok=True)
        aplicar_tema(proyecto, tema)
        assert os.path.isfile(os.path.join(static_path, 'theme.css'))
    finally:
        # Limpieza del entorno de pruebas
        if os.path.isdir(proyecto):
            shutil.rmtree(proyecto)
