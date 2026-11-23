import sys
import tracemalloc
import unittest

import pandas as pd

sys.path.insert(0, "src")

from medicion import medir
from pipeline import Pipeline
from transformadores import (
    AgrupadorTopCategorias,
    BinarizadorAmenidades,
    ImputadorPorGrupo,
    parsear_amenidades,
)


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
    def test_rechaza_transformar_antes_de_ajustar(self):
        datos = pd.DataFrame({"accommodates": [1], "beds": [None]})

        with self.assertRaisesRegex(RuntimeError, "ajustar antes"):
            ImputadorPorGrupo("beds", "accommodates").transformar(datos)

    def test_columna_sin_nulos_conserva_valores_y_no_marca_imputaciones(self):
        datos = pd.DataFrame({
            "accommodates": [1, 2, 3],
            "beds": [1, 2, 3],
        })

        resultado = ImputadorPorGrupo(
            "beds", "accommodates"
        ).ajustar_transformar(datos)

        self.assertEqual(resultado["beds"].tolist(), [1, 2, 3])
        self.assertEqual(resultado["beds_imputado"].tolist(), [0, 0, 0])

    def test_rechaza_columna_completamente_vacia(self):
        datos = pd.DataFrame({
            "accommodates": [1, 2, 3],
            "beds": [None, None, None],
        })
        with self.assertRaisesRegex(ValueError, "no hay valores disponibles"):
            ImputadorPorGrupo("beds", "accommodates").ajustar(datos)

    def test_rechaza_columna_inexistente(self):
        with self.assertRaisesRegex(KeyError, "columna no existe"):
            ImputadorPorGrupo("beds", "accommodates").ajustar(
                pd.DataFrame({"accommodates": [1, 2]})
            )


class AgrupadorTopCategoriasTests(unittest.TestCase):
    def test_agrupa_categorias_no_vistas_y_no_altera_la_entrada(self):
        datos = pd.DataFrame({"tipo": ["Casa", "Casa", "Departamento"]})
        transformador = AgrupadorTopCategorias("tipo", n_top=1)
        transformador.ajustar(datos)

        resultado = transformador.transformar(
            pd.DataFrame({"tipo": ["Casa", "Departamento", "Nueva"]})
        )

        self.assertEqual(
            resultado["tipo_agrupada"].tolist(), ["Casa", "Otro", "Otro"]
        )
        self.assertNotIn("tipo_agrupada", datos.columns)

    def test_una_categoria_no_se_convierte_en_otro(self):
        datos = pd.DataFrame({"tipo": ["Casa", "Casa"]})

        resultado = AgrupadorTopCategorias("tipo").ajustar_transformar(datos)

        self.assertEqual(resultado["tipo_agrupada"].tolist(), ["Casa", "Casa"])


class BinarizadorAmenidadesTests(unittest.TestCase):
    def test_crea_columnas_top_y_cuenta_todas_las_amenidades(self):
        datos = pd.DataFrame({
            "amenities": ['["Wifi", "Kitchen"]', '["Wifi"]', None],
        })
        transformador = BinarizadorAmenidades(n_top=1)

        resultado = transformador.ajustar_transformar(datos)

        self.assertEqual(resultado["amenities_count"].tolist(), [2, 1, 0])
        self.assertEqual(resultado["amen_wifi"].tolist(), [1, 1, 0])
        self.assertNotIn("amen_kitchen", resultado.columns)
        self.assertNotIn("amen_wifi", datos.columns)

    def test_listas_vacias_producen_conteo_cero_y_sin_columnas_binarias(self):
        datos = pd.DataFrame({"amenities": ["[]", "[]"]})

        resultado = BinarizadorAmenidades().ajustar_transformar(datos)

        self.assertEqual(resultado["amenities_count"].tolist(), [0, 0])
        self.assertEqual(
            [col for col in resultado.columns if col.startswith("amen_")], []
        )

    def test_rechaza_json_mal_formado_al_ajustar(self):
        with self.assertRaisesRegex(ValueError, "lista JSON"):
            BinarizadorAmenidades().ajustar(
                pd.DataFrame({"amenities": ['["Wifi"']})
            )


class PipelineTests(unittest.TestCase):
    def test_encadena_transformadores_y_resume_sus_pasos(self):
        pipeline = Pipeline([
            AgrupadorTopCategorias("tipo", n_top=1),
            BinarizadorAmenidades(n_top=1),
        ])
        entrenamiento = pd.DataFrame({
            "tipo": ["Casa", "Casa", "Departamento"],
            "amenities": ['["Wifi"]', '["Wifi", "Kitchen"]', '["Kitchen"]'],
        })
        pipeline.ajustar(entrenamiento)
        resultado = pipeline.transformar(pd.DataFrame({
            "tipo": ["Nueva"],
            "amenities": ['["Wifi", "Piscina"]'],
        }))

        self.assertEqual(resultado.loc[0, "tipo_agrupada"], "Otro")
        self.assertEqual(resultado.loc[0, "amenities_count"], 2)
        self.assertEqual(resultado.loc[0, "amen_wifi"], 1)
        self.assertEqual(
            pipeline.resumen()["clase"].tolist(),
            ["AgrupadorTopCategorias", "BinarizadorAmenidades"],
        )

    def test_rechaza_transformar_antes_de_ajustar_y_pasos_invalidos(self):
        with self.assertRaisesRegex(RuntimeError, "ajustar antes"):
            Pipeline().transformar(pd.DataFrame())
        with self.assertRaisesRegex(TypeError, "Se esperaba un Transformador"):
            Pipeline().agregar("no soy un transformador")


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
