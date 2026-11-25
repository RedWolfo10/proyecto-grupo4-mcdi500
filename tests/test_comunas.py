import unittest

import pandas as pd

from src.visualizacion import agrupar_comunas, resumen_desempeno


class AgruparComunasTests(unittest.TestCase):
    def test_conserva_limite_y_agrupa_sin_perder_filas(self):
        df = pd.DataFrame({"neighbourhood_cleansed": ["A"] * 30 + ["B"] * 29 + ["C"]})
        original = df.copy(deep=True)
        resultado = agrupar_comunas(df)
        self.assertEqual(resultado["comuna_agrupada"].value_counts().to_dict(),
                         {"A": 30, "Otras comunas": 30})
        pd.testing.assert_frame_equal(df, original)
        self.assertEqual(len(resultado), len(df))

    def test_mediana_se_calcula_sobre_registros(self):
        df = pd.DataFrame({
            "neighbourhood_cleansed": ["A", "B", "B", "B"],
            "estimated_occupancy_l365d": [255, 10, 20, 30],
            "price_clp": [100] * 4,
            "estimated_revenue_l365d": [1000] * 4,
        })
        resultado = resumen_desempeno(agrupar_comunas(df), "comuna_agrupada").iloc[0]
        self.assertEqual(resultado["n"], 4)
        self.assertEqual(resultado["ocupacion_mediana"], 25)
        self.assertEqual(resultado["pct_en_tope"], 0.25)

    def test_sin_comunas_pequenas_no_crea_categoria_ficticia(self):
        df = pd.DataFrame({"neighbourhood_cleansed": ["A"] * 30})
        self.assertNotIn("Otras comunas", agrupar_comunas(df)["comuna_agrupada"].values)

    def test_rechaza_nulos_y_umbral_invalido(self):
        with self.assertRaises(ValueError):
            agrupar_comunas(pd.DataFrame({"neighbourhood_cleansed": [None]}))
        with self.assertRaises(ValueError):
            agrupar_comunas(pd.DataFrame({"neighbourhood_cleansed": ["A"]}), 0)
