# SMAT - Sistema de Monitoreo Ambiental con Seguridad Avanzada JWT

**Autor:** Jhonathan Gomez  
**Materia:** Desarrollo Basado en Plataformas - Backend

## Descripción del Proyecto
Evolución del ecosistema SMAT, implementando una arquitectura modular robusta y un sistema de seguridad basado en estándares de la industria. El proyecto integra autenticación mediante tokens de corta duración (JWT) y una capa de validación de integridad referencial cruzada para garantizar la consistencia de los datos ambientales almacenados.

## Tecnologías y Seguridad Implementada
* **FastAPI:** Framework de alto rendimiento con inyección de dependencias para seguridad.
* **OAuth2 & JWT:** Protocolo de autorización con JSON Web Tokens (algoritmo HS256) para la protección de endpoints de escritura.
* **Passlib & BCrypt:** Gestión de hashing y verificación de credenciales de seguridad.
* **SQLAlchemy ORM:** Mapeo objeto-relacional con validación de llaves foráneas.
* **Pytest:** Suite de pruebas automatizadas para validación de flujos protegidos y lógica de negocio.

## Estructura de la Solución (Modularización)
La arquitectura se basa en la separación de responsabilidades para facilitar el mantenimiento y la escalabilidad:
* **app/main.py:** Punto de entrada, configuración de Middleware CORS y rutas protegidas.
* **app/auth.py:** Lógica de generación de tokens, hashing de contraseñas y validación de identidad.
* **app/models.py:** Definición de entidades relacionales (Estaciones y Lecturas).
* **app/schemas.py:** Modelos Pydantic para validación de entrada/salida y gestión de tokens.
* **app/crud.py:** Operaciones de persistencia con lógica de validación de integridad.
* **app/database.py:** Configuración del motor SQLite y gestión de sesiones de base de datos.

## Instrucciones de Instalación y Despliegue
1. **Activación del entorno virtual:**
   `.\venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Linux/macOS)
2. **Instalación de dependencias críticas:**
   `pip install -r requirements.txt`
3. **Ejecución del servidor:**
   `uvicorn app.main:app --reload`
4. **Interfaz de Pruebas (Swagger UI):**
   `http://127.0.0.1:8000/docs`

## Validación de Integridad y Pruebas Unitarias
El sistema incluye un riguroso control de calidad mediante TDD (Test Driven Development):
* **Protección de Endpoints:** Los métodos POST requieren un `access_token` válido obtenido a través del endpoint `/token`.
* **Validación de Integridad:** El sistema impide el registro de lecturas vinculadas a estaciones inexistentes mediante un error **404 Not Found**, cumpliendo con los requisitos de integridad referencial en la capa de aplicación.
* **Ejecución de Pruebas Automáticas:**
   `pytest`

## Ejemplos de Interacción (API Client / cURL)

```bash
# 1. Obtención de Token de Acceso
curl -X POST "[http://127.0.0.1:8000/token](http://127.0.0.1:8000/token)"

# 2. Registro de Estación (Requiere Token)
curl -X POST "[http://127.0.0.1:8000/estaciones/](http://127.0.0.1:8000/estaciones/)" \
     -H "Authorization: Bearer <SU_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "nombre": "Misti-Alpha", "ubicacion": "Arequipa"}'

# 3. Registro de Lectura con Validación de ID (Requiere Token)
curl -X POST "[http://127.0.0.1:8000/lecturas/](http://127.0.0.1:8000/lecturas/)" \
     -H "Authorization: Bearer <SU_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"estacion_id": 1, "valor": 35.8}'