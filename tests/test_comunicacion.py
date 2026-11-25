import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src import comunicacion as com
from src.visualizacion import comparar_amenidades, comparar_por_estratos, resumir_estratos


class ComunicacionTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def datos(self):
        return pd.DataFrame({
            "id": range(34), "neighbourhood_cleansed": ["A"] * 30 + ["B"] * 4,
            "estimated_occupancy_l365d": list(range(34)),
            "price_clp": [1000] * 34, "estimated_revenue_l365d": [10000] * 34,
            "bedrooms": [1] * 34, "banos_numero": [1] * 34, "accommodates": [2] * 34,
        })

    def test_copia_interpretable_y_cuartiles(self):
        original = self.datos()
        datos = com.preparar_visual(original)
        self.assertNotIn("comuna_agrupada", original)
        tabla = com.tabla_comunas(datos)
        self.assertEqual(tabla["n"].sum(), 34)
        self.assertIn("precio_q1", tabla)
        self.assertIn("ingresos_q3", tabla)
        self.assertEqual(tabla.set_index("comuna_agrupada").loc["Otras comunas", "n"], 4)

    def test_figura_cantidad_no_dibuja_otras_y_informa_exclusion(self):
        datos = com.preparar_visual(self.datos())
        figuras = com.figuras_comunas(datos, com.tabla_comunas(datos))
        fig = figuras["fig1_cantidad_alojamientos_comuna"]
        self.assertEqual(len(fig.axes[0].patches), 1)
        self.assertNotIn("Otras comunas", [t.get_text() for t in fig.axes[0].get_yticklabels()])
        self.assertIn("4 alojamientos", " ".join(t.get_text() for t in fig.texts))

    def test_rechaza_id_repetido_y_datos_sin_columnas(self):
        with self.assertRaises(KeyError):
            com.preparar_visual(pd.DataFrame())
        with self.assertRaises(ValueError):
            com.preparar_visual(self.datos().assign(id=1))

    def test_extremos_no_producen_intervalo_de_ancho_cero(self):
        datos = pd.DataFrame({"amen_wifi": [1] * 20 + [0] * 20,
                              "estimated_occupancy_l365d": [200] * 20 + [50] * 20})
        mascara = pd.Series([True] * 20 + [False] * 20)
        r = comparar_amenidades(datos, mascara).iloc[0]
        self.assertLess(r.ic_inf, 1)
        self.assertLess(r.p_valor, 0.05)
        self.assertTrue(r.significativa_bonf)

    def test_grupo_vacio_y_mascara_desalineada(self):
        datos = pd.DataFrame({"amen_wifi": [0, 1], "estimated_occupancy_l365d": [1, 2]})
        for mascara in [pd.Series([True, True]), pd.Series([True, False], index=[1, 0])]:
            with self.assertRaises(ValueError):
                comparar_amenidades(datos, mascara)

    def test_idioma_ponderado_por_resenas_no_por_alojamientos(self):
        datos = pd.DataFrame({"comuna_agrupada": ["A", "A"], "pct_en": [1, 0],
                              "n_resenas": [1, 9]})
        self.assertAlmostEqual(com.idioma_comunas(datos).loc["A", "pct_en"], .1)

    def test_merge_resenas_no_duplica_filas(self):
        with self.assertRaises(pd.errors.MergeError):
            com.unir_resenas(pd.DataFrame({"id": [1]}),
                            pd.DataFrame({"listing_id": [1, 1], "n_resenas": [1, 2]}))

    def test_resumen_estratos_no_confunde_signo_y_significancia(self):
        tabla = pd.DataFrame({"comodidad": ["wifi", "wifi"], "comuna": ["A", "B"],
                              "diferencia": [.1, -.2], "significativa_bonf": [False, True]})
        resumen = resumir_estratos(tabla).iloc[0]
        self.assertEqual(resumen["estratos"], 2)
        self.assertEqual(resumen["diferencias_positivas"], 1)
        self.assertEqual(resumen["significativas_bonf"], 1)
        self.assertTrue(resumir_estratos(pd.DataFrame()).empty)

    def test_estratos_sin_casos_suficientes(self):
        datos = self.datos().assign(amen_wifi=1)
        self.assertTrue(comparar_por_estratos(datos, minimo_grupo=100).empty)
