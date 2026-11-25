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

import numpy as np
import pandas as pd
from scipy import stats

OCUPACION = "estimated_occupancy_l365d"
PRECIO = "price_clp"
INGRESOS = "estimated_revenue_l365d"
TOPE_OCUPACION = 255


def agrupar_comunas(df, minimo=30):
    if minimo < 1:
        raise ValueError("El mínimo debe ser positivo.")
    columna = "neighbourhood_cleansed"
    if df[columna].isna().any():
        raise ValueError("Las comunas no pueden contener nulos.")
    resultado = df.copy()
    conteos = resultado[columna].value_counts()
    resultado["comuna_agrupada"] = resultado[columna].where(
        resultado[columna].map(conteos) >= minimo, "Otras comunas"
    )
    return resultado


def resumen_desempeno(df, grupo):
    """Resume el desempeño por cada valor de ``grupo``.

    Devuelve una tabla con una fila por categoría: tamaño, mediana y cuartiles
    de la ocupación, porcentaje en el tope de 255 noches, precio mediano,
    ingresos medianos e ingresos medianos normalizados por huésped
    (``accommodates``) y por dormitorio (``bedrooms`` > 0); las dos últimas
    solo aparecen cuando las columnas divisor existen. Ordenada por
    ocupación mediana descendente.
    """
    if grupo not in df.columns:
        raise KeyError(f"La columna '{grupo}' no existe en el conjunto.")

    filas = []
    for valor, sub in df.groupby(grupo, observed=True):
        ocup = sub[OCUPACION]
        fila = {
            grupo: valor,
            "n": len(sub),
            "ocupacion_mediana": ocup.median(),
            "ocupacion_q1": ocup.quantile(0.25),
            "ocupacion_q3": ocup.quantile(0.75),
            "pct_en_tope": (ocup >= TOPE_OCUPACION).mean(),
            "precio_mediano": sub[PRECIO].median(),
            "precio_q1": sub[PRECIO].quantile(0.25),
            "precio_q3": sub[PRECIO].quantile(0.75),
            "ingresos_medianos": sub[INGRESOS].median(),
            "ingresos_q1": sub[INGRESOS].quantile(0.25),
            "ingresos_q3": sub[INGRESOS].quantile(0.75),
        }
        if "accommodates" in sub.columns:
            fila["ingreso_huesped_mediano"] = (
                sub[INGRESOS] / sub["accommodates"].where(sub["accommodates"] > 0)
            ).median()
        if "bedrooms" in sub.columns:
            fila["ingreso_dormitorio_mediano"] = (
                sub[INGRESOS] / sub["bedrooms"].where(sub["bedrooms"] > 0)
            ).median()
        filas.append(fila)
    return pd.DataFrame(filas).sort_values("ocupacion_mediana", ascending=False)


def cuartil_superior(df, columna=OCUPACION):
    """Marca los registros sobre el cuartil 3 de ``columna``."""
    if columna not in df.columns:
        raise KeyError(f"La columna '{columna}' no existe en el conjunto.")
    if df[columna].isna().any():
        raise ValueError(f"La columna '{columna}' tiene nulos; no se puede cortar.")
    return df[columna] >= df[columna].quantile(0.75)


def intervalo_wilson(exitos, n, alfa=0.05):
    if n <= 0 or not 0 < alfa < 1:
        raise ValueError("Se requieren observaciones y alfa entre 0 y 1.")
    p = exitos / n
    z = stats.norm.ppf(1 - alfa / 2)
    divisor = 1 + z ** 2 / n
    centro = (p + z ** 2 / (2 * n)) / divisor
    margen = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / divisor
    return centro - margen, centro + margen


