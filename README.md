# Airbnb en Santiago: ocupación e ingresos estimados (Grupo 4)

Proyecto MCDI500, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

## Pregunta

¿Qué ubicación, configuración y comodidades presentan los alojamientos completos activos con mayor ocupación e ingresos estimados? El análisis describe asociaciones; no estima rentabilidad porque no dispone de precio de compra ni costos.

## Integrantes

- Alfredo Valenzuela Aburto
- Mauricio Martínez Quiñones
- María Laura Lanosa

## Datos y procedencia

- Fuente oficial: Inside Airbnb, Santiago, Chile. http://insideairbnb.com/get-the-data/
- Captura: 25–26 de septiembre de 2026, según `last_scraped`.
- Universo de origen documentado: 18.904 anuncios; muestra estratificada por comuna de 5.106 filas, fracción aproximada 27 %, semilla 42.
- Entrada versionada: `data/raw/listings.csv`, sin nombres, enlaces ni comentarios y con identificador de anfitrión seudonimizado.
- Procesado: `data/processed/listings_procesado.csv`, alojamientos completos con reseñas recientes y disponibilidad futura.
- Reseñas: `data/processed/resenas_por_listing.csv` conserva solo agregados por alojamiento. Los comentarios originales no se versionan.

La fecha de captura no es la fecha de descarga. No se conserva un registro verificable de la fecha exacta de descarga inicial; no se atribuye una fecha inventada.

Para obtener una nueva muestra, descargar el `listings.csv.gz` detallado de la fuente oficial y ejecutar:

```bash
python src/generar_muestra.py ruta/al/listings.csv.gz
```

La selección de filas usa una semilla fija. Los seudónimos de anfitrión se generan de nuevo al anonimizar, por lo que no deben compararse entre muestras regeneradas. No es necesario regenerar la muestra para ejecutar el proyecto.

## Instalación

Python 3.13 o superior; la última verificación registra la versión concreta en los cuadernos y en `docs/metadatos_f4.json`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
python -m ipykernel install --user --name grupo4_mcdi500 --display-name "Python (grupo4_mcdi500)"
python -m jupyter lab
```

En Windows, activar con `.venv\Scripts\activate`. En Jupyter seleccionar el kernel del entorno. Los cuadernos usan el identificador estándar `python3`; si apunta a otro intérprete, seleccionar `Python (grupo4_mcdi500)` antes de ejecutar.

Las dependencias utilizadas directamente y sus versiones están en `requirements.txt`. El paquete `src` se instala en modo editable; no se modifica `sys.path` desde los cuadernos.

## Ejecución

Ejecutar de principio a fin, en orden:

1. `F1/S1_F1_Definicion.ipynb`: definición, procedencia y verificación del entorno.
2. `F2/S1_F2_Preprocesamiento.ipynb`: preparación y exportación del procesado.
3. `F3/S2_F3_NucleoAlgoritmico_Eficiencia_POO.ipynb`: clases, equivalencia de 26 columnas y eficiencia.
4. `F4/S3_F4_Visualizacion_Comunicacion.ipynb`: indicadores y comunicación de resultados.

Desde la raíz, también se puede ejecutar cada cuaderno con:

```bash
python -m jupyter nbconvert --execute --inplace F4/S3_F4_Visualizacion_Comunicacion.ipynb
```

Las rutas de entrada y salida son relativas al repositorio. F1 verifica los archivos de configuración sin sobrescribir las correcciones de las fases posteriores.

## Fase 4

El cuaderno llama a `src/visualizacion.py` para indicadores y comparaciones y a `src/comunicacion.py` para tablas y figuras. Se conserva una copia interpretable con unidades originales.

- Comunas: mediana y P25–P75 de ocupación, precio e ingresos, tamaño y porcentaje censurado. Las comunas con n < 30 se agrupan como Otras en las tablas; los gráficos de comunas individuales informan los casos excluidos en el pie.
- Configuración: dormitorios, baños y capacidad; ingreso total y normalizado por capacidad anunciada o dormitorio. No representa huéspedes realmente alojados.
- Comodidades: diferencias de prevalencia con IC individuales Newcombe-Wilson, Fisher y Bonferroni. Se repite por comuna y capacidad manteniendo P75 global. Es un análisis observacional y exploratorio.
- Reseñas: menciones, contexto negativo e idioma inferido mediante reglas. No identifican preferencias, nacionalidad ni quejas validadas.

Figuras principales en `F4/figuras/`:

- `fig1b_ingresos_comuna.png`: ingreso mediano e intervalo intercuartílico.
- `fig3c_caja_ocupacion_dormitorios.png`: distribución de ocupación.
- `fig5_comodidades_cuartil_superior.png`: diferencias e IC del 95 %.

Cada ejecución regenera las figuras PNG y las tablas de `docs/`. `docs/hallazgos_f4.csv` identifica la celda de origen de cada cifra mediante un ID estable. El informe y el video deben usar esa misma ejecución.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren transformadores, pipeline, medición, agrupación de comunas, indicadores, intervalos, datos límite y figuras. Los tiempos comparativos de F3 quedan en `docs/eficiencia_f3.csv` y cambian con el equipo.

## Límites

La ocupación se estima desde reseñas y está censurada en 255 noches. La captura es transversal y el filtro de actividad introduce sesgo de supervivencia. Las asociaciones no prueban causalidad; los ingresos estimados no son rentabilidad. Los intervalos no incorporan completamente el diseño muestral ni la dependencia entre anuncios de un mismo anfitrión.

## Informe y video

El informe final queda en `docs/Informe_Final_Grupo4_MCDI500_Fase4.pdf`; también se conservan la versión editable `.docx` y el texto fuente `.md`. El PDF tiene diez páginas, índice correspondiente y las cifras de la ejecución verificada. El guion del video queda en `docs/guion_video_f4.md`, con los mismos números y figuras del informe. El video de 5–8 minutos se entrega por Canvas; no se dispone todavía de su archivo o enlace para verificarlo desde este repositorio. Deben participar los tres integrantes y coincidir con las cifras exportadas.

## Organización y trazabilidad

`src/` contiene módulos, `tests/` sus pruebas, `data/` las entradas y salidas y `docs/` decisiones y evidencia. El patrón de F3 es Template Method con pipeline por composición. El registro de decisiones y `changelog.md` documentan la evolución. Se utilizan ramas y PR; los mensajes de commit describen cambios con prefijos `feat`, `fix`, `data` o `docs`.
