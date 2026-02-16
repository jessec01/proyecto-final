class QueueDIV {
  constructor() {
    this.queue = []; 
    this.size=0; 
  }
  enqueue(objectDOM) {
   if(objectDOM == null) {
         return "No se puede encolar un elemento nulo"; 
   }
   let div_element=objectDOM;  
   this.size=this.size+1; 
   this.queue.push(div_element);
  }
    dequeue() { 
    if (this.isEmpty()) { 
        this.size=0; 
        return "Underflow";
         
    } 
    this.size=this.size-1; 
    return this.queue.shift(); 
    } 
    getSize(){ 
        return this.size; 
    } 
    isEmpty() { 
    return this.queue.length === 0;      
    } 
}
class QueueMessage{
  constructor() {
    this.queue = []; 
    this.size=0;
  }
  enqueue(message) {
   this.size=this.size+1; 
   this.queue.push(message);
  }
    dequeue() { 
    if (this.isEmpty()) {
        this.size=0;  
        return "Underflow"; 
    } 
    this.size=this.size-1;  
    return this.queue.shift(); 
    } 
        isEmpty() { 
        return this.queue.length === 0; 
        }
    getSize(){ 
        return this.size; 
    } 
}




//definir una cola de divs para manejar la ubicacion de los spans
let queue_divs=new QueueDIV();
//definir una cola de mensaje de error 
let queue_messages=new QueueMessage(); 
let mapinput; 
// conjunto para evitar mensajes de error duplicados (campo:mensaje)
let errorSet = new Set();
// An array of messages is defined to store a flexible array of objects for defining new dynamic spans.
//function para leer los datos del formulario 
function ready_data_information(){

    let value_date=[];
    const name_date=[];
    // The logic to access DOM fields was reduced
    // by accessing with document.querySelectorALL 

    // Read known fields explicitly to avoid depending on DOM order
    const fields = ['email','username','first_name','last_name','phone','password','confirmation_password'];
    for (let i=0;i<fields.length;i++){
        const id = fields[i];
        const el = document.getElementById(id) || document.querySelector('[name="'+id+'"]');
        const val = el ? el.value : '';
        name_date[i]=id;
        value_date[i]=val;
    }
    //console.log(code);
    const arraydate=[];
    for (let i=0;i<value_date.length;i++){
        if (value_date[i]!==undefined ){
            arraydate.push([name_date[i],value_date[i]]);
        }
   }
    // Creates a map with the input name and value for validation
    mapinput=new Map(arraydate);
    //alert("llegue aqui y no me detuve2");
    //console.log(mapinput); 
    return mapinput;
}
function validate_data(){
    // This allows resetting error states
    queue_divs=new QueueDIV(); 
    queue_messages=new QueueMessage(); 
    // reset dedupe set
    errorSet = new Set();
    
    let mapdata=ready_data_information();
    var is_data_valid=true; // Variable to track overall validity
    // Existing validations
    if (!validate_username(mapdata.get("username"))){
        is_data_valid=false;
    }
    if (!validate_first_name(mapdata.get("first_name"))){
        is_data_valid=false;
    }
    if (!validate_last_name(mapdata.get("last_name"))){
        is_data_valid=false;
    }
    if (!validate_email(mapdata.get("email"))){
        is_data_valid=false;
    }
    if (!validate_phone(mapdata.get("phone"))){
        is_data_valid=false;
    }
    if (!validate_password_timenow(mapdata.get("password"))){
        is_data_valid=false;
    }
    if (!validate_phone(mapdata.get("phone"))){
        is_data_valid=false;
    } 
    if (!validate_password(mapdata.get("password"),mapdata.get("confirmation_password"))){
        is_data_valid=false;
    }
    //alert("llegue aqui y no me detuve3");
    return is_data_valid;
}
function validate_username(username){
    let usernamenew=username.trim(); 
    const usernameRegex = new RegExp(/^(?=.*[a-zA-Z])(?!.*[#$<>])[a-zA-Z0-9_]{4,16}$/); 
    if(usernamenew===""){ 
        let objectDOM=document.getElementsByName('username'); 
        queue_messages.enqueue("Username is required");
        queue_divs.enqueue(objectDOM);
        return false;   
    }     
    else if(!usernameRegex.test(usernamenew)){
        let objectDOM=document.getElementsByName('username'); 
        queue_messages.enqueue("Username is invalid");
        queue_divs.enqueue(objectDOM);  
        return false;        
          
    }
  return true;       
}
function validate_first_name(name){
    let namenew=name.trim();
    const first_nameRegex = new RegExp(/^[a-zA-Z]{4,16}$/); 
    if(namenew===""){ 
        let objectDOM=document.getElementsByName('first_name'); 
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("First name is required"); 
        return false;
    }
    else if(namenew.length===1){ 
        let objectDOM=document.getElementsByName('first_name');          
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("First name is too short"); 
        return false;
    }   
    else if(!first_nameRegex.test(namenew)){
        let objectDOM=document.getElementsByName('first_name'); 
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("First name is invalid"); 
        return false;        
    }
    return true; 
}

function validate_last_name(name){
    let namenew=name.trim();
    const last_nameRegex = new RegExp(/^[a-zA-Z]{4,16}$/); 
    if(namenew===""){ 
        let objectDOM=document.getElementsByName('last_name'); 
        queue_divs.enqueue(objectDOM ); 
        queue_messages.enqueue("Last name is required");
        return false;
    }
    else if(namenew.length===1){ 
        let objectDOM=document.getElementsByName('last_name'); 
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("Last name is too short"); 
        return false; 
    }              
    else if(!last_nameRegex.test(namenew)){
        let objectDOM=document.getElementsByName('last_name');
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("Last name is invalid"); 
        return false;        
          
    }
    return true; 
}
function validate_email(email){
    let emailnew=email.trim(); 
    // Regular expression to reinforce correct email handling with greater precision for incorrect cases
    const emailRegex = new RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
    if(emailnew===""){ 
        let objectDOM=document.getElementsByName('email');
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("Email is required"); 
        return false;
    }
    else if (!emailRegex.test(email)){
        let objectDOM=document.getElementsByName('email'); 
        queue_divs.enqueue(objectDOM ); 
        queue_messages.enqueue("Email is invalid");
        return false;
    }
    return true;
}
function validate_phone(phone) {
    console.log(phone);
    if(!phone){
        // enqueue only once per message
        const key = 'phone:Phone number is required';
        if (!errorSet.has(key)){
            errorSet.add(key);
            let objectDOM=document.getElementsByName('phone'); 
            queue_divs.enqueue(objectDOM ); 
            queue_messages.enqueue("Phone number is required"); 
        }
        return false;
    }
    let phonenew = phone.trim();
    // Accept leading + and 7-15 digits (E.164-ish)
    const phoneRegex = new RegExp(/^\+?[0-9]{7,15}$/);

    if (phonenew === "") {
        const key = 'phone:Phone number is required';
        if (!errorSet.has(key)){
            errorSet.add(key);
            let objectDOM=document.getElementsByName('phone'); 
            queue_divs.enqueue(objectDOM ); 
            queue_messages.enqueue("Phone number is required"); 
        }
        return false;
    }
    // Regular expression that validates the phone number format
    else if (!phoneRegex.test(phonenew)) {
        const key = 'phone:Phone number is invalid';
        if (!errorSet.has(key)){
            errorSet.add(key);
            let objectDOM=document.getElementsByName('phone'); 
            queue_divs.enqueue(objectDOM  ); 
            queue_messages.enqueue("Phone number is invalid"); 
        }
        return false;
    }
    return true;
}
function validate_password(password_A,password_B){
    if (password_A!==password_B){ 
        let objectDOM=document.getElementsByName('confirmation_password'); 
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("Passwords do not match");  
        return false;
    }
    return true;
}
function validate_password_timenow(password){
    if (validate_space(password)){
        let objectDOM=document.getElementsByName('password'); 
        queue_divs.enqueue(objectDOM); 
        queue_messages.enqueue("Password should not contain spaces");  
        return false;
    }
    if (password.length<8){
        let objectDOM=document.getElementsByName('password'); 
        queue_divs.enqueue(objectDOM ); 
        queue_messages.enqueue("Password is too short"); 
        return false;
    }
    // Regular expression that validates the password format
    const password_good=new RegExp(/^(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).+$/);
    if (!password_good.test(password)){
        let objectDOM=document.getElementsByName('password'); 
        queue_divs.enqueue(objectDOM ); 
        queue_messages.enqueue("Password must contain at least one uppercase letter and one special character"); 
        return false;
    }
    return true;
}
function validate_space(str){
    if(str.includes(' ')){
        return true;
    }
    return false;
}
// Attach behaviors after DOM is ready; bind to the form submit event (no inline JS required)
document.addEventListener('DOMContentLoaded', function(){
    const form = document.getElementById('registerForm');
    if(!form) return; // nothing to do
    form.addEventListener('submit', function(event){
        event.preventDefault();
        // clear previous inline error messages
        document.querySelectorAll('.error-message-inline').forEach(e=>e.remove());

        const is_form_valid = validate_data();
    
        if (!is_form_valid) { 
            let div_element=null;
            let message=null; 
            let div_name=null; 
            while (!queue_divs.isEmpty() && !queue_messages.isEmpty()) { 
                div_name = queue_divs.dequeue();
                message = queue_messages.dequeue();
                // div_name is a NodeList from getElementsByName; pick first element
                const target = (div_name && div_name[0]) ? div_name[0] : null;
                if (target) {
                    div_element = document.createElement('div');
                    div_element.className = 'error-message-inline';
                    div_element.innerHTML = '<span class="error-text">' + message + '</span>';
                    target.insertAdjacentElement('afterend', div_element);
                }
            }
            return; // stop submission
        }
    else { 
        // Prepare payload
        var url = "/yogui/register/"; // ajustar según el endpoint real
        var data = { username: mapinput.get("username"),
            first_name: mapinput.get("first_name"),
            last_name: mapinput.get("last_name"),
            email: mapinput.get("email") ,
            phone: mapinput.get("phone") ,
            password: mapinput.get("password"),
            confirmation_password: mapinput.get("confirmation_password")  };

        // Include CSRF header only if token input exists (keeps compatibility with SessionAuth)
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        const headers = { 'Content-Type': 'application/json' };
        if (csrfInput) headers['X-CSRFToken'] = csrfInput.value;

        fetch(url, {
            // do not include credentials by default; if your backend requires cookies enable it
            // credentials: 'include',
            method: 'POST',
            body: JSON.stringify(data),
            headers: headers
        })
        .then(response => {
            if (!response.ok) {
                throw response; // Lanza el objeto Response para manejar errores específicos
           } 
           return response.json(); 
          // Manejamos la respuesta de la petición aqui
        })
        .then( data=> {
            if (!('error' in data)) {
                const div_element = document.createElement('div'); 
                div_element.className = 'success-message';
                div_element.innerHTML = '<p>Usuario yogui creado exitosamente</p>';
                form.insertAdjacentElement('beforebegin', div_element); 
            }
            else { 
                throw data;   // Rechaza la promesa con los datos de error  
           }
            // Aquí puedes manejar los datos recibidos
      })
      .catch(error => {
        if (error instanceof Response) {
            // Leer el body sólo una vez
            error.json().then(errData => {
                try {
                    if (error.status === 400) {
                        // mostrar errores inline por campo
                        for (const k in errData) {
                            const input = document.querySelector('[name="' + k + '"]') || document.getElementById(k);
                            if (input) {
                                const el = document.createElement('div');
                                el.className = 'error-message-inline';
                                el.innerHTML = '<span class="error-text">' + (Array.isArray(errData[k]) ? errData[k].join(', ') : String(errData[k])) + '</span>';
                                input.insertAdjacentElement('afterend', el);
                            }
                        }
                        console.log('Validation errors:', errData);
                        return;
                    }

                    if (error.status === 500) {
                        console.log('Error 500:', errData);
                        const div_element = document.createElement('div');
                        div_element.className = 'server-error';
                        div_element.innerHTML = '<p>Error del servidor: ' + (errData.error || JSON.stringify(errData)) + '</p>';
                        form.insertAdjacentElement('beforebegin', div_element);
                        return;
                    }

                    // Otros códigos de error
                    console.log('Error inesperado:', errData);
                    const div_element = document.createElement('div');
                    div_element.className = 'unexpected-error';
                    div_element.innerHTML = '<p>Error inesperado</p>';
                    form.insertAdjacentElement('beforebegin', div_element);
                } catch (e) {
                    console.log('Error manejando la respuesta de error:', e);
                }
            }).catch(e => {
                console.log('No se pudo parsear JSON de la respuesta de error:', e);
            });
        } else {
            console.log('Error inesperado:', error);
            const div_element = document.createElement('div');
            div_element.className = 'unexpected-error';
            div_element.innerHTML = '<p>Error inesperado: ' + (error && error.statusText ? error.statusText : String(error)) + '</p>';
            form.insertAdjacentElement('beforebegin', div_element);
            console.error('Error inesperado:', error);
        }
    })
    }

  
});
});
