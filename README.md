# Análisis de alojamientos Airbnb en Santiago de Chile para la decisión de inversión inmobiliaria — Grupo 4

Un inversionista que está evaluando comprar un departamento para arriendo turístico en Santiago no tiene evidencia sistemática sobre qué ubicación, tipología y equipamiento se asocian a mayores ingresos. El proyecto describe esa relación a partir de 18.904 alojamientos publicados en Airbnb (Inside Airbnb, captura del 25–26 de septiembre de 2026), de los que se toma una muestra estratificada por comuna.

## Integrantes
- Alfredo Valenzuela Aburto
- Mauricio Martínez Quiñones
- María Laura Lanosa

## Datos
- Fuente: Inside Airbnb - Santiago, Chile (listings detallado, muestra estratificada) (Inside Airbnb, Inside Airbnb - Get the data)
- Enlace: http://insideairbnb.com/get-the-data/
- Estructura original: 18.904 filas x 90 columnas; archivo de trabajo:
  muestra estratificada y anonimizada de 5106 filas x 78 columnas
  (semilla 42, mínimo un registro por comuna)
- Ubicación esperada: `data/raw/listings.csv` (versionada: ya viene anonimizada)

### Cómo obtener los datos
1. Descargar `listings.csv` (versión detallada) de Inside Airbnb, Santiago.
   La descarga original trae datos personales y NO se versiona (`*.csv.gz`).
2. Generar la muestra en la raíz del proyecto:

       python src/generar_muestra.py ruta/al/listings.csv

   El script es determinista: con la misma entrada da la misma muestra,
   ya anonimizada (sin nombres, enlaces ni fotos; `host_id` con hash).

## Estructura del repositorio
```
data/raw/        muestra anonimizada generada por src/generar_muestra.py
data/processed/  datos tras limpieza y transformación (F2)
docs/            diccionario, registro de decisiones, metadatos y validación
src/             módulos reutilizables del proyecto
F1/ F2/ F3/ F4/  cuadernos e informes de cada fase
```

## Requisitos y ejecución
Python 3.13 o superior

    python -m venv .venv
    source .venv/Scripts/activate    # Windows, Git Bash
    # source .venv/bin/activate      # macOS y Linux
    python -m pip install -r requirements.txt

Correr los cuadernos en orden, primero F1 y después F2. Cada cuaderno
encuentra la raíz del proyecto aunque Jupyter lo abra en su propia carpeta.

### Dependencias declaradas
- ipykernel
- jupyterlab
- matplotlib==3.11.2
- notebook
- numpy==2.5.4
- pandas==3.1.1
- scikit-learn==1.9.1
- seaborn==0.13.2

## Convención de commits
Prefijos usados: docs, data, feat, fix.

## Decisiones técnicas
- Los datos son comunes a todas las fases (`data/`); los cuadernos se separan por fase.
- Semilla aleatoria fijada en 42 para asegurar reproducibilidad.
- `data/raw/` sí se versiona porque la muestra llega anonimizada; las
  descargas originales (`*.csv.gz`) no (datos personales y peso).
- Registro de decisiones numeradas (D1–D8) en `docs/registro_decisiones.md`.
