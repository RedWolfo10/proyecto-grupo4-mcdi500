# Changelog: Proyecto Airbnb Santiago (Grupo 4)

Registro de mejoras y correcciones, vinculadas a commits verificables.
Formato: fecha, descripción, commit y justificación (guía Sumativa 3,
apartado 27).

## 2026-11-24 · Cierre final, cambios locales sin commit

- Se revisó `main` en `9397168` antes de modificar: se conservan ABC, copia de parámetros, Template Method, pruebas de clases y paquete instalable.
- F1 verifica configuración y módulos sin sobrescribir README, dependencias ni código. F1–F4 usan kernel estándar e importación del paquete instalado.
- Se corrige la imputación con capacidad constante o una sola fila. F3 registra mínimo de siete repeticiones y memoria para cada tamaño en `docs/eficiencia_f3.csv`.
- F4 separa indicadores y figuras en módulos. Se agregan cuartiles de precio e ingreso, ingreso por comuna con RIC y comparaciones por baños y capacidad.
- Otras conserva sus registros en las tablas; se retira de los gráficos de comunas individuales y se informa la exclusión en el pie.
- Se corrigen intervalos y proporciones extremas: IC Newcombe-Wilson, Fisher y Bonferroni. La revisión por comuna/capacidad mantiene el cuartil global y ajusta la familia de pruebas retenidas.
- Se revisa la redacción de F1–F4 y se eliminan inferencias no sustentadas sobre preferencia, profesionalización, nacionalidad y causalidad. La censura y la diferencia entre ingresos y rentabilidad quedan explícitas.
- README y dependencias se actualizan. Los hallazgos identifican celdas estables y se exportan junto con las figuras.
- Se recuperan las salvaguardas de seudonimización: mapa aleatorio al generar la muestra y clave efímera por proceso en las utilidades. Las pruebas comprueban relaciones, exclusión de nombres y selección reproducible de filas.
- Se agrega el informe final en PDF y DOCX con diez páginas, 29 apartados, índice, figuras, diagrama y referencias verificadas. También se agrega el guion del video con participación repartida y cifras alineadas. El video sigue pendiente de archivo o enlace; no se acredita una entrega no recibida.

## [F4] 2026-11-15

### Agregado

- Decisión D10 en `docs/registro_decisiones.md`: el tope de 255 noches de
  `estimated_occupancy_l365d` se trata como censura a la derecha (% topado
  por grupo + mediana/cuartiles). Responde a la observación de la
  Sumativa 1 sobre el tratamiento del tope. *(commit pendiente)*
- `docs/informe_sumativa_f4.md`: informe reestructurado a los 29
  apartados del entregable. Responde a la observación sobre la estructura
  del informe. *(commit pendiente)*
- `changelog.md` (este archivo). *(commit pendiente)*

### Cambiado

- `docs/metadatos_fase3.csv` y cuaderno F3: `medicion.ganador` corregido a
  `map/bucle` (antes decía `explode()`, en contradicción con la medición
  que muestra que map es ~2× más rápido y usa ~50× menos memoria).
  *(commit pendiente)*
- `docs/registro_decisiones.md`: agregada D9 (mantener `map` en
  `BinarizadorAmenidades` por medición de eficiencia).
  *(commit pendiente)*
- `docs/vinculacion_mapa_conceptual.csv`: estados actualizados a la Fase 3
  (núcleo algorítmico, pipeline y medición implementados).
  *(commit pendiente)*
- `.gitignore`: excluido `Material_Didactico_Semana_3/` (material docente
  de referencia, no versionable). *(commit pendiente)*

## [F3] 2026-11-15

### Cambiado

- Kernel de los cuadernos unificado a `grupo4_mcdi500` (antes `grupox`
  placeholder) en `F1/S1_F1_Definicion.ipynb`,
  `F1/Untitled.ipynb` y `F3/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb`.
  *(commit pendiente)*

## [F3] Semana 2 (trabajo del equipo, ya en main)

### Agregado

- Núcleo algorítmico F3 con clases (`src/transformadores.py`,
  `src/pipeline.py`, `src/medicion.py`) y cuaderno
  `F3/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb`. Commits `bab02aa`,
  `36a73b4`, `77b77a6`, `85acad0`.
- Trabajo por ramas integrado mediante pull request (PR #1,
  `feature/f3-ajustes-cuaderno`; rama `new-feature`). Responde a la
  observación de la Sumativa 1 sobre distribución del desarrollo.

## [F4] 2026-11-20

### Agregado

- `F4/S3_F4_Visualizacion_Comunicacion.ipynb`: cuaderno de la fase final.
  Carga `listings_procesado.csv`, verifica el contrato de F2 (8 controles),
  prueba las funciones nuevas (caso normal, límite y excepción) y responde
  las tres preguntas operativas con 5 figuras exportadas a `F4/figuras/`.
- `src/visualizacion.py`: módulo nuevo con `resumen_desempeno`,
  `cuartil_superior`, `comparar_amenidades` y `guardar_figura`. Respeta D10:
  todo reporta mediana, cuartiles y % en el tope de 255 noches.
- `docs/hallazgos_f4.csv` y `docs/metadatos_f4.json`: hallazgos por figura
  y metadatos de ejecución de la fase.

### Cambiado

- `docs/vinculacion_mapa_conceptual.csv`: "Indicadores por comuna" y
  "Visualizaciones e informe final" pasan de Proyectado (F4) a Implementado.

### Notas

- Las figuras son una primera versión; el refinamiento visual queda para un
  commit posterior del equipo.

## [F4] 2026-11-20 (reseñas)

### Agregado

- `src/resenas.py`: procesa `reviews_detalladas.csv` (no versionado, D7) a un
  agregado anónimo por alojamiento (ventana de últimos 12 meses, alineada con D2): idioma inferido por palabras funcionales
  (D6) y % de reseñas que mencionan cada comodidad (D11). No cargan ni salen
  nombres ni ids de huéspedes (D5).
- `data/processed/resenas_por_listing.csv`: 3.313 filas, 18 columnas, sin
  datos personales, versionable.
- Sección 7 del cuaderno F4 con `fig6_resenas_vs_declarado.png`: lo declarado
  por el anfitrión vs. lo mencionado por huéspedes, y % de reseñas en inglés
  por comuna.
- `.gitignore`: `data/raw/reviews*.csv` (el detallado trae datos personales).

### Cambiado

- D6 pasa a Tomada (heurística de idioma; ~7 % inglés, ~20 % en Lo Barnechea). Nueva D11 en `docs/registro_decisiones.md`.
- `docs/hallazgos_f4.csv`: nueva fila para fig6.
