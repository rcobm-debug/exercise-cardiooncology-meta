# Reproducibilidad: metaanálisis de ejercicio y desenlaces cardiacos en cáncer de mama

Este repositorio contiene el **código** y los **datos derivados** necesarios para reproducir los metaanálisis y las figuras cuantitativas (forest plots) reportadas en el manuscrito.

Versión pública actual: v1.0.5
Zenodo (versión archivada): [PENDING_NEW_ZENODO_VERSION_DOI]

Novedades en v1.0.5
- Actualización del paquete de trazabilidad de figuras para el envío a revista.
- Inclusión de una figura compuesta vertical ensamblada a partir de los outputs validados de Figure 4 y Figure 5.
- Actualización de archivos de procedencia/empaquetado para las Figuras 4–7.

Importante: no se han modificado los datos extraídos, los cálculos meta-analíticos, los resultados ni las conclusiones.

## Contenido
- `scripts/run_all.py`: reproduce los metaanálisis (DerSimonian–Laird) e intervalos Hartung–Knapp.
- `scripts/make_forestplots.py`: genera forest plots (Figuras 4–7) a partir de los CSV derivados.
- `data/derived/`: datasets derivados (CSV/XLSX) para análisis y síntesis SWiM.
- `data/traceability/`: trazabilidad por etapas (E4–E9) con registros de deduplicación, cribado, exclusiones y extracción.
- figures/published/: PNG finales de Figuras 1–7 y figura compuesta derivada de Figures 4–5 para el paquete editorial/trazable.

> Nota sobre derechos de autor: este repositorio **no incluye** PDFs a texto completo ni material protegido (p. ej., textos completos/figuras de artículos). Solo incluye **datos derivados** y metadatos necesarios para reproducibilidad.

## Requisitos
- Python 3.10+ (recomendado 3.11)

Instalación:
```bash
pip install -r requirements.txt
```

## Reproducir análisis
```bash
python scripts/run_all.py
python scripts/session_info.py
```

## Generar forest plots (Figuras 4–7)
```bash
python scripts/make_forestplots.py
```

## Procedencia de figuras
- **Figura 1 (PRISMA 2020):** generada con PRISMA2020 (web/Shiny) usando los recuentos en `data/derived/E5_PRISMA_counts.csv`.
- **Figuras 2–3 (RoB 2):** generadas con *robvis* usando `data/derived/E8_RoB2_table_LVEF_GLS.csv`.
- **Figuras 4–7 (forest plots):** generadas con Python (`scripts/make_forestplots.py`) usando `data/derived/`.
- Figura compuesta Figure 4–5 (panel a/panel b): ensamblada a partir de los outputs validados de Figure 4 y Figure 5 para el paquete de trazabilidad/editorial; no implica recálculo de resultados.

## Licencia
MIT (ver `LICENSE`).
