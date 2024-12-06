from generador.admin import crear_superusuario


def test_crear_superusuario():
    """
    (Prueba manual) Verifica que el comando crea correctamente un superusuario.
    """
    try:
        crear_superusuario()
        # Esta prueba debe validarse manualmente al observar la interacción CLI.
    except Exception as e:
        assert False, f"Error durante la prueba de superusuario: {e}"
