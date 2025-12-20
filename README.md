# FastAPI Project

Este repositorio contiene una aplicación backend construida con **FastAPI**, utilizando **PostgreSQL** como base de datos y **Alembic** para manejo de migraciones. A continuación encontrarás una guía completa para instalar, configurar y ejecutar el proyecto en tu entorno local.

---

## 🚀 Requisitos Previos
Asegúrate de tener instalado lo siguiente en tu máquina:

- **Python 3.10+**
- **PostgreSQL**
- **Git**
- (Opcional) **Rust** – requerido solo si no deseas modificar versiones de ciertos paquetes

---

## 📦 Instalación y Configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/mauritalkie/Personal_Finance_App_Backend.git
cd Personal_Finance_App_Backend
```

### 2️⃣ Crear base de datos en PostgreSQL
Crea una base de datos con el nombre que prefieras.

Este nombre deberá coincidir con tu **connection string** dentro del archivo `.env`.

---

### 3️⃣ Crear y activar un entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# (Opcional) Linux/MacOS\ source venv/bin/activate
```

---

### 4️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

#### ⚠️ Nota importante
Durante la instalación podrían ocurrir errores debido al compilado de algunos wheels.

Para solucionarlo puedes optar por:
- **Opción A:** Instalar Rust para permitir la recompilación de paquetes.
- **Opción B:** Eliminar manualmente las versiones especificadas de los paquetes conflictivos en `requirements.txt` para instalar las versiones más recientes que ya incluyen wheel precompilado.

---

### 5️⃣ Configurar variables de entorno
Crea un archivo `.env` basado en `.env.example` que se incluirá en el proyecto.

Solo es necesario sustituir tus credenciales.

#### Generar `secret_key`
```bash
openssl rand -hex 32
```
Si no funciona en CMD, puedes usar Git Bash.

---

### 6️⃣ Ejecutar migraciones con Alembic
```bash
alembic upgrade head
```
Esto aplicará todas las migraciones y dejará la base de datos lista.

---

### 7️⃣ Ejecutar el servidor de desarrollo
Cambia al directorio `app/`:
```bash
cd app
```

Ejecuta FastAPI en modo desarrollo:
```bash
fastapi dev main.py
```

---

## 🌐 Probar la API
Una vez iniciado, el servidor estará disponible en:
- http://127.0.0.1:8000

Para explorar los endpoints con Swagger UI visita:
- http://127.0.0.1:8000/docs

