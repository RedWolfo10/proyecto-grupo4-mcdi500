"""Transformadores del pipeline: contrato comun y clases que aprenden del dataset."""

import json
from abc import ABC, abstractmethod
from copy import deepcopy

import numpy as np
import pandas as pd

from .utilidades import normalizar_nombre


def parsear_amenidades(valor):
    """Convierte el texto JSON de amenities en una lista de strings."""
    if valor is None or valor is pd.NA or (np.isscalar(valor) and pd.isna(valor)):
        return []
    if not isinstance(valor, str):
        raise ValueError("amenities debe ser texto JSON.")
    try:
        lista = json.loads(valor)
    except json.JSONDecodeError as error:
        raise ValueError("amenities debe contener una lista JSON valida.") from error
    if not isinstance(lista, list):
        raise ValueError(f"amenities no es una lista: {valor!r}")
    if not all(isinstance(amenidad, str) for amenidad in lista):
        raise ValueError("Cada amenidad debe ser texto.")
    return lista


class Transformador(ABC):
    """Contrato de los pasos del pipeline.

    ajustar() aprende los parametros del conjunto y transformar() los aplica.
    Las clases hijas solo implementan aprender() y aplicar().
    """

    def __init__(self, columna):
        self.columna = columna
        self._parametros = {}
        self._ajustado = False

    @property
    def nombre(self):
        return f"{type(self).__name__}({self.columna})"

    @property
    def parametros(self):
        return deepcopy(self._parametros)

    def ajustar(self, df):
        if self.columna not in df.columns:
            raise KeyError(f"{self.nombre}: la columna no existe en el conjunto.")
        self._parametros = self.aprender(df)
        self._ajustado = True
        return self

    def transformar(self, df):
        if not self._ajustado:
            raise RuntimeError(f"{self.nombre}: hay que ajustar antes de transformar.")
        return self.aplicar(df.copy())

    def ajustar_transformar(self, df):
        return self.ajustar(df).transformar(df)

    @abstractmethod
    def aprender(self, df):
        raise NotImplementedError("Cada clase hija debe implementar aprender().")

    @abstractmethod
    def aplicar(self, df):
        raise NotImplementedError("Cada clase hija debe implementar aplicar().")


class ImputadorPorGrupo(Transformador):
    """Rellena nulos con la mediana del tramo de una variable agrupadora.

    Replica la decision de la Fase 2: los nulos de beds y bedrooms se imputan
    con la mediana de su tramo de accommodates (qcut en 4 grupos), con la
    mediana global como respaldo. Agrega la bandera '<columna>_imputado'.
    """

    def __init__(self, columna, agrupador, n_grupos=4):
        super().__init__(columna)
        self.agrupador = agrupador
        self.n_grupos = n_grupos

    def aprender(self, df):
        mediana_global = df[self.columna].median()
        if pd.isna(mediana_global):
            raise ValueError(
                f"{self.nombre}: no hay valores disponibles para calcular la mediana."
            )
        tramos = pd.qcut(df[self.agrupador], q=self.n_grupos, duplicates="drop")
        medianas = df[self.columna].groupby(tramos, observed=True).median()
        return {
            "tramos": tramos.cat.categories,
            "medianas": {iv: float(m) for iv, m in medianas.items()},
            "global": float(mediana_global),
        }

    def aplicar(self, df):
        if len(self._parametros["tramos"]) == 0:
            mediana = pd.Series(self._parametros["global"], index=df.index)
        else:
            tramos = pd.cut(df[self.agrupador], bins=self._parametros["tramos"])
            mediana = tramos.map(self._parametros["medianas"]).astype(float)
            mediana = mediana.fillna(self._parametros["global"])
        df[f"{self.columna}_imputado"] = df[self.columna].isna().astype(int)
        df[self.columna] = df[self.columna].fillna(mediana)
        return df


class AgrupadorTopCategorias(Transformador):
    """Conserva las n_top categorias mas frecuentes y agrupa el resto en 'Otro'."""

    def __init__(self, columna, n_top=5, nombre_salida=None, etiqueta_otro="Otro"):
        super().__init__(columna)
        self.n_top = n_top
        self.nombre_salida = nombre_salida or f"{columna}_agrupada"
        self.etiqueta_otro = etiqueta_otro

    def aprender(self, df):
        return {"top": df[self.columna].value_counts().head(self.n_top).index.tolist()}

    def aplicar(self, df):
        df[self.nombre_salida] = df[self.columna].where(
            df[self.columna].isin(self._parametros["top"]), self.etiqueta_otro
        )
        return df


class BinarizadorAmenidades(Transformador):
    """Aprende las comodidades mas frecuentes y crea una columna 0/1 por cada una.

    Tambien calcula amenities_count con el largo de la lista parseada.
    """

    def __init__(self, columna="amenities", n_top=20, prefijo="amen_"):
        super().__init__(columna)
        self.n_top = n_top
        self.prefijo = prefijo

    def aprender(self, df):
        listas = df[self.columna].map(parsear_amenidades)
        frecuencias = pd.Series(
            [a for lista in listas for a in lista]
        ).value_counts()
        return {"top": frecuencias.head(self.n_top).index.tolist()}

    def aplicar(self, df):
        listas = df[self.columna].map(parsear_amenidades)
        df["amenities_count"] = listas.map(len)
        for amenidad in self._parametros["top"]:
            columna = self.prefijo + normalizar_nombre(amenidad)
            df[columna] = listas.map(lambda lista, a=amenidad: int(a in lista))
        return df
