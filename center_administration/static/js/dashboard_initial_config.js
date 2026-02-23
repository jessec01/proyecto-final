document.addEventListener('DOMContentLoaded', () => {
    const steps = document.querySelectorAll('.wizard-content');
    const indicators = document.querySelectorAll('[data-step-indicator]');
    const summaryPanel = document.getElementById('summaryPanel');
    const toast = document.getElementById('toast');
    const submitUrl = '/center_administrator/api/dashboard/config/initial/';
    let currentStep = 0;
    const wizardData = {};

    const setToast = (message, type = 'success') => {
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        setTimeout(() => toast.classList.remove('show'), 5000);
    };

    const showStep = (index) => {
        steps.forEach((step, idx) => {
            step.classList.toggle('active', idx === index);
        });
        indicators.forEach((ind, idx) => {
            ind.classList.toggle('active', idx === index);
        });
        currentStep = index;
    };

    const normalizeValue = (field) => {
        if (field.type === 'checkbox') return field.checked;
        if (field.dataset.type === 'number') return parseInt(field.value || '0', 10);
        if (field.dataset.type === 'float') return parseFloat(field.value || '0');
        if (field.tagName === 'SELECT' && field.value === 'true') return true;
        if (field.tagName === 'SELECT' && field.value === 'false') return false;
        return field.value;
    };

    const persistStepData = (stepEl) => {
        stepEl.querySelectorAll('[data-entity]').forEach((group) => {
            const entity = group.dataset.entity;
            wizardData[entity] = wizardData[entity] || {};
            group.querySelectorAll('input, select, textarea').forEach((field) => {
                if (!field.name) return;
                // Evitamos enviar archivos binarios u originar strings "C:\fakepath..." que rompan DRF.
                if (field.type === 'file') return;
                wizardData[entity][field.name] = normalizeValue(field);
            });
        });
        summaryPanel.innerHTML = `
            <div class="status-chip">Borrador actualizado</div>
            <p class="summary-note">
                Paso ${currentStep + 1}/4 guardado. Puedes navegar sin perder la información.
            </p>
        `;
    };

    document.querySelectorAll('[data-next]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const stepEl = steps[currentStep];
            const form = stepEl.querySelector('form');
            if (form && !form.reportValidity()) return;
            persistStepData(stepEl);
            showStep(Math.min(currentStep + 1, steps.length - 1));
        });
    });

    document.querySelectorAll('[data-prev]').forEach((btn) => {
        btn.addEventListener('click', () => {
            persistStepData(steps[currentStep]);
            showStep(Math.max(currentStep - 1, 0));
        });
    });

    const getCSRFToken = () => {
        const name = 'csrftoken=';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name)) {
                return decodeURIComponent(cookie.substring(name.length));
            }
        }
        return '';
    };

    document.querySelector('[data-submit]').addEventListener('click', async () => {
        let allValid = true;

        // Validación global estricta: chequeamos que ningún formulario atrás se haya saltado o vaciado
        for (let i = 0; i < steps.length; i++) {
            const f = steps[i].querySelector('form');
            if (f && !f.checkValidity()) {
                allValid = false;
                showStep(i); // Regresamos visualmente al usuario al paso faltante
                f.reportValidity(); // Mostramos el globo rojo indicando qué llenar
                break;
            }
        }

        if (!allValid) return; // Si algún campo en cualquier paso falla, se aborta el envío

        // Guardamos explícitamente los datos del último paso
        persistStepData(steps[currentStep]);

        try {
            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(wizardData)
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok) {
                let errorMsg = 'No se pudo completar la configuración.';
                if (payload.error) {
                    errorMsg = payload.error;
                } else if (Object.keys(payload).length > 0) {
                    // Convertimos errores de DRF {"campo": ["Error"]} a un solo string
                    errorMsg = Object.entries(payload).map(([k, v]) => `${k}: ${v}`).join(' | ');
                }
                throw new Error(errorMsg);
            }
            setToast('¡Configuración registrada exitosamente! Redirigiendo a tu nuevo Panel de Control...', 'success');
            setTimeout(() => {
                window.location.href = '/center_administrator/dashboard/';
            }, 3500);
        } catch (error) {
            setToast(error.message, 'error');
        }
    });
});
