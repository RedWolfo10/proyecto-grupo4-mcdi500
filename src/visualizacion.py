"""Indicadores descriptivos para comunicar resultados (Fase 4).

La Fase 4 no limpia ni transforma: toma ``listings_procesado.csv`` tal como lo
dejó el pipeline y resume el desempeño (ocupación, precio e ingresos estimados)
por grupos. Todas las funciones trabajan sobre pandas y devuelven tablas o
máscaras, para que el cuaderno solo se preocupe de graficar.

Como ``estimated_occupancy_l365d`` está topada en 255 noches (decisión D10),
los resúmenes usan mediana y cuartiles y siempre reportan qué porcentaje del
grupo quedó pegado en el tope.
"""

import os

import pandas as pd

OCUPACION = "estimated_occupancy_l365d"
PRECIO = "price_clp"
INGRESOS = "estimated_revenue_l365d"
TOPE_OCUPACION = 255


def resumen_desempeno(df, grupo):
    """Resume el desempeño por cada valor de ``grupo``.

    Devuelve una tabla con una fila por categoría: tamaño, mediana y cuartiles
    de la ocupación, porcentaje en el tope de 255 noches, precio mediano,
    ingresos medianos e ingresos medianos normalizados por huésped
    (``accommodates``) y por dormitorio (``bedrooms`` > 0). Ordenada por
    ocupación mediana descendente.
    """
    if grupo not in df.columns:
        raise KeyError(f"La columna '{grupo}' no existe en el conjunto.")

    filas = []
    for valor, sub in df.groupby(grupo, observed=True):
        ocup = sub[OCUPACION]
        filas.append({
            grupo: valor,
            "n": len(sub),
            "ocupacion_mediana": ocup.median(),
            "ocupacion_q1": ocup.quantile(0.25),
            "ocupacion_q3": ocup.quantile(0.75),
            "pct_en_tope": (ocup >= TOPE_OCUPACION).mean(),
            "precio_mediano": sub[PRECIO].median(),
            "ingresos_medianos": sub[INGRESOS].median(),
            "ingreso_huesped_mediano":
                (sub[INGRESOS] / sub["accommodates"]).median(),
            "ingreso_dormitorio_mediano":
                (sub[INGRESOS] / sub["bedrooms"].where(sub["bedrooms"] > 0)).median(),
        })
    return pd.DataFrame(filas).sort_values("ocupacion_mediana", ascending=False)


def cuartil_superior(df, columna=OCUPACION):
    """Marca los registros sobre el cuartil 3 de ``columna``."""
    if columna not in df.columns:
        raise KeyError(f"La columna '{columna}' no existe en el conjunto.")
    if df[columna].isna().any():
        raise ValueError(f"La columna '{columna}' tiene nulos; no se puede cortar.")
    return df[columna] >= df[columna].quantile(0.75)


def comparar_amenidades(df, mascara, columnas_amen=None):
    """Compara la frecuencia de cada comodidad dentro y fuera de ``mascara``.

    Además de la frecuencia en cada grupo, calcula la mediana de ocupación de
    los alojamientos que tienen la comodidad frente a los que no, que es lo que
    en realidad le importa al perfil buscado.
    """
    if columnas_amen is None:
        columnas_amen = [c for c in df.columns if c.startswith("amen_")]
    if not columnas_amen:
        raise ValueError("No se encontraron columnas binarias 'amen_'.")

    filas = []
    for col in columnas_amen:
        dentro = df.loc[mascara, col].mean()
        fuera = df.loc[~mascara, col].mean()
        con = df.loc[df[col] == 1, OCUPACION].median()
        sin = df.loc[df[col] == 0, OCUPACION].median()
        filas.append({
            "comodidad": col.replace("amen_", ""),
            "frec_top": dentro,
            "frec_resto": fuera,
            "diferencia": dentro - fuera,
            "ocup_con": con,
            "ocup_sin": sin,
        })
    return pd.DataFrame(filas).sort_values("diferencia", ascending=False)


def guardar_figura(figura, carpeta, nombre, dpi=200):
    """Guarda la figura en PNG con resolución de impresión y devuelve la ruta."""
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"{nombre}.png")
    figura.savefig(ruta, dpi=dpi, bbox_inches="tight")
    return ruta
