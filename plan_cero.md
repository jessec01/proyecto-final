# PLAN CERO: Desarrollo Acelerado (MVP Yoga Center)

Este **Plan Cero** detalla la ruta crítica de las cosas *estrictamente esenciales* para construir el Producto Mínimo Viable (MVP). Está diseñado para obviar configuraciones avanzadas (como pasarelas de pago, creación dinámica de paquetes complejos, manejo de reembolsos, ajustes visuales menores) y centrar el desarrollo en demostrar el ciclo básico de negocio de un Centro de Yoga: Un administrador que contrata/crea instructores, programa clases, y un Yogui (estudiante) que reserva su asiento en esa clase.

## Fase 1: Cimientos (Completado ✅)
1. **Modelos Base**: Usuarios, Direcciones, Yoga Center.
2. **Registro y Autenticación de Administradores**: Login, JSON Web Tokens y gestión condicional de redirecciones si la cuenta es nueva.
3. **Mega-Transacción (Configuración Guiada)**: Captura inicial y atómica de las reglas del centro (Paso a Paso).

## Fase 2: Panel MVP del Administrador (En Proceso ⏳)
*El corazón logístico del Centro. (Aquí estamos).*

1. **Gestión de Instructores (CRUD Básico)**:
   - Crear endpoint en DJango REST Framework para enlistar y registrar a un `Instructor`.
   - Modificar la vista Frontend actual para conectar la lista "Placeholder" de instructores con la API Backend (Fetch GET).
   - Crear un modal simple o un botón "Añadir Nuevo" que envíe un usuario nuevo tipo Instructor.
2. **Gestión de Clases y Horarios (Schedule)**:
   - Crear lógica Back/Front para crear una "Sesión/Clase".
   - Atributos mínimos: `Instructor`, `Fecha y Hora`, `Capacidad de la clase`, `Estatus`.

## Fase 3: Portal del Yogui Estudiante (Próximamente 🎯)
*Donde sucede el negocio.*

1. **Catálogo de Clases Disponibles (Read-Only List)**:
   - Entorno donde el estudiante puede ver todas las clases "Abiertas" creadas por el Administrador.
2. **Mecanismo de Reserva**:
   - Botón simple de "Reservar Asiento". 
   - Backend debe disminuir el cupo de la `Sesión/Clase` y crear un registro del tipo `Reserva`.

## Reglas de Desarrollo Rápido del Plan Cero
- **Sin Pagos Reales Aún**: Saltaremos la pasarela Zinli/Stripe en esta fase. Asumiremos que el estudiante puede "Agendar" y paga presencialmente en el local.
- **Sin Email Verification**: Obviar el envío real de correos electrónicos hasta que el MVP central funcione.
- **CSS Estático Limitado**: El dashboard se mantendrá funcional y con aspecto "Glassmorphism", pero sin oscuros ni temas dinámicos.

---
> **Siguiente Pasos para el Código:** Ya simplificamos el Dashboard para mostrar sólo 'Instructores', 'Clases' y Métricas esenciales. Vamos ahora por conectar el Frontend de Instructores con tu base de datos SQLite.
