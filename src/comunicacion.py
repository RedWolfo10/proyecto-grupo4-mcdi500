"""Tablas y figuras de la Fase 4, en unidades originales."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, PercentFormatter
import numpy as np
import pandas as pd
import seaborn as sns

from . import visualizacion as viz

AZUL = "#1B6CA8"
NARANJO = "#D95F02"
GRIS = "#8D8D8D"
FUENTE = "Fuente: Inside Airbnb, Santiago, septiembre de 2026. Muestra de alojamientos completos activos."
NOMBRES = {
    "self_check_in": "Self check-in", "long_term_stays_allowed": "Permite estadías largas",
    "wine_glasses": "Copas de vino", "hot_water_kettle": "Hervidor", "oven": "Horno",
    "microwave": "Microondas", "elevator": "Ascensor", "tv": "TV", "iron": "Plancha",
    "toaster": "Tostador", "refrigerator": "Refrigerador", "wifi": "WiFi",
    "kitchen": "Cocina", "hair_dryer": "Secador de pelo", "hangers": "Perchas",
    "cooking_basics": "Básicos de cocina", "dishes_and_silverware": "Vajilla",
    "bed_linens": "Ropa de cama", "hot_water": "Agua caliente",
    "extra_pillows_and_blankets": "Almohadas extra",
}


def estilo():
    plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold",
                         "axes.titlesize": 12, "font.size": 10})


def finalizar(fig, nota=""):
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.text(0.02, 0.02, FUENTE + ("\n" + nota if nota else ""),
             fontsize=8, color=GRIS, va="bottom")
    return fig


def preparar_visual(df):
    requeridas = {viz.OCUPACION, viz.PRECIO, viz.INGRESOS, "id", "bedrooms",
                  "banos_numero", "accommodates", "neighbourhood_cleansed"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise KeyError(f"Faltan columnas: {sorted(faltantes)}")
    if df.empty or not df["id"].is_unique:
        raise ValueError("El conjunto debe contener alojamientos con id único.")
    if not df[viz.OCUPACION].between(0, 255).all() or not (df[viz.PRECIO] > 0).all():
        raise ValueError("Ocupación fuera de rango o precio no positivo.")
    if not np.isfinite(df[[viz.PRECIO, viz.INGRESOS]]).all().all() or (df[viz.INGRESOS] < 0).any():
        raise ValueError("Precio e ingresos deben ser finitos y no negativos.")
    if not (df["accommodates"] > 0).all() or not (df["bedrooms"] >= 0).all():
        raise ValueError("Capacidad o dormitorios fuera de rango.")
    datos = viz.agrupar_comunas(df)
    datos["dormitorios_grupo"] = datos["bedrooms"].clip(upper=4).map(
        lambda v: "4 o más" if v == 4 else str(int(v)))
    datos["banos_grupo"] = datos["banos_numero"].map(
        lambda v: "Sin dato" if pd.isna(v) else "3 o más" if v >= 3 else f"{v:g}")
    datos["capacidad_grupo"] = pd.cut(datos["accommodates"], [0, 2, 4, 6, np.inf],
                                     labels=["1–2", "3–4", "5–6", "7 o más"])
    return datos


def tabla_comunas(df):
    return viz.resumen_desempeno(df, "comuna_agrupada")


def nota_excluidas(df):
    otras = df[df["comuna_agrupada"] == "Otras comunas"]
    return (f"No se muestran {otras['neighbourhood_cleansed'].nunique()} comunas con n < 30: "
            f"{len(otras)} alojamientos. El grupo Otras se conserva en la tabla.")


def figuras_comunas(df, tabla):
    datos = tabla[tabla["comuna_agrupada"] != "Otras comunas"]
    if datos.empty:
        raise ValueError("No hay comunas individuales con al menos 30 alojamientos.")
    figuras = {}
    for variable, titulo, unidad, nombre in [
        ("ocupacion", "Ocupación estimada por comuna", "Noches/año", "fig1_ocupacion_comuna"),
        ("ingresos", "Ingresos estimados por comuna", "Millones CLP/año", "fig1b_ingresos_comuna"),
    ]:
        mediana = "ocupacion_mediana" if variable == "ocupacion" else "ingresos_medianos"
        orden = datos.sort_values(mediana)
        escala = 1 if variable == "ocupacion" else 1e6
        fig, ax = plt.subplots(figsize=(9.5, 5.8))
        centros = orden[mediana] / escala
        ax.barh(orden["comuna_agrupada"], centros, color=AZUL)
        ax.errorbar(centros, range(len(orden)),
                    xerr=[(orden[mediana] - orden[variable + "_q1"]) / escala,
                          (orden[variable + "_q3"] - orden[mediana]) / escala],
                    fmt="none", ecolor="#222222", capsize=3)
        limite = (orden[variable + "_q3"] / escala).max()
        for y, (_, fila) in enumerate(orden.iterrows()):
            ax.text(limite * 1.04, y,
                    f"n={int(fila['n'])} · tope {fila['pct_en_tope']:.1%}", fontsize=8, va="center")
        ax.set_xlim(0, limite * 1.7)
        ax.set_xlabel(unidad)
        lider = orden.iloc[-1]["comuna_agrupada"]
        hallazgo = "la mayor ocupación mediana" if variable == "ocupacion" else "el mayor ingreso estimado mediano"
        ax.set_title(f"{lider} presenta {hallazgo}\nMediana y rango intercuartílico")
        figuras[nombre] = finalizar(fig, nota_excluidas(df))
    cantidades = datos.set_index("comuna_agrupada")["n"].sort_values()
    fig, ax = plt.subplots(figsize=(8, 5.8))
    ax.barh(cantidades.index, cantidades, color=AZUL)
    for y, v in enumerate(cantidades):
        ax.text(v + cantidades.max() * 0.01, y, f"n = {int(v):,}".replace(",", "."), va="center")
    ax.set_xlim(0, cantidades.max() * 1.17)
    ax.set_xlabel("Alojamientos en la muestra")
    ax.set_title("Cantidad de alojamientos por comuna (n ≥ 30)")
    figuras["fig1_cantidad_alojamientos_comuna"] = finalizar(fig, nota_excluidas(df))
    fig, ax = plt.subplots(figsize=(8, 5.8))
    ax.scatter(datos["precio_mediano"], datos["ocupacion_mediana"], s=datos["n"] * 0.4,
               alpha=0.6, color=AZUL)
    desplazamientos = {"Santiago": (3, 25), "Ñuñoa": (20, 2),
                       "Estación Central": (0, -30), "Recoleta": (4, -16),
                       "Lo Barnechea": (-80, 6)}
    for _, fila in datos.iterrows():
        ax.annotate(fila["comuna_agrupada"], (fila["precio_mediano"], fila["ocupacion_mediana"]),
                    xytext=desplazamientos.get(fila["comuna_agrupada"], (5, 6)),
                    textcoords="offset points", fontsize=8,
                    arrowprops={"arrowstyle": "-", "color": GRIS, "lw": .6})
    ax.set_xscale("log")
    ax.set_xticks([30000, 50000, 100000, 200000, 400000],
                  ["30.000", "50.000", "100.000", "200.000", "400.000"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Precio mediano por noche (CLP; escala logarítmica)")
    ax.set_ylabel("Ocupación mediana (noches/año)")
    ax.set_title("Precio y ocupación estimada por comuna")
    figuras["fig2_precio_ocupacion_comuna"] = finalizar(fig, nota_excluidas(df))
    return figuras


def tablas_configuracion(df):
    return {eje: viz.resumen_desempeno(df, eje + "_grupo").sort_values(eje + "_grupo")
            for eje in ["dormitorios", "banos", "capacidad"]}


def figuras_configuracion(df, tablas):
    figuras = {}
    tabla = tablas["dormitorios"]
    grupos = [g for g in ["0", "1", "2", "3", "4 o más"] if g in set(tabla["dormitorios_grupo"])]
    tabla = tabla.set_index("dormitorios_grupo").loc[grupos]
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    for ax, col, titulo, unidad in [
        (axes[0], "ocupacion_mediana", "Ocupación por dormitorios", "Noches/año"),
        (axes[1], "precio_mediano", "Precio por dormitorios", "CLP/noche"),
    ]:
        ax.bar(tabla.index, tabla[col], color=AZUL)
        ax.set_title(titulo)
        ax.set_xlabel("Dormitorios")
        ax.set_ylabel(unidad)
    figuras["fig3_desempeno_dormitorios"] = finalizar(fig)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([df.loc[df["dormitorios_grupo"] == g, viz.OCUPACION] for g in grupos],
               tick_labels=grupos, showfliers=False)
    ax.set_xlabel("Dormitorios")
    ax.set_ylabel("Ocupación estimada (noches/año)")
    ax.set_title("Distribución de la ocupación por dormitorios")
    figuras["fig3c_caja_ocupacion_dormitorios"] = finalizar(fig, "Cajas: P25–P75; línea: mediana. Valores atípicos no dibujados.")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(tabla.index, tabla["ingreso_huesped_mediano"] / 1e6, color=AZUL)
    ax.set_xlabel("Dormitorios")
    ax.set_ylabel("Millones CLP por plaza de capacidad al año")
    ax.set_title("Ingreso estimado normalizado por capacidad")
    figuras["fig3b_ingreso_huesped_dormitorios"] = finalizar(fig, "Divisor: capacidad anunciada, no huéspedes efectivamente alojados.")
    for eje, etiqueta in [("banos", "Baños"), ("capacidad", "Capacidad anunciada")]:
        t = tablas[eje]
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        for ax, col, unidad, escala in [
            (axes[0], "ocupacion_mediana", "Noches/año", 1),
            (axes[1], "ingreso_huesped_mediano", "Millones CLP por plaza/año", 1e6),
        ]:
            valores = t[col] / escala
            ax.bar(t[eje + "_grupo"].astype(str), valores,
                   color=[GRIS if n < 30 else AZUL for n in t["n"]])
            for x, (valor, n) in enumerate(zip(valores, t["n"])):
                ax.text(x, valor + valores.max() * .025, f"n={int(n)}", ha="center", fontsize=8)
            ax.set_ylim(0, valores.max() * 1.15)
            ax.set_xlabel(etiqueta)
            ax.set_ylabel(unidad)
            ax.tick_params(axis="x", rotation=30)
        fig.suptitle(f"Ocupación e ingreso normalizado según {etiqueta.lower()}")
        figuras[f"fig3_{eje}"] = finalizar(fig, "Gris: grupos con n < 30, solo descriptivos. La tabla informa dispersión y censura.")
    return figuras


def figura_cruce(df, comunas):
    seleccion = comunas[comunas["comuna_agrupada"] != "Otras comunas"].nlargest(6, "ocupacion_mediana")["comuna_agrupada"]
    sub = df[df["comuna_agrupada"].isin(seleccion) & df["bedrooms"].between(1, 3)]
    conteos = pd.crosstab(sub["comuna_agrupada"], sub["bedrooms"]).reindex(seleccion)
    matriz = sub.pivot_table(index="comuna_agrupada", columns="bedrooms", values=viz.INGRESOS,
                             aggfunc="median", observed=True).reindex(seleccion) / 1e6
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(matriz, mask=conteos < 10, annot=True, fmt=".1f", ax=ax, cmap="YlOrRd",
                cbar_kws={"label": "Millones CLP/año"})
    ax.set_title("Ingreso estimado según comuna y dormitorios")
    ax.set_xlabel("Dormitorios")
    ax.set_xticklabels([f"{col:g}" for col in matriz.columns])
    ax.set_ylabel("")
    return finalizar(fig, "Seis comunas con mayor ocupación mediana (n ≥ 30). Se ocultan celdas con n < 10."), conteos


def figura_amenidades(comp):
    tabla = comp.sort_values("diferencia")
    fig, ax = plt.subplots(figsize=(9, 8))
    for y, (_, fila) in enumerate(tabla.iterrows()):
        ax.errorbar(fila["diferencia"] * 100, y,
                    xerr=[[100 * (fila["diferencia"] - fila["ic_inf"])],
                          [100 * (fila["ic_sup"] - fila["diferencia"])]],
                    fmt="o", color=NARANJO if fila["significativa_bonf"] else GRIS, capsize=3)
    ax.set_yticks(range(len(tabla)), [NOMBRES.get(c, c) for c in tabla["comodidad"]])
    ax.axvline(0, color=GRIS, lw=1)
    ax.set_xlabel("Diferencia de prevalencia: cuartil superior − resto (puntos porcentuales)")
    ax.set_title(f"{int(comp['significativa_bonf'].sum())} comodidades presentan diferencias tras Bonferroni")
    return finalizar(fig, "IC individuales Newcombe-Wilson. Naranjo: Fisher con Bonferroni (p ajustado < 0,05).")


def unir_resenas(df, agregado):
    agregado = agregado.rename(columns={"listing_id": "id"})
    if {"comments", "reviewer_name", "reviewer_id"} & set(agregado.columns):
        raise ValueError("El agregado contiene datos personales.")
    datos = df.merge(agregado, on="id", how="left", validate="one_to_one")
    columnas = [c for c in agregado if c != "id"]
    datos[columnas] = datos[columnas].fillna(0)
    if not (datos["n_resenas"] >= 0).all():
        raise ValueError("El número de reseñas no puede ser negativo.")
    return datos


def resumen_resenas(df):
    total = df["n_resenas"].sum()
    if total <= 0:
        raise ValueError("No hay reseñas para calcular frecuencias.")
    filas = []
    for amen in [c for c in df if c.startswith("amen_")]:
        clave = amen.removeprefix("amen_")
        if "menc_" + clave not in df:
            continue
        menciones = (df["menc_" + clave] * df["n_resenas"]).sum()
        negativas = (df["neg_" + clave] * df["n_resenas"]).sum()
        filas.append({"comodidad": clave, "declarada": df[amen].mean(),
                      "mencionada": menciones / total, "menciones": menciones,
                      "pct_queja": negativas / menciones if menciones else np.nan})
    return pd.DataFrame(filas).sort_values("mencionada")


def idioma_comunas(df):
    datos = df.assign(resenas_ingles=df["pct_en"] * df["n_resenas"])
    totales = datos.groupby("comuna_agrupada", observed=True)[["resenas_ingles", "n_resenas"]].sum()
    totales["pct_en"] = totales["resenas_ingles"] / totales["n_resenas"].where(totales["n_resenas"] > 0)
    return totales


def figuras_resenas(df, comparacion, idiomas):
    figuras = {}
    top = comparacion.tail(5)
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(top))
    ax.barh(y + 0.2, top["declarada"], height=0.4, color=AZUL, label="Alojamientos que la declaran")
    ax.barh(y - 0.2, top["mencionada"], height=0.4, color=NARANJO, label="Reseñas que la mencionan")
    ax.set_yticks(y, [NOMBRES.get(c, c) for c in top["comodidad"]])
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Frecuencia (%); los denominadores son distintos")
    ax.set_title("Comodidades declaradas y mencionadas en reseñas")
    ax.legend(fontsize=8)
    figuras["fig6a_resenas_vs_declarado"] = finalizar(fig, "Últimos 12 meses. Menciones por diccionario: no miden preferencia ni satisfacción.")
    tabla = comparacion[comparacion["mencionada"] > 0.005].sort_values("pct_queja")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh([NOMBRES.get(c, c) for c in tabla["comodidad"]], tabla["pct_queja"], color=AZUL)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Reseñas con contexto negativo / reseñas que mencionan la comodidad (%)")
    ax.set_title("Contexto negativo detectado cerca de cada comodidad")
    figuras["fig6b_quejas_por_comodidad"] = finalizar(fig, "Heurística de palabras en una ventana de 50 caracteres; no equivale a una queja validada.")
    tabla = idiomas.drop(index="Otras comunas", errors="ignore").dropna(subset=["pct_en"]).sort_values("pct_en")
    fig, ax = plt.subplots(figsize=(8, 5.8))
    ax.barh(tabla.index, tabla["pct_en"], color=AZUL)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Reseñas inferidas en inglés (%)")
    ax.set_title("Idioma inferido de las reseñas por comuna")
    figuras["fig6c_resenas_en_ingles"] = finalizar(fig, nota_excluidas(df) + "\nEl idioma no identifica nacionalidad ni demanda extranjera.")
    return figuras


def mostrar(figuras):
    from IPython.display import Markdown, display
    lecturas = {
        "fig1_ocupacion_comuna": "Las medianas se comparan junto con su dispersión; el porcentaje en el tope identifica la censura de cada grupo.",
        "fig1b_ingresos_comuna": "Los ingresos medianos no representan rentabilidad. El segmento P25–P75 muestra diferencias entre alojamientos de una misma comuna.",
        "fig1_cantidad_alojamientos_comuna": "Santiago concentra la mayor cantidad de casos. Los conteos corresponden a la muestra, no a la oferta total de cada comuna.",
        "fig2_precio_ocupacion_comuna": "Una comuna con precio mediano mayor no necesariamente presenta mayor ocupación. El tamaño del punto representa su número de casos.",
        "fig3_desempeno_dormitorios": "El precio crece con los dormitorios, pero la ocupación no sigue el mismo patrón.",
        "fig3c_caja_ocupacion_dormitorios": "Las cajas permiten comparar dispersión y no solo medianas. La variable permanece limitada a 255 noches.",
        "fig3b_ingreso_huesped_dormitorios": "La normalización cambia la comparación respecto del ingreso total: las unidades grandes no encabezan el ingreso por plaza.",
        "fig3_banos": "Baños se compara sin separar comuna y tamaño. Estas diferencias no permiten atribuir un efecto al número de baños.",
        "fig3_capacidad": "La capacidad anunciada permite normalizar ingresos, pero no informa cuántos huéspedes se alojaron efectivamente.",
        "fig4_ingresos_comuna_dormitorios": "No se interpreta una celda sin revisar su tamaño; se ocultan las combinaciones con menos de diez casos.",
        "fig5_comodidades_cuartil_superior": "Los puntos describen equipamiento declarado. El color refleja el contraste ajustado, no causalidad ni preferencia.",
        "fig6a_resenas_vs_declarado": "Declarar y mencionar una comodidad usan denominadores distintos. Su contraste no mide satisfacción.",
        "fig6b_quejas_por_comodidad": "El contexto negativo es una detección por reglas; requiere revisión manual antes de interpretarse como queja.",
        "fig6c_resenas_en_ingles": "La proporción se pondera por cantidad de reseñas. Idioma inferido no equivale a nacionalidad.",
    }
    for nombre, figura in figuras.items():
        display(figura)
        display(Markdown("**Lectura.** " + lecturas.get(nombre, "La interpretación se desarrolla en el texto siguiente.")))
        plt.close(figura)


def exportar(figuras, tablas, carpeta_figuras, carpeta_docs):
    rutas = {nombre: viz.guardar_figura(fig, carpeta_figuras, nombre) for nombre, fig in figuras.items()}
    for nombre, tabla in tablas.items():
        tabla.to_csv(Path(carpeta_docs) / (nombre + ".csv"), index=False)
    return rutas
