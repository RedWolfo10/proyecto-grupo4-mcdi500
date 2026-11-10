"""Utilidades compartidas del proyecto MCDI500 - Grupo 4.

Este modulo lo genera el cuaderno de la Fase 1 y lo importan las fases
siguientes. Proyecto: alojamientos Airbnb en Santiago de Chile.
"""

import re
import hashlib


class ProyectoError(Exception):
    """Error propio del proyecto: permite distinguirlo de los de las librerias."""


def normalizar_nombre(texto):
    """Convierte un nombre de columna a minusculas, sin espacios ni signos.

    Ejemplo
    -------
normalizar_nombre('Bathrooms Text ')
    'bathrooms_text'
    """
    if not isinstance(texto, str):
        raise ProyectoError(f"Se esperaba texto y se recibio {type(texto).__name__}.")
    limpio = texto.strip().lower()
    limpio = re.sub(r"[^a-z0-9]+", "_", limpio)   # lo que no sea letra o digito -> _
    return limpio.strip("_")


def normalizar_columnas(nombres):
    """Aplica normalizar_nombre a una lista y verifica que no haya duplicados."""
    normalizados = [normalizar_nombre(n) for n in nombres]
    if len(set(normalizados)) != len(normalizados):
        raise ProyectoError("La normalizacion produjo nombres duplicados.")
    return normalizados


def seudonimizar(valor, largo=12):
    """Devuelve un codigo seudonimo estable para un identificador personal.

    Se aplica a host_id (decision D5): permite contar anuncios por anfitrion
    sin conservar el identificador original. El mismo valor de entrada produce
    siempre el mismo codigo, de modo que el conteo sigue siendo valido.

    Ejemplo
    -------
seudonimizar(224592)  # doctest omite el valor exacto a proposito
    '...'
    """
    if not isinstance(valor, (str, int)):
        raise ProyectoError(
            f"Se esperaba texto o entero y se recibio {type(valor).__name__}.")
    return hashlib.sha256(str(valor).encode("utf-8")).hexdigest()[:largo]
