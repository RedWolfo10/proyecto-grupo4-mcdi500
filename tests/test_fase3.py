import sys
import tracemalloc
import unittest

import pandas as pd

sys.path.insert(0, "src")

from medicion import medir
from transformadores import ImputadorPorGrupo, parsear_amenidades


class ParsearAmenidadesTests(unittest.TestCase):
    def test_acepta_lista_json_y_valores_vacios(self):
        self.assertEqual(parsear_amenidades('["Wifi", "Kitchen"]'), ["Wifi", "Kitchen"])
        self.assertEqual(parsear_amenidades("[]"), [])
        self.assertEqual(parsear_amenidades(None), [])
        self.assertEqual(parsear_amenidades(float("nan")), [])
        self.assertEqual(parsear_amenidades(pd.NA), [])

    def test_rechaza_json_mal_formado_y_contenido_inesperado(self):
        for valor in ('["Wifi"', '{"amenity": "Wifi"}', "[1]"):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    parsear_amenidades(valor)


class ImputadorPorGrupoTests(unittest.TestCase):
    def test_rechaza_columna_completamente_vacia(self):
        datos = pd.DataFrame({
            "accommodates": [1, 2, 3],
            "beds": [None, None, None],
        })
        with self.assertRaisesRegex(ValueError, "no hay valores disponibles"):
            ImputadorPorGrupo("beds", "accommodates").ajustar(datos)


class MedirTests(unittest.TestCase):
    def tearDown(self):
        if tracemalloc.is_tracing():
            tracemalloc.stop()

    def test_devuelve_resultado_tiempo_y_memoria(self):
        resultado, segundos, memoria_mb = medir(lambda: [1, 2, 3])
        self.assertEqual(resultado, [1, 2, 3])
        self.assertGreaterEqual(segundos, 0)
        self.assertGreaterEqual(memoria_mb, 0)
        self.assertFalse(tracemalloc.is_tracing())

    def test_detiene_trazado_si_la_funcion_falla(self):
        def fallar():
            raise ValueError("error de prueba")

        with self.assertRaisesRegex(ValueError, "error de prueba"):
            medir(fallar)
        self.assertFalse(tracemalloc.is_tracing())

    def test_no_interfiere_con_un_trazado_existente(self):
        tracemalloc.start()
        with self.assertRaisesRegex(RuntimeError, "tracemalloc ya activo"):
            medir(lambda: None)
        self.assertTrue(tracemalloc.is_tracing())


if __name__ == "__main__":
    unittest.main()
