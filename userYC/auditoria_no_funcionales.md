Auditoría profunda — Requisitos No Funcionales (resumen)

Contexto
- Pruebas analizadas: `userYC.test_auditoriaprofundatest`.
- Resultados relevantes: 3 pruebas en `AuditoriaProfundaTests` donde:
  - `test_basico_campos_obligatorios_y_validaciones`: OK
  - `test_intermedio_integrity_error_en_guardado`: ERROR (django.db.utils.IntegrityError: unique constraint)
  - `test_potente_operational_exception_generica_y_fuzz`: ERROR (django.db.utils.OperationalError: db down)

Requisitos no funcionales básicos (priorizados)

1. Integridad de datos
- Descripción: La aplicación debe garantizar consistencia e integridad (únicidad, constraints).
- Justificación: Fallo por `IntegrityError` indica falta de control previo a persistir o manejo transaccional.
- Criterio de aceptación: Validaciones y checks previos evitan violaciones de unicidad; las excepciones de BD se capturan y se tradujeron en respuestas controladas.

2. Robustez y manejo de errores
- Descripción: El sistema debe capturar excepciones operativas (p. ej. BD caída) y responder de forma predecible.
- Justificación: `OperationalError: db down` ocurrió durante la creación; actualmente la excepción asciende sin degradación controlada.
- Criterio de aceptación: Errores operativos devuelven código HTTP adecuado (p. ej. 503) y no provocan trazas sin control al cliente.

3. Atomicidad y transaccionalidad
- Descripción: Operaciones que tocan múltiples registros deben ser atómicas o tener compensaciones.
- Justificación: IntegrityError sugiere intentos parciales de guardado; usar transacciones evita estados intermedios.
- Criterio de aceptación: Uso de `transaction.atomic()` en puntos críticos; rollback asegurado ante fallo.

4. Observabilidad y logging
- Descripción: Registros claros, métricas y trazas para identificar fallos y su causa (DB, constraints, etc.).
- Justificación: Para diagnosticar errores como `db down` y `unique constraint` se requieren logs con contexto.
- Criterio de aceptación: Logs estructurados con request id, payload parcial y stacktrace; integración con monitor/alertas.

5. Resiliencia y recuperación
- Descripción: Retiradas suaves y reintentos con backoff para fallos transitorios de infra.
- Justificación: `db down` puede ser temporal; reintento y circuit breaker evitan fallos sistémicos.
- Criterio de aceptación: Políticas de retry en operaciones idempotentes y circuit breaker para evitar efecto cascada.

6. Validación y saneamiento de entradas
- Descripción: Validaciones estrictas en capas (serializers, modelos) para evitar datos inválidos que lleguen a la BD.
- Justificación: Previene IntegrityError y reduce la superficie de fallo en pruebas de fuzz.
- Criterio de aceptación: Tests de validación cubren reglas de unicidad/formato y rechazan entradas inválidas con 4xx claros.

7. Testabilidad
- Descripción: Código diseñado para facilitar mocks y pruebas que simulen fallos de infra sin provocar errores no capturados.
- Justificación: Los tests de auditoría ejercitan fallos (fuzz, DB down); el código debe manejar mocks que provoquen excepciones.
- Criterio de aceptación: Pruebas reproducen fallos y el sistema traduce excepciones en respuestas controladas sin romper la ejecución de la suite.

Recomendaciones rápidas de implementación
- Añadir validaciones de unicidad a nivel de aplicación antes de insertar (existence checks atomizados).
- Envolver guardados críticos en `transaction.atomic()` y capturar `IntegrityError` para devolver 409 o 400 según caso.
- Capturar `OperationalError` y devolver 503 / activar retry según política; no exponer stacktraces al cliente.
- Añadir logs estructurados y métricas para DB connectivity y errores de persistencia.
- Introducir reintentos con backoff para operaciones idempotentes y circuit-breaker para protecciones mayores.


