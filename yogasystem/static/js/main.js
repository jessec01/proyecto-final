// Delegación: un listener central que redirige según el atributo `data-href`
document.addEventListener('click', function (e) {
  const btn = e.target.closest('[data-href]');
  if (!btn) return;
  e.preventDefault();
  const href = btn.dataset.href || btn.getAttribute('href');
  if (href) window.location.href = href;
});

// Inicialización ligera al cargar el DOM
document.addEventListener('DOMContentLoaded', function(){
  // 1) Conexión con `theme.js`: si existe una función global para alternar tema,
  //    vincularla a cualquier elemento con id 'dark-mode-btn' (botón) o
  //    al checkbox 'dark-mode-toggle'. `theme.js` ya hace el binding para
  //    el checkbox con id 'dark-mode-toggle', así que aquí sólo añadimos
  //    el soporte para un botón si se prefiere ese control en la UI.
  const dmBtn = document.getElementById('dark-mode-btn');
  if(dmBtn && window.toggleYogaTheme){
    dmBtn.addEventListener('click', function(){ window.toggleYogaTheme(); });
  }

  // 2) Nota sobre modo Empresa/Usuario:
  //    Actualmente la plantilla `home.html` contiene un script inline que
  //    alterna los CTAs basados en botones con clase 'mode-btn' y atributos
  //    `data-mode`. Para centralizar la lógica en este archivo y mejorar
  //    mantenibilidad, se debería mover esa función aquí y:
  //      - Persistir el modo seleccionado en `localStorage` (clave 'yc_mode')
  //      - Emitir eventos personalizados (p.ej. 'yc:mode-changed') para
  //        que otros módulos reaccionen (analytics, forms dinámicos)
  //      - Actualizar `aria-pressed` en los botones de modo por accesibilidad
  //    Falta implementar: consolidar/migrar la lógica inline del template a
  //    este archivo, y asegurar que las rutas de las CTAs existen en el backend.

  // 3) Falta por agregar (comentario):
  //    - Sincronización con servidor: si el modo debe asociarse a la sesión
  //      del usuario (empresa vs usuario), hay que exponer una API para
  //      guardar la preferencia y restaurarla al iniciar sesión.
  //    - Tests de accesibilidad y soporte para teclas (keyboard navigation).
});