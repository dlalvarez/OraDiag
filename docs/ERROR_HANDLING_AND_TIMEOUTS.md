# Manejo de errores y timeouts

Toda conexión, consulta, collector y adaptador tiene timeout. Ninguna fuente
puede dejar colgado el diagnóstico.

## Reglas

- Conexión con timeout de conexión configurable.
- Cada consulta con `call_timeout` de `python-oracledb`, configurable por
  revisión, con un valor por defecto conservador.
- Presupuesto total de tiempo por diagnóstico: al agotarse, las revisiones
  pendientes quedan `not_evaluated` con limitación `timeout` y se emite el
  reporte con lo obtenido.
- Todo collector y adaptador falla de forma controlada y devuelve limitaciones.
- Un timeout es una limitación, no un crash.
- Una fuente fallida no impide evaluar fuentes independientes.
- Los motivos se registran exactos: vista, código ORA- o DPY- y mensaje.

## Mapeo de errores frecuentes

| Error | Significado típico | Limitación |
|---|---|---|
| ORA-00942 | Vista inexistente o sin grant | `permission_denied` o `unsupported_version` según el preflight |
| ORA-01031 | Privilegios insuficientes | `permission_denied` |
| ORA-01017 | Credenciales inválidas | `connection_failed` |
| ORA-12170, ORA-12541, ORA-12514 | Red, listener o servicio no alcanzable | `connection_failed` |
| ORA-28000 | Cuenta de OraDiag bloqueada | `connection_failed` |
| Timeout de llamada de `python-oracledb` | La consulta excedió `call_timeout` | `timeout` |

El mapeo exacto de códigos DPY- de `python-oracledb` se valida en la spec 004.

## Continuidad entre fuentes

1. **Núcleo SQL**: si la conexión falla, los dominios que dependen de SQL quedan
   `not_evaluated`, pero el propio fallo es evidencia (por ejemplo, para
   `cannot_connect`).
2. **Fuentes licenciadas**: sin licencia declarada no se consultan; con licencia
   y fallo, se registran como limitación sin afectar al núcleo.
3. **Adaptadores de plataforma**: si fallan, el núcleo sigue; si el núcleo
   falla, los adaptadores aún pueden aportar evidencia de plataforma (por
   ejemplo, un failover registrado en los eventos de RDS).

Si la base está caída, OraDiag explica qué pudo y no pudo evaluar, y con qué
fuentes.

## Reporte

El reporte muestra las revisiones no evaluadas, su motivo exacto, su impacto en
la confianza y las acciones seguras para obtener la evidencia faltante (por
ejemplo, el grant concreto que falta).
