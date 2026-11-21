# Registro de decisiones — Proyecto Airbnb Santiago (Grupo 4)

Decisiones metodológicas y técnicas del proyecto, con su motivo y su estado.
Se va actualizando cada vez que se cierra una fase.

| N.° | Decisión | Motivo y evidencia | Estado |
|---|---|---|---|
| D1 | Unidad de análisis: `room_type = "Entire home/apt"` | La pregunta trata sobre comprar un departamento completo; 15.383 de 18.904 anuncios son de este tipo | Tomada |
| D2 | Alojamiento activo = `number_of_reviews_ltm > 0` y `availability_365 > 0` | Excluye anuncios inactivos; 4.786 tienen ocupación estimada cero. Cumplen 13.788 (72,9 %); de ellos 12.253 son alojamientos completos | Tomada |
| D3 | Métrica principal: ocupación estimada; precio como segunda métrica; ingresos solo como métrica derivada | `estimated_revenue_l365d` = ocupación × precio en el 100 % de los casos: no aporta información independiente | Tomada |
| D4 | Hablar de "ingresos estimados", nunca de rentabilidad | No hay datos de costos ni del precio de compra del departamento | Tomada |
| D5 | Eliminar datos personales al generar la muestra (`src/generar_muestra.py`) y verificar la regla al cargar en F2 | Protección de datos de anfitriones y huéspedes; aplicarla en la generación permite versionar `data/raw/` (ver D7) | Tomada |
| D6 | Inferir el idioma de las reseñas como aproximación a la demanda extranjera | Heurística de palabras funcionales por idioma en `src/resenas.py` (no hay clasificador instalado); ~7 % de las reseñas recientes en inglés, ~20 % en Lo Barnechea | Tomada |
| D7 | Las descargas originales (`*.csv.gz`) no se versionan; la muestra de `data/raw/` sí, porque llega anonimizada | El original contiene datos personales y ~50 MB; la muestra anonimizada pesa ~9 MB y no tiene datos personales | Tomada |
| D8 | Trabajar con una muestra aleatoria estratificada por comuna (~27 %, semilla 42, mínimo 1 registro por comuna) | El archivo detallado pesa ~50 MB; la muestra conserva las 32 comunas y deja los cuadernos livianos. `src/generar_muestra.py` la reproduce de forma determinista | Tomada |
| D9 | `BinarizadorAmenidades` conserva la implementación con `map` por comodidad en vez de la vectorizada (`explode` + `pivot_table`) | La medición en F3 mostró que la vectorizada es ~2× más lenta y usa ~50× más memoria (54 MB vs 1 MB) al materializar una matriz densa con ~70 comodidades crudas cuando solo se usan 20 | Tomada |
| D11 | Minar menciones de comodidades en las reseñas detalladas y contrastarlas con lo declarado por el anfitrión | Responde si los huéspedes valoran las `amen_*`: solo ~7 % de las reseñas menciona siquiera la TV, y nombrar no es valorar: se estima contexto negativo junto a la mención (WiFi 22 % en queja, TV 3 %); el agregado se hace por alojamiento y los textos/nombres nunca salen a data/processed (D5) | Tomada |
| D10 | El tope de 255 noches de `estimated_occupancy_l365d` se trata como censura a la derecha | Al comparar perfiles se reporta el % de alojamientos en el tope por grupo, se usan mediana y cuartiles (robustas al tope) y el cuartil superior se declara potencialmente subestimado. Responde a la observación de la Sumativa 1 | Tomada |

## Datos personales eliminados (D5)

Se aplican en `src/generar_muestra.py` al producir la muestra versionada, y la
primera función del pipeline F2 las reaplica y las verifica al cargar
(idempotente: si el archivo cambiara, las vuelve a eliminar).

- **listings:** se eliminan `name`, `description` (pueden traer nombres o
  teléfonos), `host_name`, `host_about`, `host_location`, `host_url`,
  `host_profile_id`, `host_profile_url`, `host_picture_url`,
  `host_thumbnail_url`, `picture_url` y `listing_url`. `host_id` se reemplaza
  por un código seudonimizado (hash), para poder seguir contando anuncios por
  anfitrión.
- **reviews:** el detallado (`reviews_detalladas.csv`, 169 MB) no entra al
  análisis con nombres ni ids: `src/resenas.py` solo carga `listing_id`,
  `date` y `comments`, y exporta un agregado por alojamiento (idioma inferido
  y % de menciones por comodidad) sin ningún dato personal.

## Sesgos declarados

- **Supervivencia:** la captura solo trae los anuncios que estaban publicados
  en septiembre de 2026; los que dejaron de operar no salen, así que el
  desempeño típico queda sobrestimado.
- **Estimación de la ocupación:** `estimated_occupancy_l365d` se estima a
  partir de las reseñas (correlación 0,87 con `number_of_reviews_ltm`) y tiene
  un tope de 255 noches (~70 % del año).
- **Ingresos:** heredan el sesgo de la ocupación y asumen que el precio
  publicado se mantuvo todo el año.
- **Muestra (D8):** los indicadores se calculan sobre la muestra, no sobre el
  universo de 18.904 anuncios; la estratificación por comuna conserva la
  representación geográfica.
