# Registro de decisiones: Airbnb Santiago, Grupo 4

| N.° | Decisión | Motivo y evidencia |
|---|---|---|
| D1 | Analizar `room_type == "Entire home/apt"` | Se comparan viviendas completas, no habitaciones. La categoría también incluye casas; no equivale exclusivamente a departamentos. |
| D2 | Definir actividad como reseñas en los últimos doce meses y disponibilidad futura | Se conservan `number_of_reviews_ltm > 0` y `availability_365 > 0`. El filtro puede excluir anuncios activos sin reseñas o sin disponibilidad. |
| D3 | Usar ocupación estimada como medida principal y precio e ingresos estimados como complementos | Los ingresos se relacionan con precio y ocupación; no constituyen una evidencia independiente de desempeño. |
| D4 | Distinguir ingresos estimados de rentabilidad | No se dispone de compra, gastos ni comisiones para calcular retorno de inversión. |
| D5 | Eliminar nombres y enlaces y seudonimizar anfitriones antes de publicar la muestra | `src/generar_muestra.py` utiliza un mapa aleatorio que conserva relaciones dentro del archivo. Las utilidades emplean una clave efímera por proceso. No se conserva una correspondencia con los identificadores originales. |
| D6 | Describir el idioma inferido de las reseñas, sin equipararlo a nacionalidad | Las reglas de `src/resenas.py` no tienen validación manual. Los porcentajes se ponderan por número de reseñas, no por número de anuncios. |
| D7 | Versionar la muestra y los agregados; excluir las descargas originales y comentarios | Los archivos utilizados por F1–F4 están disponibles al clonar. Los textos y nombres de reseñantes no son necesarios para ejecutar F4. |
| D8 | Utilizar muestreo estratificado por comuna, fracción aproximada de 27 %, semilla 42 y mínimo un caso | Se conserva la cobertura geográfica. La selección es reproducible; los seudónimos cambian al regenerar. Los resúmenes describen la muestra y no estiman totales del universo. |
| D9 | Conservar `map` por comodidad en `BinarizadorAmenidades` | F3 compara equivalencia, mínimo de siete mediciones de tiempo y memoria en tres tamaños. Las cifras vigentes están en `docs/eficiencia_f3.csv`; no se fijan razones de rendimiento que dependan del equipo. |
| D10 | Tratar el tope de 255 noches como censura a la derecha | Cada grupo informa porcentaje en el tope, mediana y P25–P75. No se pueden distinguir ocupaciones superiores; el efecto sobre un cuantil depende de cuántos casos estén censurados. |
| D11 | Contrastar comodidades declaradas con menciones y contexto negativo | Las reglas de texto aportan una revisión exploratoria. Ni una mención prueba valoración ni su ausencia prueba indiferencia. El contexto negativo no constituye una queja validada. |
| D12 | Template Method con pipeline por composición | La base abstracta fija ajuste y transformación; las clases concretas implementan aprendizaje y aplicación. Los parámetros se consultan mediante copia profunda. No se implementan estrategias de imputación intercambiables. |
| D13 | Agrupar comunas con menos de 30 alojamientos en las tablas | Otras se calcula desde los registros originales. Los gráficos de comunas individuales excluyen ese grupo e informan cuántos casos no muestran. No se interpreta Otras como una ubicación. |
| D14 | Comparar prevalencias con IC Newcombe-Wilson, Fisher y Bonferroni | Se manejan proporciones extremas y grupos pequeños. Los IC del 95 % son individuales; el ajuste se aplica a los p-valores. La familia global contiene veinte comodidades. |
| D15 | Revisar confusión por comuna y capacidad manteniendo P75 global | Se comparan estratos con al menos diez anuncios en cada grupo y se corrige la familia completa de pruebas retenidas. No se afirma que este análisis controle toda la confusión. |

## Privacidad

La muestra no contiene nombres, descripciones ni enlaces de perfiles. `host_id`
es un seudónimo para conservar relaciones entre anuncios, no una variable de
magnitud. La muestra ya versionada se utiliza sin regenerarla en F1–F4.

El procesamiento opcional del detallado de reseñas utiliza comentarios en
memoria para producir `resenas_por_listing.csv`. Ese agregado no conserva
texto, nombres ni identificadores de reseñantes. El archivo de comentarios no
se requiere para ejecutar los resultados de F4.

## Limitaciones

La captura es transversal. El filtro de actividad introduce selección y sesgo
de supervivencia, sin que pueda cuantificarse aquí su dirección o magnitud.
La ocupación no corresponde a reservas observadas y está limitada a 255 noches.
Los ingresos heredan sus supuestos y utilizan el precio publicado.

La muestra conserva cobertura por comuna, pero los resúmenes globales no usan
ponderadores para estimar el universo. Los intervalos estadísticos tampoco
incorporan por completo la estratificación ni la dependencia entre anuncios
del mismo anfitrión. Las diferencias se interpretan como asociaciones
exploratorias, no como efectos causales.
