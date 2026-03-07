

# 🚀 Sistema de Gestión de Shalas o Centros de Yoga

[![Licencia](https://img.shields.io/badge/Licencia-Open%20Source-blue.svg)](LICENSE)
[![Versión](https://img.shields.io/badge/Versión-1.0.0-green.svg)]()

> El proyecto consiste en desarrollar un sistema de gestión para centros o shalas de yoga, que permita a los administradores gestionar clientes (yoguis), clases, horarios, instructores, paquetes y pagos. Los clientes (yoguis) podrán registrarse, comprar paquetes, reservar clases y llevar control de su progreso mensual.

---

## 📑 Tabla de Contenidos

* [✨ Características](#-características)
* [🛠️ Requisitos Previos](#-requisitos-previos)
* [💻 Instalación](#-instalación)
* [🚀 Uso](#-uso)
* [🤝 Contribución](#-contribución)
* [📄 Licencia](#-licencia)
* [✉️ Contacto](#-contacto)

---

## ✨ Características

* **Registro y autenticación:** El sistema permite registrar usuarios y mantener la seguridad en el acceso de los recursos por rol.
* **Creación del centro:** El administrador del centro puede crear desde cero un centro con todas sus configuraciones.
* **Administración de componentes:** El sistema ofrece la gestión de crear, visualizar y editar los principales datos asociados al centro.
* **Compra de paquetes:** El sistema permite comprar paquetes siempre que el usuario no tenga una suscripción activa.
* **Factura de compra:** El usuario puede generar una factura después de que se procese su pago.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

* **Python 3.14+**
* **PostgreSQL**
* **Visual Studio Code** (u otro editor de tu preferencia)
* **Git**

---

## 💻 Instalación

Sigue estos pasos para configurar el entorno de desarrollo localmente:

### 1. Clonar el repositorio
Elige el método de tu preferencia:

**Vía SSH:**
```bash
git clone git@github.com:jessec01/proyecto-final.git

```

**Vía HTTPS:**

```bash
git clone [https://github.com/jessec01/proyecto-final.git](https://github.com/jessec01/proyecto-final.git)

```

### 2. Preparar la Base de Datos

Accede a tu terminal de PostgreSQL:

```bash
psql -U postgres

```

Ejecuta los siguientes comandos (ajusta el nombre y la contraseña según tu preferencia):

```sql
-- Crear un usuario
CREATE USER nombredeusuario WITH PASSWORD '1234';

-- Crear la base de datos y asignarla al usuario
CREATE DATABASE nombrebasededato OWNER nombredeusuario;

```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y añade tus credenciales:

```env
POSTGRES_DB=nombrebasededato
POSTGRES_USER=nombredeusuario
POSTGRES_PASSWORD=1234
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

```

> ⚠️ **IMPORTANTE:** Nunca subas el archivo `.env` a GitHub. Asegúrate de incluirlo en tu `.gitignore`.

### 4. Entorno Virtual y Dependencias

Crea y activa el entorno virtual según tu sistema operativo:

* **Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```


* **Windows:**
```cmd
# CMD
python -m venv venv
venv\Scripts\activate.bat

# PowerShell
.\venv\Scripts\Activate.ps1

```



Una vez activado, instala las librerías necesarias:

```bash
pip install -r requirements.txt

```

---

## 🚀 Uso

Para iniciar el sistema, ejecuta el comando principal:

```bash
python django manage.py runserver

```

---

## 🤝 Contribución

1. Haz un *Fork* del proyecto.
2. Crea una rama para tu mejora (`git checkout -b feature/MejoraIncreible`).
3. Haz *Commit* de tus cambios (`git commit -m 'Añade una mejora'`).
4. Sube tus cambios (`git push origin feature/MejoraIncreible`).
5. Abre un *Pull Request*.

---

## 📄 Licencia

Este proyecto es de código abierto y está bajo la licencia [MIT/Open Source]. Consulta el archivo `LICENSE` para más información.

---

## ✉️ Contacto

**Jessec01** * GitHub: [@jessec01](https://github.com/jessec01)

---

⭐️ *Si este proyecto te ha servido de ayuda, ¡no olvides darle una estrella!*

```

¿Te gustaría que generemos también el contenido de un archivo `.gitignore` básico para evitar que se suban las carpetas de Python y tu archivo `.env` por accidente?

```
