// center_administration/static/center_administration/js/register.js
// Cola de validación inspirada en tu implementación de Yogui para mensajes y nodos DOM
class QueueDIV {
  constructor() { this.queue = []; this.size = 0; }
  enqueue(objectDOM) { if (objectDOM) { this.size++; this.queue.push(objectDOM); } }
  dequeue() { if (this.isEmpty()) return null; this.size--; return this.queue.shift(); }
  isEmpty() { return this.queue.length === 0; }
}

class QueueMessage {
  constructor() { this.queue = []; this.size = 0; }
  enqueue(message) { this.size++; this.queue.push(message); }
  dequeue() { if (this.isEmpty()) return null; this.size--; return this.queue.shift(); }
  isEmpty() { return this.queue.length === 0; }
}

let queue_divs = new QueueDIV();
let queue_messages = new QueueMessage();
let errorSet = new Set();
let mapinput;

function ready_data_information() {
  const fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'password', 'confirmation_password'];
  const arraydate = [];
  for (let id of fields) {
    const el = document.getElementById(id) || document.querySelector('[name="' + id + '"]');
    const val = el ? el.value : '';
    arraydate.push([id, val]);
  }
  mapinput = new Map(arraydate);
  return mapinput;
}

function processError(name, msg) {
  const key = `${name}:${msg}`;
  if (!errorSet.has(key)) {
    errorSet.add(key);
    let objectDOM = document.getElementsByName(name);
    queue_divs.enqueue(objectDOM);
    queue_messages.enqueue(msg);
  }
}

function validate_data() {
  queue_divs = new QueueDIV();
  queue_messages = new QueueMessage();
  errorSet = new Set();

  let mapdata = ready_data_information();
  let is_valid = true;

  // Username validation
  let username = mapdata.get("username").trim();
  if (username === "") { processError('username', "Nombre de usuario requerido"); is_valid = false; }
  else if (!/^(?=.*[a-zA-Z])(?!.*[#$<>])[a-zA-Z0-9_]{4,16}$/.test(username)) { processError('username', "Usuario inválido"); is_valid = false; }

  // Nombres
  let first = mapdata.get("first_name").trim();
  if (!first) { processError('first_name', "Nombre requerido"); is_valid = false; }
  else if (!/^[a-zA-Z\s]{4,16}$/.test(first)) { processError('first_name', "Nombre muy corto o inválido"); is_valid = false; }

  let last = mapdata.get("last_name").trim();
  if (!last) { processError('last_name', "Apellido requerido"); is_valid = false; }

  // Email
  let email = mapdata.get("email").trim();
  if (!email) { processError('email', "Correo requerido"); is_valid = false; }
  else if (!/^[^@]+@[^@]+\.[a-zA-Z]{2,}$/.test(email)) { processError('email', "Correo inválido"); is_valid = false; }

  // Phone
  let phone = mapdata.get("phone").trim();
  if (!phone) { processError('phone', "Teléfono requerido"); is_valid = false; }
  else if (!/^\+?[0-9]{7,15}$/.test(phone)) { processError('phone', "Formato inválido (E.164 requerido)"); is_valid = false; }

  // Password
  let pass1 = mapdata.get("password");
  let pass2 = mapdata.get("confirmation_password");
  if (pass1.includes(' ')) { processError('password', "Sin espacios"); is_valid = false; }
  if (pass1.length < 8) { processError('password', "Mínimo 8 caracteres"); is_valid = false; }
  if (pass1 !== pass2) { processError('confirmation_password', "No coinciden"); is_valid = false; }

  return is_valid;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registerForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    document.querySelectorAll('.error-message-inline, .server-error, .unexpected-error, .success-message').forEach(e => e.remove());

    if (!validate_data()) {
      while (!queue_divs.isEmpty()) {
        const div_name = queue_divs.dequeue();
        const message = queue_messages.dequeue();
        const target = (div_name && div_name[0]) ? div_name[0] : null;
        if (target) {
          const el = document.createElement('div');
          el.className = 'error-message-inline';
          el.innerHTML = '<span>' + message + '</span>';
          target.insertAdjacentElement('afterend', el);
        }
      }
      return;
    }

    // El Action URL via HTML Attribute `action` o custom API path
    const url = "/center_administrator/api/register/";
    const data = Object.fromEntries(mapinput);
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]');

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf ? csrf.value : ''
      },
      body: JSON.stringify(data)
    })
      .then(async res => {
        if (!res.ok) {
          const errorData = await res.json();
          throw errorData;
        }
        return res.json();
      })
      .then(data => {
        const succ = document.createElement('div');
        succ.className = 'success-message';
        succ.innerHTML = '<p>Administrador creado exitosamente, redirigiendo a login...</p>';
        form.insertAdjacentElement('beforebegin', succ);
        setTimeout(() => {
          window.location.href = form.getAttribute('data-success-url') || '/center_administrator/login/';
        }, 2000);
      })
      .catch(err => {
        // Remove previous messages just in case
        document.querySelectorAll('.error-message-inline, .server-error').forEach(e => e.remove());

        if (err && typeof err === 'object') {
          // DRF Errors display inline
          for (let k in err) {
            const input = document.querySelector(`[name="${k}"]`);
            if (input) {
              const el = document.createElement('div');
              el.className = 'error-message-inline';
              el.innerHTML = `<span>${Array.isArray(err[k]) ? err[k].join(', ') : err[k]}</span>`;
              input.insertAdjacentElement('afterend', el);
            }
          }
        } else {
          const errDiv = document.createElement('div');
          errDiv.className = 'server-error';
          errDiv.innerHTML = '<p>Fallo de red o servidor.</p>';
          form.insertAdjacentElement('beforebegin', errDiv);
        }
      });
  });
});
