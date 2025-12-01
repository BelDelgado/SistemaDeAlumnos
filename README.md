# Sistema de Gestión de Alumnos

Sistema web desarrollado en Django para la administración y gestión de alumnos, con funcionalidades de autenticación, dashboard interactivo, generación de reportes PDF y web scraping automatizado.

## 🚀 Características

- **Autenticación de Usuarios**: Sistema de login seguro con Django Authentication
- **Dashboard de Alumnos**: Interfaz completa para gestionar información de estudiantes
- **Base de Datos**: Almacenamiento y gestión de datos de alumnos con PostgreSQL
- **Generación de PDF**: Creación automática de reportes y documentos en formato PDF
- **Web Scraping**: Búsqueda automatizada por palabra clave con envío de resultados por correo electrónico

## 📋 Requisitos Previos

- Python 3.8 o superior
- PostgreSQL
- Git
- pip (gestor de paquetes de Python)

## 🔧 Instalación Local

### 1. Clonar el repositorio

```bash
git clone  https://github.com/BelDelgado/SistemaDeAlumnos.git
cd tu-repositorio
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Mac/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432

# Configuración de correo
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
EMAIL_USE_TLS=True
```

### 5. Configurar la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Accede a `http://127.0.0.1:8000/` en tu navegador.

## 🌐 Deploy en Render

### Preparación

Asegúrate de tener los siguientes archivos en tu repositorio:

- `requirements.txt`
- `build.sh` (script de construcción)
- `.gitignore` (excluir archivos sensibles)

### Pasos para el deploy

1. **Crear cuenta en Render**: [render.com](https://render.com)

2. **Crear PostgreSQL Database**:
   - Dashboard → New + → PostgreSQL
   - Configura nombre y región
   - Copia las credenciales

3. **Crear Web Service**:
   - Dashboard → New + → Web Service
   - Conecta tu repositorio de GitHub
   - Configura:
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn nombre_proyecto.wsgi:application`

4. **Configurar Variables de Entorno**:
   ```
   DEBUG=False
   SECRET_KEY=clave-secreta-produccion
   ALLOWED_HOSTS=tu-app.onrender.com
   DB_NAME=valor-de-render
   DB_USER=valor-de-render
   DB_PASSWORD=valor-de-render
   DB_HOST=valor-de-render
   DB_PORT=5432
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=tu-email@gmail.com
   EMAIL_HOST_PASSWORD=tu-contraseña
   EMAIL_USE_TLS=True
   ```

5. **Deploy**: Render construirá y desplegará automáticamente

## 📦 Estructura del Proyecto

```
proyecto/
│
├── nombre_proyecto/          # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── alumnos/                  # App principal
│   ├── models.py            # Modelos de base de datos
│   ├── views.py             # Lógica de vistas
│   ├── urls.py              # Rutas
│   ├── forms.py             # Formularios
│   └── templates/           # Templates HTML
│
├── static/                   # Archivos estáticos
├── media/                    # Archivos subidos
├── requirements.txt          # Dependencias
├── build.sh                  # Script de build
├── .env                      # Variables de entorno (no subir a Git)
└── manage.py
```

## 🔐 Seguridad

- Las contraseñas se almacenan hasheadas con Django
- Protección CSRF habilitada
- Variables sensibles en archivo `.env`
- Validación de datos de entrada

## 📧 Configuración de Correo

Para usar la función de envío de correos con Gmail:

1. Activa la verificación en 2 pasos en tu cuenta de Google
2. Genera una contraseña de aplicación
3. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.x
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **PDF**: ReportLab / WeasyPrint
- **Web Scraping**: BeautifulSoup4 / Scrapy
- **Servidor**: Gunicorn
- **Deploy**: Render

## 📝 Uso

### Login

1. Accede a `/login/`
2. Ingresa tus credenciales
3. Serás redirigido al dashboard

### Gestión de Alumnos

- **Ver alumnos**: Lista completa en el dashboard
- **Agregar**: Botón "Nuevo Alumno"
- **Editar**: Click en el alumno deseado
- **Eliminar**: Opción en el detalle del alumno

### Generar PDF

- Selecciona uno o varios alumnos
- Click en "Generar Reporte PDF"
- El archivo se descargará automáticamente

### Web Scraping

1. Accede a la sección de scraping
2. Ingresa una palabra clave
3. Configura el correo destino
4. Click en "Buscar y Enviar"
5. Recibirás los resultados por email

## 🐛 Solución de Problemas

**Error de conexión a la base de datos**:
- Verifica las credenciales en `.env`
- Asegúrate de que PostgreSQL esté corriendo

**Archivos estáticos no se cargan**:
```bash
python manage.py collectstatic
```

**Error al enviar correos**:
- Verifica la configuración de EMAIL en settings.py
- Revisa que uses una contraseña de aplicación de Gmail

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

Tu Nombre - Belén Gisele Delgado

Proyecto: https://github.com/BelDelgado/

## 📞 Soporte

Si tienes alguna pregunta o problema, abre un [issue] https://github.com/BelDelgado/SistemaDeAlumnos/issues en GitHub.

---

⭐️ Si este proyecto te fue útil, considera darle una estrella en GitHub