# Foro Manga

**Foro Manga** es una aplicación web desarrollada con Django que permite a los aficionados del manga interactuar, compartir opiniones y descubrir nuevos títulos. Además de las funcionalidades básicas de un foro, integra datos externos de la API Jikan (MyAnimeList) para enriquecer la experiencia.

## Funcionalidades principales

- **Autenticación de usuarios**: Registro, inicio/cierre de sesión y recuperación de contraseña.
- **Perfiles**: Avatar, biografía y configuración de privacidad.
- **Foro de discusión**:
  - Creación, edición y eliminación de hilos (temas).
  - Respuestas (posts) dentro de cada hilo.
  - Sistema de votos (upvotes) para valorar publicaciones.
  - Paginación y buscadores en listados de hilos y respuestas.
- **Gestión de contenidos**:
  - Administradores y autores pueden editar o eliminar hilos y respuestas.
- **Integración con Jikan API**:
  - Búsqueda de géneros de anime.
  - Listado de animes por género con portada, sinopsis y puntuación.
  - Paginación y buscador en los listados de géneros y animes.
- **API REST** (Django REST Framework):
  - Endpoints para CRUD de Manga y Posts.
  - Soporte para JSON y multipart/form-data (subida de imágenes).
  - Filtrado por género y paginación.

## Estructura del proyecto

```
foromanga/            # Proyecto Django
├── forum/            # App principal (foro, manga, integración Jikan)
│   ├── models.py     # Modelos: Thread, Post, Genre, Manga, Upvote
│   ├── services.py   # Wrapper de llamadas a Jikan API
│   ├── serializers.py# Serializers para la API REST
│   ├── views.py      # Vistas del foro y consumo de API
│   └── urls.py       # Rutas del foro y de la API interna
├── users/            # App de autenticación y perfiles
├── templates/        # Plantillas base, foro, usuarios, API browsable
└── manage.py         # Comandos de gestión
```

## Tecnologías utilizadas

- **Backend**: Django, Django REST Framework
- **Frontend**: Bootstrap 5, plantillas Django
- **API externa**: Jikan (MyAnimeList)
- **Base de datos**: Oracle Cloud / local (configurable)

## Cómo empezar

1. **Clonar** el repositorio.
2. Crear un **entorno virtual** e instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar** credenciales en `.env` o `settings.py` (base de datos, Jikan API URL).
4. Ejecutar **migraciones** y crear superusuario:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

¡Listo para disfrutar de Foro Manga!