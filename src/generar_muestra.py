#!/usr/bin/env python3
"""
Generador de la muestra de trabajo - MCDI500 - Grupo 4

El archivo detallado listings.csv de Inside Airbnb (Santiago, captura de
septiembre de 2026) tiene 18.904 filas x 90 columnas y unos 50 MB. Para que
los cuadernos sean livianos de ejecutar y de versionar, el proyecto trabaja
con una muestra aleatoria ESTRATIFICADA por comuna.

La muestra es reproducible: con la misma entrada y la misma semilla, este
script produce siempre el mismo archivo. Cada integrante descarga el archivo
original desde Inside Airbnb y ejecuta este script una sola vez.

Uso:
    python src/generar_muestra.py ruta/al/listings.csv
    python src/generar_muestra.py ruta/al/listings.csv.gz
    python src/generar_muestra.py listings.csv --salida data/raw/listings.csv
    python src/generar_muestra.py listings.csv --fraccion 0.30
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Parámetros de la muestra. Cambiarlos aquí y documentarlo en el informe.
# ---------------------------------------------------------------------------
SEMILLA = 42                         # la misma semilla de los cuadernos
FRACCION = 0.27                      # proporción de cada comuna en la muestra
ESTRATO = "neighbourhood_cleansed"   # variable de estratificación (32 comunas)
MINIMO_POR_COMUNA = 1                # comunas muy pequeñas conservan un registro


def generar_muestra(df, estrato=ESTRATO, fraccion=FRACCION,
                    minimo=MINIMO_POR_COMUNA, semilla=SEMILLA):
    """Devuelve una muestra aleatoria estratificada por comuna.

    Parametros
    ----------
    df : pd.DataFrame
        Conjunto completo de alojamientos.
    estrato : str
        Columna de estratificacion.
    fraccion : float
        Proporcion de cada estrato que entra a la muestra.
    minimo : int
        Registros minimos por estrato (evita que comunas pequenas desaparezcan).
    semilla : int
        Semilla del muestreo aleatorio.

    Retorna
    -------
    pd.DataFrame
        Muestra en el orden original del archivo.
    """
    if estrato not in df.columns:
        raise KeyError(f"La columna de estratificacion '{estrato}' no existe.")
    if not 0 < fraccion <= 1:
        raise ValueError("fraccion debe estar en el rango (0, 1].")

    partes = []
    for estrato_valor, grupo in df.groupby(estrato):
        n = max(minimo, int(round(len(grupo) * fraccion)))
        partes.append(grupo.sample(n=n, random_state=semilla))
    return pd.concat(partes).sort_index()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("origen", help="listings.csv o listings.csv.gz completo de Inside Airbnb")
    p.add_argument("--salida", default="data/raw/listings.csv",
                   help="Archivo de salida (por defecto data/raw/listings.csv)")
    p.add_argument("--fraccion", type=float, default=FRACCION,
                   help=f"Proporcion por comuna (por defecto {FRACCION})")
    args = p.parse_args()

    origen = Path(args.origen)
    if not origen.exists():
        sys.exit(f"No se encontro el archivo: {origen}\n"
                 "Descarguelo desde http://insideairbnb.com/get-the-data/ "
                 "(Santiago, Chile, archivo 'listings.csv' detallado).")

    df = pd.read_csv(origen)
    muestra = generar_muestra(df, fraccion=args.fraccion)

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    muestra.to_csv(salida, index=False)

    n_comunas = df[ESTRATO].nunique()
    print(f"Origen   : {origen} -> {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"Muestra  : {muestra.shape[0]} filas ({muestra.shape[0] / df.shape[0]:.1%}), "
          f"{muestra[ESTRATO].nunique()} de {n_comunas} comunas")
    print(f"Escrita  : {salida} ({salida.stat().st_size / 1024**2:.1f} MB)")


if __name__ == "__main__":
    main()
