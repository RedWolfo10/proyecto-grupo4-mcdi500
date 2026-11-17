# Changelog — Proyecto Airbnb Santiago (Grupo 4)

Registro de mejoras y correcciones, vinculadas a commits verificables.
Formato: fecha, descripción, commit y justificación (guía Sumativa 3,
apartado 27).

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
