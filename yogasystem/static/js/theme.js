/* theme.js - script compartido para modo oscuro (pequeño y no intrusivo)
   Uso: incluir {% static 'yogacenterwebapp/js/theme.js' %} en plantillas.
   Funcionalidad:
   - Aplica preferencia guardada en localStorage ('yoga_theme') o la preferencia del sistema.
   - Enlaza automáticamente con cualquier checkbox con id 'dark-mode-toggle'.
   - Expone window.toggleYogaTheme() para alternar desde consola.

   Nota: este archivo es intencionalmente pequeño. Validación avanzada o estilos
   adicionales deben manejarse en CSS/otros scripts.
*/

(function(){
  try{
    const root = document.documentElement;
    const savedTheme = localStorage.getItem('yoga_theme');
    const applyTheme = (t) => {
      if(t === 'dark') root.classList.add('dark'); else root.classList.remove('dark');
    };

    if(savedTheme) applyTheme(savedTheme);
    else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) applyTheme('dark');

    const dmToggle = document.getElementById('dark-mode-toggle');
    if(dmToggle){
      dmToggle.checked = root.classList.contains('dark');
      dmToggle.addEventListener('change', () => {
        const next = dmToggle.checked ? 'dark' : 'light';
        applyTheme(next);
        try{ localStorage.setItem('yoga_theme', next); }catch(e){}
      });
    }

    window.toggleYogaTheme = function(){
      const isDark = root.classList.toggle('dark');
      try{ localStorage.setItem('yoga_theme', isDark ? 'dark' : 'light'); }catch(e){}
      return isDark;
    };
  }catch(e){
    // no bloquear en caso de error
    console.warn('theme init failed', e);
  }
})();
