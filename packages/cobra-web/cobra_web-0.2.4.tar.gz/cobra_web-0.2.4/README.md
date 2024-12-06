# Cobra Web

**Cobra Web** es una librería en Python que facilita la automatización en el desarrollo de sitios web con Django. Incluye herramientas para la generación de proyectos, configuración de estilos CSS, documentación automática con Sphinx, y soporte para APIs REST con Django REST Framework.

---

## 🚀 **Características**
- Creación de proyectos Django con configuración básica.
- Generación automática de documentación técnica usando Sphinx.
- Gestión de temas CSS con personalización a través de SCSS.
- Configuración rápida de Django REST Framework.
- Automatización para crear superusuarios en proyectos Django.

---

## 📦 **Instalación**
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/cobra_web.git
   cd cobra_web
   ````

2. Crea un entorno virtual e instala las dependencias:
````bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

## 🛠️ Uso del CLI

El archivo ```main.py``` actúa como CLI principal para interactuar con la librería. A continuación, se detallan los comandos disponibles.

### 1. Crear un Proyecto Django
Genera un proyecto Django con configuración básica.
````bash
python main.py crear_proyecto [nombre]
````
- **Ejemplo**:
````bash
python main.py crear_proyecto mi_sitio
````
- Si no se proporciona un nombre, se usará ```proyecto_defecto.```

### 2. Configurar Sphinx

Crea el directorio ```docs/``` y configura Sphinx en el proyecto.
````bash
python main.py configurar_sphinx [ruta_proyecto]
````
- **Ejemplo**:
````bash
python main.py configurar_sphinx mi_sitio
````

###  3. Generar Documentación

Genera documentación en formato HTML usando Sphinx.
````bash
python main.py generar_documentacion [ruta_proyecto]
````
- **Ejemplo**:
````bash
python main.py generar_documentacion mi_sitio
````

### 4. Listar Temas CSS Disponibles

Muestra una lista de temas CSS predefinidos.
````bash
python main.py listar_temas
````

### 5. Aplicar un Tema CSS

Copia un tema CSS predefinido al proyecto.
````bash
python main.py aplicar_tema [ruta_proyecto] [nombre_tema]
````
- **Ejemplo**:
````bash
python main.py aplicar_tema mi_sitio bootstrap
````

### 6. Crear un Superusuario

Automatiza la creación de un superusuario en un proyecto Django.
````bash
python main.py crear_superusuario [ruta_proyecto]
````
- **Ejemplo**:
````bash
python main.py crear_superusuario mi_sitio
````

### 7. Configurar Django REST Framework

Instala y configura Django REST Framework en un proyecto.
````bash
python main.py configurar_rest [ruta_proyecto]
````
- **Ejemplo**:
````bash
python main.py configurar_rest mi_sitio
````

## 🔧 Contribuir
¿Tienes ideas para mejorar este proyecto? ¡Eres bienvenido/a a contribuir! Sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad:
````bash
git checkout -b mi-nueva-funcionalidad
````
3. Haz tus cambios y crea un commit:
````bash
git commit -m "Descripción clara del cambio"
````
4. Sube tu rama al repositorio:
````bash
git push origin mi-nueva-funcionalidad
````
5. Crea un pull request.

## 📜 Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## 📫 Contacto
Si tienes dudas o necesitas soporte, no dudes en contactar:

- **Autor**: Adolfo González Hernández. 
- **Email**: adolfogonzal@gmail.com
- **Repositorio**: Cobra Web






