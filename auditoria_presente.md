# Auditoría del Estado Presente (Proyecto Yoga)

## 1. Arquitectura de Aplicaciones (Apps) y Modelos Actuales
El proyecto se encuentra dividido en una arquitectura modular orientada al de un SaaS (Software as a Service) para la administración de centros de yoga. Actualmente existen las siguientes aplicaciones confirmadas en la base de datos:

*   **Identidad y Acceso**:
    *   `userYC`: Gestión del usuario general del sistema.
    *   `center_administration`: Modelo `CenterAdministrator`, que extiende la funcionalidad del usuario para actuar como director del centro.
    *   `instructor`: Entidad `Instructor` (relacionada al centro y al usuario).
    *   `yogui` (y relacionadas como `classyogui`): Entidades destino, clientes finales que toman las clases.
*   **Núcleo de Negocio (Core)**:
    *   `centeryoga`: Entidad maestra (`YogaCenter`) que almacena la ubicación, horarios y contacto de cada local.
    *   `classyoga`: Entidad para gestionar la creación de cada rama de clases impartida.
*   **Gestión Monetaria y Suscripciones (Configuración Base)**:
    *   `packages`: Paquetes de comercialización (mensuales, anuales, etc.).
    *   `promotion`: Políticas de descuentos sobre los registros o paquetes.
    *   `rules`, `rulespackages`, `rulespayment`, `rulescenter`, `policy`: Motor de reglas y restricciones de pago, devoluciones, accesos, porcentajes.
    *   `pay`: Entidad para procesar pagos de los yoguis.
*   **Ayuda Integral**:
    *   `system_help`: Módulo recientemente diseñado para brindar una guía de uso para los usuarios a nivel estructural sin tocar las aplicaciones maestras.

## 2. Lógica Actual Soportada (Backend & Frontend)
1.  Se ha consolidado de manera robusta y exhaustiva el flujo para **Inicializar Centro (Caso de Uso AC4)** a través de una transacción atómica central (`CenterAdminConfiginitialSerializer`), el cual recoge en un solo paso: Centro, Administrador, Instructor Base, Reglas, Paquetes, Promociones y la primera Clase Inaugural.
2.  Existen validaciones RegEx dinámicas para los campos de textos, y se enmascara el control de datos complejos de Frontend a Backend mediante el empaquetado de JSON (`dashboard_initial_config.js`).

## 3. Estado de la Sesión
*   El **Iniciar de Sesión (AC2 / AC3 / Y3)** y el ruteo de usuarios (Control de Estado AC3) por permisos de perfil (`is_active_profile`) / (`is_first_session`) está definido a nivel estructural en los Serializadores Base (Token serializers).
