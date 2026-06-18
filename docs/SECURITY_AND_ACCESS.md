# Seguridad y acceso

OraDiag debe operar con mínimos privilegios y proteger secretos. La seguridad es parte del diseño, no una mejora posterior.

## Autenticación prevista

- Password inline solo para pruebas controladas y con advertencias.
- Password por variable de entorno.
- Prompt interactivo futuro sin eco.
- Vault o gestor de secretos futuro.
- SSH con password o llave SSH.
- Credenciales Oracle con privilegios técnicos mínimos.

## Reglas de secretos

- No guardar passwords en el repositorio.
- No registrar passwords, tokens o cadenas sensibles en logs.
- Redactar datos sensibles innecesarios en reportes.
- Preferir referencias a secretos sobre valores literales.

## Mínimos privilegios

Los permisos Oracle deben limitarse a fuentes técnicas necesarias: catálogo, diccionario y vistas dinámicas autorizadas. Si faltan permisos, el resultado debe ser `ERROR`, `SKIPPED` o limitación, no una razón para escalar privilegios automáticamente.

## Prohibición de tablas de negocio

OraDiag no consulta tablas de negocio ni investiga datos funcionales. El dominio Datos no cambia esta regla; solo permite declarar que, sin evidencia técnica, el análisis debe continuar fuera de OraDiag.
