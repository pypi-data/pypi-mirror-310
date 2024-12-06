import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
import main


class TestMainCLI(unittest.TestCase):
    @patch("main.crear_proyecto")
    def test_crear_proyecto(self, mock_crear_proyecto):
        """
        Prueba el comando 'crear_proyecto' con un nombre válido.
        """
        with patch("sys.argv", ["main.py", "crear_proyecto", "mi_sitio"]):
            main.main()
            mock_crear_proyecto.assert_called_once_with("mi_sitio")

    @patch("main.configurar_sphinx")
    def test_configurar_sphinx(self, mock_configurar_sphinx):
        """
        Prueba el comando 'configurar_sphinx' con un proyecto válido.
        """
        with patch("sys.argv", ["main.py", "configurar_sphinx", "mi_proyecto"]):
            main.main()
            mock_configurar_sphinx.assert_called_once_with("mi_proyecto")

    @patch("main.generar_documentacion")
    def test_generar_documentacion(self, mock_generar_documentacion):
        """
        Prueba el comando 'generar_documentacion' con un proyecto válido.
        """
        with patch("sys.argv", ["main.py", "generar_documentacion", "mi_proyecto"]):
            main.main()
            mock_generar_documentacion.assert_called_once_with("mi_proyecto")

    @patch("main.listar_temas")
    def test_listar_temas(self, mock_listar_temas):
        """
        Prueba el comando 'listar_temas'.
        """
        mock_listar_temas.return_value = ["bootstrap", "tailwind"]
        with patch("sys.argv", ["main.py", "listar_temas"]):
            with patch("builtins.print") as mock_print:
                main.main()
                mock_listar_temas.assert_called_once()
                mock_print.assert_any_call("Temas disponibles:")
                mock_print.assert_any_call("- bootstrap")
                mock_print.assert_any_call("- tailwind")

    @patch("main.aplicar_tema")
    def test_aplicar_tema(self, mock_aplicar_tema):
        """
        Prueba el comando 'aplicar_tema' con un tema válido.
        """
        with patch("sys.argv", ["main.py", "aplicar_tema", "mi_proyecto", "bootstrap"]):
            main.main()
            mock_aplicar_tema.assert_called_once_with("mi_proyecto", "bootstrap")

    def test_comando_invalido(self):
        """
        Prueba la ejecución con un comando no válido.
        """
        with patch("sys.argv", ["main.py", "comando_inexistente"]):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(SystemExit):  # argparse llama a SystemExit
                    main.main()
                # Verifica que el mensaje de error contenga "invalid choice"
                self.assertIn("invalid choice", mock_stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
