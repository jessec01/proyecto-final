# Auditoría de Requerimientos y Casos de Uso (Gap Analysis)

*Nota: Por requerimiento del sistema se ignoran los casos de uso "Gestionar Notificaciones (AC5)" y "Ver Reporte (AC8)".*

## 1. Caso de Uso Explícito: Y1 Ubicar Centro
### Definición Lógica Exigida
Para el actor principal (**Yogui**), ubicar un centro de yoga marca el inicio de toda la interacción con el sistema. Funciona como un catálogo visual.

*   **Flujo Ideal:** El usuario (esté o no registrado como Yogui aún) entra a la plataforma. Visualiza un buscador principal que se conecta a la API. Esta vista arrojará una lista de los `YogaCenter` públicos activos, mostrando nombre, descripción y dirección (`hours_of_operation`).
*   **Comportamiento de la lógica Backend:**
    1.  Se necesita un Endpoint (Ej: `GET /api/centeryoga/search/`) sin necesidad de Token inicial o con permisos públicos de solo lectura (`AllowAny`).
    2.  Este endpoint devuelve todos los centros disponibles junto a su `codigo` identificador.
    3.  El usuario (Yogui) da *clic* a un centro específico, lo que habilita que salte al requerimiento **Y2 Registro**, donde el Yogui se matriculará como "Hijo/Cliente" de ese `YogaCenter` en específico a través del código que acaba de escoger de la ubicación.

---

## 2. Lógicas y Modelos Faltantes (Lo que falta codificar)

Al contrastar tu base de datos presente contra el `.docx` de Casos de Uso, he detectado que careces de algunas entidades clave para cerrar el flujo de los Instructores y Yoguis:

### A) Modelos (Base de Datos) Faltantes
1.  **Modelo de Reserva o Matriculación (`Reservation` / `Booking`)**
    *   *(Cubre los Casos Y7 Reservar y Y5 Ver Clases)*: Tu Yogui puede comprar un paquete (`Y8`), pero necesitas una tabla que cruce `Yogui` con `ClassYoga` y con un campo `Date` (Fecha) o `Schedule` exacto apartado en el tiempo. Si no, no sabrás para qué clase ni a qué hora reservó.
2.  **Modelo de Instancia de Clase (Diaria) y Asistencia (`ClassSession` y `Attendance`)**
    *   *(Cubre el Caso I4 Gestionar Clases)*: El instructor necesita pasar asistencia. No puede hacerlo en el modelo superior `ClassYoga`. Necesita un modelo que represente la clase de un día particular (ej. *Hatha Yoga - Jueves 15 a las 10AM*) y otra de `Attendance` donde se relacione a los Yoguis que asistieron y a los que se ausentaron.
3.  **Modelo de Suscripción Activa (`YoguiSubscription` / `ActivePackage`)**
    *   *(Cubre los Casos Y8 Comprar Paquete)*: Tienes los `Packages` (El producto en la tienda) y el `pay` (La factura). Debes relacionar qué Yogui es dueño de qué paquete actualmente y cuánto le falta para expirar el *"access_days"*.

### B) Lógica de Backend (APIs y Reglas) por Desarrollar
Para dar vida a los casos que todavía no hemos tocado, programarás estas lógicas clave de validación:
1.  **Lógica del Balance o Acceso de Paquetes (Backend Validation)**
    *   Para que un Yogui ejecute el caso **Y7 (Reservar)**, debe existir un método backend que revise si tiene un paquete comprado válido `has_active_subscription()`, antes de dejarlo ocupar un puesto.
2.  **Lógica de Creación Multi-Día de Horario (AC7 Crear Horario)**
    *   Será necesario un bloque de código en Python que no solo guarde un texto de JSON (`schedules`), sino que tome una plantilla y auto-genere entradas semanales en la base de datos de manera recursiva (para predecir cuándo el Instructor deberá dar clase).
3.  **Filtrados por Rol (I4 / S1)**
    *   El caso del Instructor gestionando clases requiere restricciones severas de Backend: *Solo veo a LOS YOGUIS que reservaron MI clase particular*. No a todos los Yoguis del centro. Esto exige escribir métodos `.filter(instructor=self.request.user.instructor)` para casi todas las vistas de Instructor.
