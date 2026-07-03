# Contract: CLI OraDiag Fase 1

## Commands

### `oradiag version`

Identifica la herramienta.

**Expected behavior**:
- Imprime nombre y version.
- No requiere configuracion, fixture ni conectividad.
- Salida humana en espanol.

### `oradiag run`

Ejecuta diagnostico simulado desde laboratorio.

**Options**:
- `--target <id>`: target definido en configuracion YAML.
- `--profile <name>`: perfil declarativo; Fase 1 debe soportar `diag_all`.
- `--symptom <category>`: uno de `cannot_connect`, `connection_hangs`, `errors`, `slow_performance`, `partial_impact`, `availability_down`, `unspecified`.
- `--fixture <path-or-id>`: escenario humano de laboratorio.
- `--output console|json`: formato de salida.
- `--config <path>`: ruta opcional a configuracion YAML humana.

**Behavior**:
1. Cargar y validar configuracion YAML humana.
2. Resolver target y profile.
3. Cargar fixture mediante `FixtureEvidenceProvider`.
4. Transformar fixture a Evidence Payload/modelos internos.
5. Ejecutar RCA engine con modelos validados.
6. Emitir Diagnostic Result como console o JSON.

## Error contract

Errores controlados deben:
- aparecer en espanol para humanos;
- no mostrar secretos;
- terminar con codigo distinto de cero;
- no invocar RCA engine si fallan configuracion, target, profile, fixture o validacion de payload.

Errores esperados:
- configuracion inexistente o YAML invalido;
- target inexistente;
- profile inexistente o no soportado;
- symptom invalido;
- output invalido;
- fixture inexistente o YAML invalido;
- Evidence Payload invalido.

## Non-goals

- No comandos de conectividad real.
- No endpoints web.
- No comandos para SQL, listener, SSH, alert log, AWR, ASH o historico.
