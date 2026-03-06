// center_administration/static/center_administration/js/login.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        document.querySelectorAll('.error-message-inline, .server-error, .unexpected-error, .success-message').forEach(e => e.remove());

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        if (!email || !password) {
            alert("Por favor rellene todos los campos.");
            return;
        }

        const url = "/center_administrator/api/login/";
        const data = { email, password };

        fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
            .then(res => {
                if (!res.ok) throw res;
                return res.json();
            })
            .then(data => {
                if (data.access && data.refresh) {
                    localStorage.setItem('access', data.access);
                    localStorage.setItem('refresh', data.refresh);

                    // Mensaje de exito
                    const succ = document.createElement('div');
                    succ.className = 'success-message';
                    succ.innerHTML = '<p>Sesión iniciada. Redirigiendo...</p>';
                    form.insertAdjacentElement('beforebegin', succ);

                    setTimeout(() => {
                        // Va al dashboard del administrador
                        window.location.href = '/center_administrator/dashboard/';
                    }, 1000);
                } else {
                    throw new Error("Tokens no recibidos");
                }
            })
            .catch(async err => {
                let msg = "Credenciales inválidas";
                if (err instanceof Response) {
                    try {
                        const detail = await err.json();
                        msg = detail.detail || detail.error || msg;
                    } catch (_) { }
                }

                const errDiv = document.createElement('div');
                errDiv.className = 'error-message-inline server-error';
                errDiv.innerHTML = '<span>' + msg + '</span>';
                form.insertAdjacentElement('beforebegin', errDiv);
            });
    });
});
