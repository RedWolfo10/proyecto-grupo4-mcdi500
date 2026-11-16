"""Carga y verificacion del conjunto de datos."""

import os

import pandas as pd


def leer_archivo(ruta):
    """Lee el archivo según su extensión y devuelve un DataFrame."""
    extension = os.path.splitext(ruta)[1].lower()

    if extension in (".csv", ".txt"):
        return pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8")
    if extension in (".xlsx", ".xls"):
        return pd.read_excel(ruta)
    if extension == ".parquet":
        return pd.read_parquet(ruta)

    raise ValueError(
        f"Extension no reconocida: '{extension}'. "
        "Se admiten .csv, .txt, .xlsx, .xls y .parquet."
    )


def verificar_esquema(df, columnas_esperadas):
    """Comprueba que estén todas las columnas declaradas en la configuración."""
    faltantes = [c for c in columnas_esperadas if c not in df.columns]
    if faltantes:
        raise KeyError(
            f"Faltan columnas declaradas en la configuración: {faltantes}\n"
            f"Columnas disponibles en el archivo: {list(df.columns)}"
        )
    sobrantes = [c for c in df.columns if c not in columnas_esperadas]
    return {"declaradas": len(columnas_esperadas),
            "en_archivo": df.shape[1],
            "no_declaradas": sobrantes}


def cargar(ruta, columnas_esperadas, columnas_numericas=()):
    """Carga el conjunto desde el archivo externo y verifica su esquema."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")

    df = leer_archivo(ruta)

    for columna in columnas_numericas:
        if columna in df.columns:
            df[columna] = pd.to_numeric(df[columna], errors="coerce")

    informe = verificar_esquema(df, columnas_esperadas)
    print(f"Forma: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"Esquema verificado: {informe['declaradas']} columnas declaradas, "
          f"{len(informe['no_declaradas'])} no declaradas")
    if informe["no_declaradas"]:
        print("  No declaradas:", informe["no_declaradas"])
    return df
