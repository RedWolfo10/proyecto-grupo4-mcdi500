"""Pipeline: encadena transformadores y los ejecuta en orden."""

import pandas as pd

from transformadores import Transformador


class Pipeline:
    """Recorre los pasos sin preguntar de que tipo son (polimorfismo)."""

    def __init__(self, pasos=None):
        self._pasos = list(pasos) if pasos else []
        self._ajustado = False

    def agregar(self, transformador):
        if not isinstance(transformador, Transformador):
            raise TypeError(
                f"Se esperaba un Transformador y se recibio {type(transformador).__name__}."
            )
        self._pasos.append(transformador)
        return self

    def ajustar(self, df):
        """Aprende los parametros de cada paso con este conjunto."""
        intermedio = df.copy()
        for paso in self._pasos:
            intermedio = paso.ajustar_transformar(intermedio)
        self._ajustado = True
        return self

    def transformar(self, df):
        if not self._ajustado:
            raise RuntimeError("Pipeline: hay que ajustar antes de transformar.")
        resultado = df.copy()
        for paso in self._pasos:
            resultado = paso.transformar(resultado)
        return resultado

    @property
    def pasos(self):
        return tuple(self._pasos)

    def resumen(self):
        return pd.DataFrame([
            {"orden": i, "paso": p.nombre, "clase": type(p).__name__}
            for i, p in enumerate(self._pasos, start=1)
        ])
