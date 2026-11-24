import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import pandas as pd

from src import visualizacion


class ResumenDesempenoTests(unittest.TestCase):
    def setUp(self):
        self.datos = pd.DataFrame({
            "comuna": ["A"] * 4 + ["B"] * 4,
            "estimated_occupancy_l365d": [10, 20, 255, 255, 5, 15, 25, 35],
            "price_clp": [100] * 4 + [200] * 4,
            "estimated_revenue_l365d": [1000] * 4 + [2000] * 4,
        })

    def test_resume_mediana_tope_y_orden_por_ocupacion(self):
        resultado = visualizacion.resumen_desempeno(self.datos, "comuna")
        fila_a = resultado.set_index("comuna").loc["A"]

        self.assertEqual(fila_a["ocupacion_mediana"], 137.5)
        self.assertEqual(fila_a["pct_en_tope"], 0.5)
        self.assertEqual(fila_a["precio_mediano"], 100)
        self.assertEqual(resultado.iloc[0]["comuna"], "A")

    def test_rechaza_grupo_inexistente(self):
        with self.assertRaisesRegex(KeyError, "no existe"):
            visualizacion.resumen_desempeno(self.datos, "no_existe")


class CuartilSuperiorTests(unittest.TestCase):
    def test_valores_iguales_quedan_todos_en_el_cuartil_superior(self):
        datos = pd.DataFrame({"ocupacion": [50, 50, 50]})

        resultado = visualizacion.cuartil_superior(datos, "ocupacion")

        self.assertTrue(resultado.all())

    def test_rechaza_columna_inexistente_y_valores_nulos(self):
        with self.assertRaisesRegex(KeyError, "no existe"):
            visualizacion.cuartil_superior(pd.DataFrame(), "ocupacion")
        with self.assertRaisesRegex(ValueError, "tiene nulos"):
            visualizacion.cuartil_superior(
                pd.DataFrame({"ocupacion": [10, None]}), "ocupacion"
            )


class CompararAmenidadesTests(unittest.TestCase):
    def test_compara_frecuencias_y_mediana_de_ocupacion(self):
        datos = pd.DataFrame({
            "estimated_occupancy_l365d": [10, 20, 30, 40],
            "amen_wifi": [1, 0, 1, 0],
            "amen_pool": [1, 1, 0, 0],
        })

        resultado = visualizacion.comparar_amenidades(
            datos, pd.Series([True, True, False, False])
        ).set_index("comodidad")

        self.assertEqual(resultado.loc["pool", "diferencia"], 1)
        self.assertEqual(resultado.loc["pool", "ocup_con"], 15)
        self.assertEqual(resultado.loc["pool", "ocup_sin"], 35)
        self.assertEqual(resultado.loc["wifi", "diferencia"], 0)

    def test_rechaza_ausencia_de_columnas_binarias(self):
        datos = pd.DataFrame({"estimated_occupancy_l365d": [10]})

        with self.assertRaisesRegex(ValueError, "No se encontraron"):
            visualizacion.comparar_amenidades(datos, pd.Series([True]))


class GuardarFiguraTests(unittest.TestCase):
    def test_crea_carpeta_y_guarda_con_resolucion_solicitada(self):
        with tempfile.TemporaryDirectory() as temporal:
            figura = Mock()

            ruta = visualizacion.guardar_figura(
                figura, Path(temporal) / "figuras", "resultado", dpi=150
            )

            self.assertEqual(ruta, str(Path(temporal) / "figuras" / "resultado.png"))
            figura.savefig.assert_called_once_with(
                ruta, dpi=150, bbox_inches="tight"
            )
            self.assertTrue((Path(temporal) / "figuras").is_dir())


if __name__ == "__main__":
    unittest.main()
