# Decision Log

## ADR-0001: OraDiag es RCA, no health check
- **Estado**: aceptada.
- **Decisión**: OraDiag investigará incidentes reportados y no listará anomalías generales como objetivo principal.
- **Consecuencia**: todo hallazgo debe clasificarse causalmente.

## ADR-0002: No consultar tablas de negocio
- **Estado**: aceptada.
- **Decisión**: solo se consultarán fuentes técnicas.
- **Consecuencia**: problemas funcionales se derivan fuera de OraDiag.

## ADR-0003: Síntoma como pista, no verdad
- **Estado**: aceptada.
- **Decisión**: el síntoma prioriza, pero la evidencia decide.
- **Consecuencia**: se evita sesgo de anclaje.

## ADR-0004: Separar causa principal de hallazgos incidentales
- **Estado**: aceptada.
- **Decisión**: se usarán roles causales explícitos.
- **Consecuencia**: reportes más útiles y menos ruidosos.

## ADR-0005: Usar dominios causantes
- **Estado**: aceptada.
- **Decisión**: todo diagnóstico relevante intentará clasificar dominio.
- **Consecuencia**: facilita asignación al equipo correcto.

## ADR-0006: Perfiles desde el diseño inicial
- **Estado**: aceptada.
- **Decisión**: los perfiles agruparán revisiones sin cambiar reglas RCA.
- **Consecuencia**: permite ejecución enfocada.

## ADR-0007: Consola como salida obligatoria futura
- **Estado**: aceptada.
- **Decisión**: console será salida base; json, markdown y html vendrán después.
- **Consecuencia**: operación inicial sencilla.

## ADR-0008: Histórico como fase futura
- **Estado**: aceptada.
- **Decisión**: el histórico de incidentes no se implementa al inicio.
- **Consecuencia**: se evita complejidad temprana y se mantiene en roadmap.

## ADR-0009: Reinicio de la implementación con Claude Code
- **Estado**: aceptada (2026-11-21).
- **Decisión**: el código de las antiguas specs 001 y 002 no se reutiliza. La planeación se reescribe bajo la constitución v2.0.0 y la implementación se hace con Claude Code a partir de specs aprobadas, en la rama `develop-claude`.
- **Motivo**: el motor anterior calculaba la causa sumando pesos por severidad, sin correlación temporal ni cadenas causales; el costo de rehacer era bajo frente al de corregir.
- **Consecuencia**: las specs 001 y 002 quedan como históricas; la nueva agrupación inicia en 003.

## ADR-0010: Núcleo SQL independiente de plataforma
- **Estado**: aceptada (2026-11-21).
- **Decisión**: toda evidencia obligatoria se obtiene por SQL de solo lectura; CloudWatch, eventos RDS, SSH y APIs de OCI son adaptadores opcionales.
- **Motivo**: servir para cloud y on-premise sin dependencia de un proveedor.
- **Consecuencia**: sin adaptador, los dominios de host, volumen e infraestructura de plataforma quedan `not_evaluated` y bajan la confianza; el diagnóstico sigue siendo posible.

## ADR-0011: Packs de Oracle deshabilitados por defecto
- **Estado**: aceptada (2026-11-21).
- **Decisión**: ASH, AWR y demás fuentes de Diagnostics/Tuning Pack solo se usan con licencia declarada en el target y parámetro coherente. Nunca se infiere la licencia.
- **Motivo**: riesgo de auditoría de licenciamiento en un entorno bancario.
- **Consecuencia**: sin licencia, el RCA de incidentes pasados tiene menor confianza; se prefiere declararlo antes que usar fuentes no licenciadas. Statspack queda fuera del alcance inicial por decisión del responsable del proyecto.

## ADR-0012: Amazon RDS for Oracle como plataforma inicial
- **Estado**: aceptada (2026-11-21).
- **Decisión**: las specs se validan primero contra RDS for Oracle Enterprise Edition; on-premise y OCI se agregan después con el mismo núcleo.
- **Consecuencia**: cada spec documenta grants vía `rdsadmin` y limitaciones por ausencia de acceso al host.

## ADR-0013: Solo lectura estricta
- **Estado**: aceptada (2026-11-21).
- **Decisión**: OraDiag solo ejecuta `SELECT`; no genera archivos en el servidor ni invoca procedimientos que cambien estado, incluidos los de `rdsadmin` que crean reportes AWR/ASH.
- **Consecuencia**: el análisis de AWR/ASH se hace consultando las vistas, no generando reportes.
