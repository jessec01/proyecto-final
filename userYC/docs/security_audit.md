**Resumen de auditoría de seguridad**

Fecha: 12 de febrero de 2026

Este documento lista vulnerabilidades detectadas rápidamente en el código actual, su impacto, archivos relevantes y recomendaciones accionables. También incluye ideas para mejoras futuras.

**Vulnerabilidades y observaciones (prioridad alta → baja)**

- **CSRF: token faltante o manejo inconsistente**
  - Impacto: Peticiones POST pueden ser rechazadas por falta de token; riesgo de mal manejo si se cambia a JWT sin ajustar cabeceras.
  - Archivos: `userYC/templates/userYC/register.html`, `userYC/static/userYC/js/register.js`
  - Recomendación: mantener `CsrfViewMiddleware` activo, asegurar `{% csrf_token %}` en formularios, y si se pasa a JWT, actualizar `fetch` para usar `Authorization` y desactivar/ajustar CSRF sólo para endpoints API protegidos por tokens.

- **Respuestas de error que filtran detalles (exposición de información)**
  - Impacto: `SaveUserView` devuelve `str(ValidationError)` o mensajes de excepción; puede filtrar trazas o detalles no deseados al cliente.
  - Archivos: `userYC/views.py`, `userYC/serializer.py`
  - Recomendación: devolver JSON estructurado con campos y mensajes (p. ej. `return Response(serializer.errors, status=400)`), y loggear internamente mensajes de excepción sin exponer stack traces en producción (DEBUG=False).

- **Confianza excesiva en validación cliente**
  - Impacto: la validación en `register.js` es útil UX, pero la seguridad debe aplicarse en servidor (ya hay validadores, verificar cobertura).
  - Archivos: `userYC/static/userYC/js/register.js`, `userYC/serializer.py`
  - Recomendación: confirmar que todas las reglas del cliente (longitudes, patrones) se repiten en el servidor y agregar pruebas unitarias para ellas.

- **Manejo de excepciones genéricas**
  - Impacto: capturas amplias pueden ocultar causas raíz; devolver 500 con mensaje genérico está bien, pero hay que evitar mostrar información sensible.
  - Archivos: `userYC/views.py`
  - Recomendación: capturar y diferenciar `IntegrityError`, `OperationalError`, `TransactionManagementError`; loggear con nivel adecuado y retornar mensajes estandarizados al cliente.

- **Ausencia de limitación de tasa / anti-bot en puntos de registro**
  - Impacto: permite intentos masivos de registro o abuso del endpoint.
  - Recomendación: agregar rate-limiting (DRF throttle, nginx rate limiting), y/o reCAPTCHA para evitar abuso.

- **Validación y normalización parcial de entradas**
  - Impacto: emails y usernames deberían normalizarse (lowercase para email), y sanitizar antes de almacenar.
  - Archivos: `userYC/serializer.py`, `userYC/models.py`
  - Recomendación: usar `validate_email` normalizando y `validate_username` consistente; aplicar `full_clean()` en modelos si conviene.

- **Falta de cabeceras de seguridad HTTP**
  - Impacto: falta de HSTS, CSP, X-Frame-Options pueden exponer a clickjacking, XSS, etc.
  - Recomendación: configurar `SecurityMiddleware`, establecer `SECURE_HSTS_SECONDS`, `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, y servir con HTTPS en producción.

- **Logging y monitoreo limitado**
  - Impacto: sin logs estructurados y alertas es difícil detectar ataques o fallos.
  - Recomendación: añadir logging centralizado, niveles, y conectar alertas (Sentry/ELK) para excepciones 5xx y autenticación fallida.

**Hallazgos menores / Code-style / operativos**

- Validaciones client-side manipulan el DOM mediante `getElementsByName` y `NodeList` — robustez OK pero preferir `querySelector` para consistencia.
- `register.js` debe evitar insertar HTML crudo (usar textContent cuando sea posible) para reducir riesgo XSS. Las cadenas de error provenientes del servidor deben tratarse como datos, no HTML.

**Recomendaciones a futuro (features / hardening)**

- Implementar verificación de correo (token enviado por email) antes de activar cuentas.
- Añadir bloqueo temporal y throttle por IP/usuario tras reintentos fallidos.
- Soporte opcional de autenticación por JWT con endpoints bien documentados y CSRF deshabilitado sólo para token-auth.
- Forzar políticas de contraseñas más fuertes (zxcvbn para evaluación), y permitir MFA (TOTP) en futuras versiones.
- Añadir pruebas automáticas de seguridad: pruebas que simulen inyecciones, fuzzing de campos, y pruebas de rate-limiting.
- Implementar Content Security Policy (CSP) y Subresource Integrity (SRI) para recursos externos.
- Preparar checklist de despliegue seguro (HTTPS obligatorio, variables secretas en secret manager, DEBUG=False, ALLOWED_HOSTS configurado).

**Archivos referenciados**

- `userYC/views.py` — manejo de errores
- `userYC/serializer.py` — validación/normalización
- `userYC/templates/userYC/register.html` — CSRF token y carga de JS
- `userYC/static/userYC/js/register.js` — validación cliente y envío

Si quieres, puedo:
- crear tickets (issues) con cada recomendación priorizada,
- añadir una plantilla `docs/SECURITY.md` con pasos de despliegue seguro,
- implementar cambios concretos (por ejemplo: respuesta JSON en `SaveUserView`, rate-limiting o normalización de email).

---
Archivo generado automáticamente por auditoría ligera del repo.
