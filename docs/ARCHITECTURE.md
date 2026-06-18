# Arquitectura conceptual

La arquitectura futura separa recolección, evaluación, correlación y reporte para evitar que un collector determine conclusiones RCA sin contexto.

## Componentes

- **CLI**: entrada futura para ejecutar perfiles, targets y formatos de salida.
- **Configuración**: targets, credenciales referenciadas, timeouts y límites.
- **Perfiles**: agrupaciones de revisiones; no cambian reglas RCA.
- **Connectors**: capas SSH, SQL, archivos/logs y APIs futuras, todas con timeout.
- **Discovery**: identificación de instancia, versión, CDB/PDB, RAC, ASM y standby.
- **Collectors**: recolección técnica sin conclusiones definitivas.
- **Checks**: evaluación de reglas sobre datos recolectados.
- **RCA Engine**: correlación, roles causales, dominios y confianza.
- **Evidence Model**: estructura común para evidencias, limitaciones y datos detallados.
- **Reporters**: salidas futuras console, json, markdown y html.
- **History Store**: histórico futuro de incidentes y resoluciones confirmadas.
- **Knowledge Base**: recomendaciones y patrones técnicos futuros.

## Árbol conceptual futuro

```text
src/oradiag/
  cli/
  config/
  core/
  connectors/
  discovery/
  collectors/
  checks/
  rca/
  reports/
  history/
  sql/
```

## Flujo lógico

1. Cargar configuración y perfil.
2. Intentar conectividad por capas.
3. Descubrir contexto Oracle disponible.
4. Recolectar evidencias técnicas.
5. Evaluar revisiones con estados uniformes.
6. Correlacionar hallazgos con el síntoma opcional.
7. Clasificar dominio causante y rol causal.
8. Emitir reporte con OK, problemas, limitaciones y recomendaciones.
