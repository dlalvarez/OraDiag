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