def comparar_amenidades(df, mascara, columnas_amen=None, alfa=0.05):
    """Diferencia de prevalencias, IC Newcombe-Wilson y prueba exacta de Fisher.

    Los IC son individuales. Bonferroni corrige los p-valores de la familia
    de comodidades evaluada, no los IC. El análisis es observacional.
    """
    if columnas_amen is None:
        columnas_amen = [c for c in df.columns if c.startswith("amen_")]
    if not columnas_amen:
        raise ValueError("No se encontraron columnas binarias 'amen_'.")
    if not 0 < alfa < 1:
        raise ValueError("Alfa debe estar entre 0 y 1.")
    if not mascara.index.equals(df.index) or mascara.isna().any() or mascara.dtype != bool:
        raise ValueError("La máscara debe ser booleana, sin nulos y alineada con los datos.")
    if not df[columnas_amen].isin([0, 1]).all().all():
        raise ValueError("Las comodidades deben ser binarias y no contener nulos.")
    n_top, n_resto = int(mascara.sum()), int((~mascara).sum())
    if not n_top or not n_resto:
        raise ValueError("Ambos grupos deben contener alojamientos.")
    filas = []
    for col in columnas_amen:
        x_top = int(df.loc[mascara, col].sum())
        x_resto = int(df.loc[~mascara, col].sum())
        p_top, p_resto = x_top / n_top, x_resto / n_resto
        dif = p_top - p_resto
        li_top, ls_top = intervalo_wilson(x_top, n_top, alfa)
        li_resto, ls_resto = intervalo_wilson(x_resto, n_resto, alfa)
        p_valor = stats.fisher_exact([[x_top, n_top - x_top],
                                     [x_resto, n_resto - x_resto]]).pvalue
        ajustado = min(1.0, p_valor * len(columnas_amen))
        filas.append({
            "comodidad": col.removeprefix("amen_"),
            "n_top": n_top, "n_resto": n_resto,
            "frec_top": p_top, "frec_resto": p_resto, "diferencia": dif,
            "ic_inf": dif - np.hypot(p_top - li_top, ls_resto - p_resto),
            "ic_sup": dif + np.hypot(ls_top - p_top, p_resto - li_resto),
            "p_valor": p_valor, "p_ajustado": ajustado,
            "significativa_bonf": ajustado < alfa,
            "ocup_con": df.loc[df[col] == 1, OCUPACION].median(),
            "ocup_sin": df.loc[df[col] == 0, OCUPACION].median(),
        })
    return pd.DataFrame(filas).sort_values("diferencia", ascending=False)


def comparar_por_estratos(df, columnas_amen=None, minimo_grupo=10):
    datos = agrupar_comunas(df)
    datos["capacidad_tramo"] = pd.cut(datos["accommodates"], [0, 2, 4, np.inf],
                                     labels=["1–2", "3–4", "5 o más"])
    datos["en_top"] = cuartil_superior(datos)
    resultados = []
    for (comuna, capacidad), sub in datos.groupby(
            ["comuna_agrupada", "capacidad_tramo"], observed=True):
        mascara = sub["en_top"]
        if min(int(mascara.sum()), int((~mascara).sum())) < minimo_grupo:
            continue
        tabla = comparar_amenidades(sub, mascara, columnas_amen)
        tabla["comuna"] = comuna
        tabla["capacidad"] = capacidad
        resultados.append(tabla)
    if not resultados:
        return pd.DataFrame()
    tabla = pd.concat(resultados, ignore_index=True)
    tabla["p_ajustado"] = (tabla["p_valor"] * len(tabla)).clip(upper=1)
    tabla["significativa_bonf"] = tabla["p_ajustado"] < 0.05
    return tabla


def resumir_estratos(tabla):
    if tabla.empty:
        return pd.DataFrame()
    datos = tabla.assign(positiva=tabla["diferencia"] > 0)
    return datos.groupby("comodidad", as_index=False).agg(
        estratos=("comuna", "size"),
        diferencias_positivas=("positiva", "sum"),
        significativas_bonf=("significativa_bonf", "sum"),
        diferencia_minima=("diferencia", "min"),
        diferencia_maxima=("diferencia", "max"),
    )


def guardar_figura(figura, carpeta, nombre, dpi=200):
    """Guarda la figura en PNG con resolución de impresión y devuelve la ruta."""
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"{nombre}.png")
    figura.savefig(ruta, dpi=dpi, bbox_inches="tight")
    return ruta
