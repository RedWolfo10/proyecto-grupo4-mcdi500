import unittest

import pandas as pd

from src.generar_muestra import anonimizar, generar_muestra
from src.utilidades import seudonimizar


class PrivacidadTests(unittest.TestCase):
    def test_preserva_relaciones_sin_exponer_ids_o_nombres(self):
        original = pd.DataFrame({"host_id": ["12", "12", " 34 ", None],
                                 "host_name": ["A", "A", "B", None]})
        salida, eliminadas = anonimizar(original)
        self.assertEqual(eliminadas, ["host_name"])
        self.assertNotIn("host_name", salida)
        self.assertEqual(salida.loc[0, "host_id"], salida.loc[1, "host_id"])
        self.assertNotEqual(salida.loc[0, "host_id"], salida.loc[2, "host_id"])
        self.assertTrue(salida["host_id"].dropna().str.fullmatch("[a-f0-9]{12}").all())
        self.assertEqual(original.loc[0, "host_id"], "12")

    def test_cada_anonimizacion_genera_mapa_nuevo(self):
        datos = pd.DataFrame({"host_id": [12, 12, 34]})
        a, _ = anonimizar(datos)
        b, _ = anonimizar(datos)
        self.assertNotEqual(a.loc[0, "host_id"], b.loc[0, "host_id"])
        self.assertEqual(seudonimizar(12), seudonimizar(12))

    def test_seleccion_muestral_es_reproducible(self):
        datos = pd.DataFrame({"neighbourhood_cleansed": ["A"] * 50 + ["B"] * 50,
                              "id": range(100)})
        pd.testing.assert_frame_equal(generar_muestra(datos), generar_muestra(datos))
