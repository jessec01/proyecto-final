// yogui/static/yogui/js/profile.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('profileForm');
    if (!form) return;

    const access = localStorage.getItem('access');
    if (!access) {
        alert("No tienes sesión iniciada.");
        window.location.href = '/yogui/login/';
        return;
    }

    // Fetch existing profile to populate the fields
    fetch('/yogui/api/profile/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${access}` }
    })
        .then(r => {
            if (r.status === 401) {
                alert("Tu sesión ha expirado. Por favor, inicia sesión de nuevo.");
                window.location.href = '/yogui/login/';
                throw new Error("401 Unauthorized");
            }
            return r.json();
        })
        .then(data => {
            // Si retorna una lista (porque usamos .filter) pillamos el primero
            const profile = Array.isArray(data) ? data[0] : data;
            if (profile) {
                if (document.getElementById('id_card')) document.getElementById('id_card').value = profile.id_card || '';
                if (document.getElementById('level_suscribed')) document.getElementById('level_suscribed').value = profile.level_suscribed || '';

                // Necesitamos guardar el ID
                form.dataset.id = profile.id;
            } else {
                // If it doesn't exist, they can create one on patch via manual trick, or we can warn them..
                console.log("Perfil Yogui no inicializado por completo.");
            }
        }).catch(e => console.error("Could not fetch profile", e));

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        document.querySelectorAll('.error-message-inline, .server-error, .unexpected-error, .success-message').forEach(e => e.remove());

        const id_card = document.getElementById('id_card').value.trim();
        const level = document.getElementById('level_suscribed').value.trim();
        const id = form.dataset.id;

        // Si existe el ID hacemos PATCH, si no POST.
        const url = id ? `/yogui/api/profile/${id}/` : `/yogui/api/profile/`;
        const methodType = id ? 'PATCH' : 'POST';

        const formData = new FormData();
        if (id_card) formData.append('id_card', id_card);
        if (level) formData.append('level_suscribed', level);

        const photoInput = document.getElementById('photo_profile');
        if (photoInput && photoInput.files.length > 0) {
            formData.append('photo_profile', photoInput.files[0]);
        }

        fetch(url, {
            method: methodType,
            headers: {
                "Authorization": `Bearer ${access}`
            },
            body: formData
        })
            .then(res => {
                if (!res.ok) throw res;
                return res.json();
            })
            .then(data => {
                if (!id) {
                    // Grab incoming id
                    form.dataset.id = data.id;
                }
                const succ = document.createElement('div');
                succ.className = 'success-message';
                succ.innerHTML = '<p>Perfil Yogui actualizado correctamente.</p>';
                form.insertAdjacentElement('beforebegin', succ);
            })
            .catch(async err => {
                let msg = "Error al actualizar perfil.";
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

    // Configurar botón logout si existe en el DOM
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            const refresh = localStorage.getItem('refresh');
            if (refresh) {
                fetch('/yogui/logout/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${access}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ refresh: refresh })
                }).then(() => {
                    localStorage.clear();
                    window.location.href = '/yogui/login/';
                }).catch(() => {
                    localStorage.clear();
                    window.location.href = '/yogui/login/';
                });
            } else {
                localStorage.clear();
                window.location.href = '/yogui/login/';
            }
        });
    }
});
