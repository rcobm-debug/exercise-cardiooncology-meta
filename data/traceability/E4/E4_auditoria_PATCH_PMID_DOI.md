# E4 — Parche deduplicación PMID↔DOI (DECISIÓN E4: B)

## Objetivo
Unir grupos duplicados que quedaban separados por usar **DOI** en unos registros y **PMID** en otros (p. ej., PubMed sin DOI).

## Archivos de entrada
- `E4_master_unique_records_UPDATED.csv`
- `E4_duplicates_map_UPDATED.csv`
- `E4_import_dedup_summary_UPDATED.csv`

## Regla aplicada (puente PMID↔DOI)
1) Identificar **PMIDs duplicados** dentro de la lista de *masters* (registros únicos).
2) Para cada PMID duplicado:
   - Seleccionar como *master final* el registro con **DOI presente** (si existe).
   - Reasignar el/los *master(s)* restantes como duplicados del master final.
3) Actualizar el mapa de duplicados:
   - `record_ids`: añadir el/los registros reasignados.
   - `n_records`: recalcular como longitud de `record_ids`.
   - `sources`: combinar sin perder fuentes.

## Casos fusionados (3)
- PMID 10561296: R00033 → R00146
- PMID 3859587: R00021 → R01093
- PMID 3516918: R00020 → R00204

(Detalle completo en `E4_patch_log_PMID_DOI.csv`.)

## Recuento antes/después (verificable)
**Antes**
- Importados totales: 1.282 (suma de `n_records` en `E4_duplicates_map_UPDATED.csv`)
- Únicos (masters): 1.068 (filas en `E4_master_unique_records_UPDATED.csv`)
- Duplicados eliminados: 1.282 − 1.068 = 214

**Después del parche**
- Importados totales: 1.282 (sin cambios)
- Únicos (masters): 1.065 (filas en `E4_master_unique_records_PATCH_PMID_DOI.csv`)
- Duplicados eliminados: 1.282 − 1.065 = 217

**Cambio neto:** −3 registros únicos; +3 duplicados eliminados.

## Archivos generados
- `E4_master_unique_records_PATCH_PMID_DOI.csv` (1065 registros)
- `E4_duplicates_map_PATCH_PMID_DOI.csv` (1065 grupos)
- `E4_duplicates_map_PATCH_PMID_DOI_dedupkey_filled.csv` (mismo mapa con `dedup_key` completo usando IDs de registro)
- `E4_patch_log_PMID_DOI.csv` (trazabilidad del parche)
- `E4_templates_full_1065_PATCH_PMID_DOI.xlsx` (plantillas cribado TA/FT + hoja de parche)

## Impacto aguas abajo (para E5+)
- El número de registros a cribado Título/Resumen pasa de **1.068 → 1.065**.
- Si ya tienes decisiones TA/FT basadas en 1.068, habrá que:
  1) Reasignar decisiones de R00033/R00021/R00020 al master final correspondiente (R00146/R01093/R00204) **solo si esos masters no tenían ya decisión**.
  2) Recalcular conteos PRISMA para mantener consistencia.

