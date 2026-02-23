// login.js - validación básica de login usando la lógica de registro adaptada
class QueueDIV {
  constructor() {
    this.queue = [];
    this.size = 0;
  }
  enqueue(objectDOM) {
    if (objectDOM == null) return "No se puede encolar un elemento nulo";
    this.size = this.size + 1;
    this.queue.push(objectDOM);
  }
  dequeue() {
    if (this.isEmpty()) {
      this.size = 0;
      return "Underflow";
    }
    this.size = this.size - 1;
    return this.queue.shift();
  }
  isEmpty() {
    return this.queue.length === 0;
  }
}

class QueueMessage {
  constructor() {
    this.queue = [];
    this.size = 0;
  }
  enqueue(message) {
    this.size = this.size + 1;
    this.queue.push(message);
  }
  dequeue() {
    if (this.isEmpty()) {
      this.size = 0;
      return "Underflow";
    }
    this.size = this.size - 1;
    return this.queue.shift();
  }
  isEmpty() {
    return this.queue.length === 0;
  }
}

let queue_divs = new QueueDIV();
let queue_messages = new QueueMessage();
let mapinput;

function ready_data_information() {
  const fields = ["email", "password"];
  const name_date = [];
  const value_date = [];

  for (let i = 0; i < fields.length; i++) {
    const id = fields[i];
    const el = document.getElementById(id) || document.querySelector('[name="' + id + '"]');
    const val = el ? el.value : "";
    name_date[i] = id;
    value_date[i] = val;
  }

  const arraydate = [];
  for (let i = 0; i < value_date.length; i++) {
    if (value_date[i] !== undefined) {
      arraydate.push([name_date[i], value_date[i]]);
    }
  }

  mapinput = new Map(arraydate);
  return mapinput;
}

function validate_email(email) {
  let emailnew = email.trim();
  const emailRegex = new RegExp(
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
  if (emailnew === "") {
    let objectDOM = document.getElementsByName("email");
    queue_divs.enqueue(objectDOM);
    queue_messages.enqueue("Email is required");
    return false;
  } else if (!emailRegex.test(emailnew)) {
    let objectDOM = document.getElementsByName("email");
    queue_divs.enqueue(objectDOM);
    queue_messages.enqueue("Email is invalid");
    return false;
  }
  return true;
}

function validate_password(password) {
  if (!password || password.trim() === "") {
    let objectDOM = document.getElementsByName("password");
    queue_divs.enqueue(objectDOM);
    queue_messages.enqueue("Password is required");
    return false;
  }
  if (password.includes(" ")) {
    let objectDOM = document.getElementsByName("password");
    queue_divs.enqueue(objectDOM);
    queue_messages.enqueue("Password should not contain spaces");
    return false;
  }
  return true;
}

function validate_data() {
  queue_divs = new QueueDIV();
  queue_messages = new QueueMessage();

  let mapdata = ready_data_information();
  let is_data_valid = true;

  if (!validate_email(mapdata.get("email"))) {
    is_data_valid = false;
  }
  if (!validate_password(mapdata.get("password"))) {
    is_data_valid = false;
  }

  return is_data_valid;
}

function render_inline_errors() {
  let div_element = null;
  let message = null;
  let div_name = null;

  while (!queue_divs.isEmpty() && !queue_messages.isEmpty()) {
    div_name = queue_divs.dequeue();
    message = queue_messages.dequeue();
    const target = div_name && div_name[0] ? div_name[0] : null;
    if (target) {
      div_element = document.createElement("div");
      div_element.className = "error-message-inline";
      div_element.innerHTML = '<span class="error-text">' + message + "</span>";
      target.insertAdjacentElement("afterend", div_element);
    }
  }
}

function show_form_error(message) {
  const form = document.getElementById("loginForm");
  if (!form) return;
  const existing = form.querySelector(".form-error");
  if (existing) existing.remove();
  const div = document.createElement("div");
  div.className = "error-message-inline form-error";
  div.innerHTML = '<span class="error-text">' + message + "</span>";
  form.insertAdjacentElement("afterbegin", div);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function resolve_login_endpoint(form) {
  const action = (form.getAttribute("action") || "").trim();
  if (action && action !== "#") return action;

  const path = window.location.pathname || "";
  if (path.startsWith("/yogui/")) return "/yogui/api/login/";
  if (path.startsWith("/instructor/")) return "/instructor/api/login/";
  if (path.startsWith("/center_administrator/")) return "/center_administrator/api/login/";
  return "/api/login/";
}

function resolve_redirect_path() {
  const path = window.location.pathname || "";
  if (path.startsWith("/yogui/")) return "/yogui/dashboard/";
  if (path.startsWith("/instructor/")) return "/instructor/dashboard/";
  if (path.startsWith("/center_administrator/")) return "/center_administrator/dashboard/";
  return "/";
}

// DOM ready
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    document.querySelectorAll(".error-message-inline").forEach((e) => e.remove());

    const is_form_valid = validate_data();
    if (!is_form_valid) {
      render_inline_errors();
      return;
    }

    const endpoint = resolve_login_endpoint(form);
    const payload = {
      email: mapinput.get("email"),
      username: mapinput.get("email"),
      password: mapinput.get("password"),
    };

    const csrfToken = getCookie("csrftoken");

    fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      },
      body: JSON.stringify(payload),
    })
      .then(async (response) => {
        if (response.ok) {
          return response.json();
        }
        if (response.status === 401 || response.status === 405) {
          let errorMsg = "Email o contraseña inválidos.";
          try {
            const errData = await response.json();
            if (errData && errData.detail) {
              errorMsg = errData.detail;
            }
          } catch (e) { }
          throw new Error(errorMsg);
        }
        throw new Error("No se pudo iniciar sesión. Intenta de nuevo.");
      })
      .then((data) => {
        if (data && data.access) {
          try {
            localStorage.setItem("access", data.access);
            if (data.refresh) localStorage.setItem("refresh", data.refresh);
          } catch (e) { }
        }
        window.location.href = resolve_redirect_path();
      })
      .catch((err) => {
        show_form_error(err.message || "Email o contraseña inválidos.");
        console.log(err.message);
      });
  });
});
