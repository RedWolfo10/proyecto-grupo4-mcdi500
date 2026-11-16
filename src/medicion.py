"""Medicion de tiempo y memoria de una funcion."""

import time
import tracemalloc


def medir(funcion, *args, **kwargs):
    """Ejecuta la funcion y devuelve (resultado, segundos, MB de pico)."""
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = funcion(*args, **kwargs)
    transcurrido = time.perf_counter() - inicio
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return resultado, transcurrido, pico / 1024 / 1024
