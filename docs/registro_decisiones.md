# Registro de decisiones — Proyecto Airbnb Santiago (Grupo 4)

Decisiones metodológicas y técnicas del proyecto, con su motivo y estado.
Se actualiza al cerrar cada fase.

| N.° | Decisión | Motivo y evidencia | Estado |
|---|---|---|---|
| D1 | Unidad de análisis: `room_type = "Entire home/apt"` | La pregunta trata sobre comprar un departamento completo; 15.383 de 18.904 anuncios son de este tipo | Tomada |
| D2 | Alojamiento activo = `number_of_reviews_ltm > 0` y `availability_365 > 0` | Excluye anuncios inactivos; 4.786 tienen ocupación estimada cero. Cumplen 13.788 (72,9 %); de ellos 12.253 son departamentos completos | Tomada |
| D3 | Métrica principal: ocupación estimada; precio como segunda métrica; ingresos solo como métrica derivada | `estimated_revenue_l365d` = ocupación × precio en el 100 % de los casos: no aporta información independiente | Tomada |
| D4 | Hablar de "ingresos estimados", nunca de rentabilidad | No hay datos de costos ni del precio de compra del departamento | Tomada |
| D5 | Eliminar datos personales al cargar, en la primera función del pipeline F2 | Protección de datos de anfitriones y huéspedes | Tomada |
| D6 | Inferir el idioma de las reseñas como aproximación a la demanda extranjera | Costo y beneficio por evaluar en F3; requiere `reviews.csv.gz` | Pendiente |
| D7 | No versionar `data/raw/` | Contiene datos personales y ~50 MB; el README documenta la descarga y la generación de la muestra | Tomada |
| D8 | Trabajar con una muestra aleatoria estratificada por comuna (~27 %, semilla 42, mínimo 1 registro por comuna) | El archivo detallado pesa ~50 MB; la muestra conserva las 32 comunas y mantiene los cuadernos livianos. `src/generar_muestra.py` la reproduce de forma determinista | Tomada |

## Datos personales eliminados en F2 (D5)

- **listings:** se eliminan `host_name`, `host_about`, `host_location`,
  `host_url`, `host_profile_url`, `host_picture_url`, `host_thumbnail_url`,
  `picture_url`, `listing_url`, `name`, `description` y
  `neighborhood_overview`. `host_id` se reemplaza por un código seudonimizado
  (hash), para seguir contando anuncios por anfitrión.
- **reviews** (si se usa en F3): se eliminarían `reviewer_name` y `comments`,
  este último después de derivar el idioma; `reviewer_id` se seudonimizaría.

## Sesgos declarados

- **Supervivencia:** la captura solo contiene los anuncios publicados en
  septiembre de 2026; los que dejaron de operar no aparecen, por lo que el
  desempeño típico queda sobrestimado.
- **Estimación de la ocupación:** `estimated_occupancy_l365d` se estima a
  partir de las reseñas (correlación 0,87 con `number_of_reviews_ltm`) y tiene
  un tope de 255 noches (~70 % del año).
- **Ingresos:** heredan el sesgo de la ocupación y suponen que el precio
  publicado se mantuvo todo el año.
- **Muestra (D8):** los indicadores se calculan sobre la muestra, no sobre el
  universo de 18.904 anuncios; la estratificación por comuna conserva la
  representación geográfica.
