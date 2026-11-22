import sys
import unittest

import pandas as pd

sys.path.insert(0, "src")

from visualizacion import resumen_desempeno


def datos():
    return pd.DataFrame({
        "grupo": ["A", "A", "B", "B"],
        "estimated_occupancy_l365d": [100, 200, 50, 255],
        "price_clp": [1000, 2000, 500, 1500],
        "estimated_revenue_l365d": [100, 400, 50, 300],
        "accommodates": [2, 4, 2, 2],
        "bedrooms": [1, 2, 0, 1],
    })


class ResumenDesempenoTests(unittest.TestCase):
    def test_agrega_ingresos_normalizados_por_grupo(self):
        resumen = resumen_desempeno(datos(), "grupo").set_index("grupo")

        self.assertAlmostEqual(resumen.loc["A", "ingreso_huesped_mediano"], 75.0)
        self.assertAlmostEqual(resumen.loc["A", "ingreso_dormitorio_mediano"], 150.0)
        self.assertAlmostEqual(resumen.loc["B", "ingreso_huesped_mediano"], 87.5)
        # El dormitorio en 0 se excluye de la normalización por dormitorio.
        self.assertAlmostEqual(resumen.loc["B", "ingreso_dormitorio_mediano"], 300.0)

    def test_columna_inexistente_lanza_keyerror(self):
        with self.assertRaises(KeyError):
            resumen_desempeno(datos(), "columna_que_no_existe")


if __name__ == "__main__":
    unittest.main()
