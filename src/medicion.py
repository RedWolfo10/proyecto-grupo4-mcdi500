"""Medicion de tiempo y memoria de una funcion."""

import time
import tracemalloc


def medir(funcion, *args, **kwargs):
    """Devuelve el resultado, tiempo y pico de memoria Python en MB."""
    if tracemalloc.is_tracing():
        raise RuntimeError("medir no puede ejecutarse con tracemalloc ya activo.")

    tracemalloc.start()
    try:
        inicio = time.perf_counter()
        resultado = funcion(*args, **kwargs)
        transcurrido = time.perf_counter() - inicio
        _, pico = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return resultado, transcurrido, pico / 1024 / 1024
