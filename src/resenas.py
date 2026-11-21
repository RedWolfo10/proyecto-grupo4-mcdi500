"""Procesamiento de resenas detalladas (Fase 4, decisiones D6 y D11).

El archivo detallado de Inside Airbnb trae nombres y comentarios, asi que no
se versiona (D7). Este modulo lo reduce a un agregado anonimo por alojamiento:
idioma inferido de cada resena y conteo de menciones de cada comodidad. El
texto y los nombres se descartan dentro del propio proceso; lo unico que sale
a data/processed/ es una tabla sin datos personales.
"""

import os
import re

import pandas as pd

from src.generar_muestra import seudonimizar

# Palabras funcionales por idioma: baratas de contar y suficientes para una
# heuristica razonable. Quien escribe en ingles casi no puede evitar "the",
# igual que "el/la" en castellano.
STOPWORDS = {
    "es": ["el", "la", "de", "en", "muy", "gracias", "departamento", "excelente",
           "ubicacion", "recomiendo", "estadia"],
    "en": ["the", "and", "was", "great", "very", "thank", "stay", "apartment",
           "location", "would", "clean"],
    "pt": ["o", "a", "de", "muito", "obrigado", "apartamento", "otimo", "estadia",
           "localizacao", "recomendo"],
    "fr": ["le", "la", "de", "tres", "merci", "appartement", "excellent",
           "emplacement", "sejour", "tres"],
}

# Menciones de cada comodidad en castellano e ingles. Solo se mapean las
# comodidades que la gente efectivamente puede comentar en una resena; las
# demas quedan fuera porque casi nadie escribe sobre ellas.
KEYWORDS_AMENIDADES = {
    "amen_self_check_in": r"self.?check|check.?in auto|llegada autonoma|check.?in facil|easy check.?in",
    "amen_wifi": r"wifi|wi.?fi|internet",
    "amen_tv": r"\btv\b|television|netflix|cable",
    "amen_kitchen": r"cocina|kitchen",
    "amen_elevator": r"ascensor|elevator|lift",
    "amen_refrigerator": r"refrigerador|frigobar|fridge|refrigerator",
    "amen_hot_water": r"agua caliente|hot water|ducha|shower",
    "amen_hair_dryer": r"secador|hair ?dryer",
    "amen_wine_glasses": r"copas de vino|wine glass",
    "amen_oven": r"horno\b|oven",
    "amen_microwave": r"microondas|microwave",
    "amen_long_term_stays_allowed": r"larga estadia|long.?term|long stay|meses",
    "amen_iron": r"plancha\b|iron\b",
    "amen_toaster": r"tostador|toaster",
}


def cargar_resenas(ruta, ids_alojamientos, columnas=("listing_id", "date", "comments")):
    """Lee el detallado de resenas y se queda solo con las de la muestra.

    No se traen reviewer_id ni reviewer_name: no hacen falta para el agregado
    y asi los datos personales ni siquiera entran a memoria del analisis.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"No se encontro {ruta}. Es el reviews.csv.gz detallado de Inside "
            "Airbnb descomprimido; no se versiona por datos personales (D7)."
        )
    resenas = pd.read_csv(ruta, usecols=list(columnas), parse_dates=["date"])
    resenas = resenas[resenas["listing_id"].isin(ids_alojamientos)]
    resenas = resenas.dropna(subset=["comments"]).reset_index(drop=True)
    return resenas


def inferir_idioma(comentarios):
    """Infiere el idioma de cada resena contando palabras funcionales.

    Heuristica simple: el idioma ganador es el que junta mas stopwords en el
    comentario; si ninguno suma al menos un acierto, queda 'otro'. No es un
    clasificador serio, pero para un proxy de demanda extranjera alcanza y se
    puede explicar en una linea (D6).
    """
    texto = comentarios.str.lower().fillna("")
    puntajes = {}
    for idioma, palabras in STOPWORDS.items():
        patron = r"\b(" + "|".join(palabras) + r")\b"
        puntajes[idioma] = texto.str.count(patron)
    puntajes = pd.DataFrame(puntajes)
    ganador = puntajes.idxmax(axis=1)
    ganador[puntajes.max(axis=1) == 0] = "otro"
    return ganador


def contar_menciones(comentarios, keywords=None):
    """Cuenta, por comodidad, en cuantas resenas aparece alguna mencion."""
    keywords = keywords or KEYWORDS_AMENIDADES
    texto = comentarios.str.lower().fillna("")
    return {col: texto.str.contains(patron, regex=True)
            for col, patron in keywords.items()}


def procesar_resenas(ruta, ids_alojamientos, ruta_salida=None):
    """Del detallado a la tabla anonima por alojamiento.

    Devuelve una fila por alojamiento de la muestra: cuantas resenas tiene,
    que porcentaje esta en cada idioma inferido y que porcentaje menciona cada
    comodidad mapeada. No sale ningun texto, nombre ni id de persona.
    """
    resenas = cargar_resenas(ruta, ids_alojamientos)
    resenas["idioma"] = inferir_idioma(resenas["comments"])
    menciones = pd.DataFrame(contar_menciones(resenas["comments"]))
    resenas = pd.concat([resenas[["listing_id", "idioma"]], menciones], axis=1)

    agregado = resenas.groupby("listing_id").agg(
        n_resenas=("idioma", "size"),
        pct_en=("idioma", lambda s: (s == "en").mean()),
        pct_es=("idioma", lambda s: (s == "es").mean()),
        **{f"menc_{c[5:]}": (c, "mean") for c in menciones.columns},
    ).reset_index()

    if ruta_salida:
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        agregado.to_csv(ruta_salida, index=False)
    return agregado
