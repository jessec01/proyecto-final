// center_administration/static/center_administration/js/profile.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('profileForm');
    if (!form) return;

    const access = localStorage.getItem('access');
    if (!access) {
        alert("No tienes sesión iniciada.");
        window.location.href = '/center_administrator/login/';
        return;
    }

    // Opcional: Fetch existing data to populate the fields
    fetch('/center_administrator/api/center_administrator/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${access}` }
    })
        .then(r => {
            if (r.status === 401) {
                alert("Tu sesión ha expirado. Por favor, inicia sesión de nuevo.");
                window.location.href = '/center_administrator/login/';
                throw new Error("401 Unauthorized");
            }
            return r.json();
        })
        .then(data => {
            // Si retorna una lista, pillamos el primero
            const profile = Array.isArray(data) ? data[0] : data;
            if (profile) {
                document.getElementById('role').value = profile.role || '';
                document.getElementById('experience_years').value = profile.experience_years || '';
                if (document.getElementById('welcome_message')) {
                    document.getElementById('welcome_message').value = profile.welcome_message || '';
                }
                // Necesitamos guardar el ID
                form.dataset.id = profile.id;
            } else {
                alert("Primero debes completar la configuración de tu Centro para poder agregar foto de perfil y roles.");
                window.location.href = '/center_administrator/dashboard/config/';
            }
        }).catch(e => console.error("Could not fetch profile", e));

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        document.querySelectorAll('.error-message-inline, .server-error, .unexpected-error, .success-message').forEach(e => e.remove());

        const role = document.getElementById('role').value.trim();
        const exp = document.getElementById('experience_years').value;
        const msg = document.getElementById('welcome_message') ? document.getElementById('welcome_message').value.trim() : '';
        const id = form.dataset.id;

        if (!id) {
            alert("No se cargó el perfil base.");
            return;
        }

        const url = `/center_administrator/api/center_administrator/${id}/`;
        const formData = new FormData();
        if (role) formData.append('role', role);
        if (exp) formData.append('experience_years', parseInt(exp, 10));
        if (msg) formData.append('welcome_message', msg);

        const photoInput = document.getElementById('photo_profile');
        if (photoInput && photoInput.files.length > 0) {
            formData.append('photo_profile', photoInput.files[0]);
        }

        const csrf = document.querySelector('[name=csrfmiddlewaretoken]');

        fetch(url, {
            method: "PATCH",
            headers: {
                "Authorization": `Bearer ${access}`,
                "X-CSRFToken": csrf ? csrf.value : ''
            },
            body: formData
        })
            .then(res => {
                if (!res.ok) throw res;
                return res.json();
            })
            .then(data => {
                const succ = document.createElement('div');
                succ.className = 'success-message';
                succ.innerHTML = '<p>Perfil actualizado correctamente.</p>';
                form.insertAdjacentElement('beforebegin', succ);
            })
            .catch(async err => {
                let msg = "Error al actualizar.";
                if (err instanceof Response) {
                    try {
                        const detail = await err.json();
                        msg = detail.detail || detail.error || JSON.stringify(detail);
                    } catch (_) { }
                }

                const errDiv = document.createElement('div');
                errDiv.className = 'error-message-inline server-error';
                errDiv.innerHTML = '<span>' + msg + '</span>';
                form.insertAdjacentElement('beforebegin', errDiv);
            });
    });
});
