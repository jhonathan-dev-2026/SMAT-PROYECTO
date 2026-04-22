# SMAT - Sistema de Monitoreo Ambiental Profesional (Arquitectura Modular)
**Autor:** Jhonathan Gomez
**Materia:** Desarrollo Basado en Plataformas (Laboratorio 4) - Backend

## Descripción del Proyecto
Este sistema representa la evolución final del ecosistema SMAT, refactorizado bajo una **arquitectura modular profesional**. Se ha implementado la **Separación de Responsabilidades** (Clean Code) y configurado políticas de seguridad **CORS** para permitir la interoperabilidad con clientes externos y aplicaciones móviles.

## Tecnologías Utilizadas
* **FastAPI:** Framework principal con integración de Middleware de seguridad.
* **SQLAlchemy:** Gestión de persistencia relacional con lógica de funciones agregadas.
* **SQLite:** Base de datos relacional para almacenamiento permanente (smat.db).
* **Pytest:** Suite de pruebas unitarias con cobertura del 100% (TDD).
* **Pydantic:** Validación estricta de esquemas y transferencia de datos.

## Estructura Profesional (Modularización)
El código se ha redistribuido en módulos especializados para garantizar la escalabilidad:
* **app/main.py:** Punto de entrada y configuración de Middleware CORS.
* **app/models.py:** Representación de tablas SQL (Estaciones y Lecturas).
* **app/schemas.py:** Definición de estructuras de datos y validaciones.
* **app/crud.py:** Lógica pura de persistencia y manipulación de datos.
* **app/database.py:** Configuración del motor y sesiones de base de datos.

## Cómo Ejecutar el Proyecto
1. **Activar el entorno virtual:**
   `source venv/bin/activate` (Linux) o `.\venv\Scripts\activate` (Windows)
2. **Instalar dependencias:**
   `pip install -r requirements.txt`
3. **Iniciar el servidor (Modo Profesional):**
   `uvicorn app.main:app --reload`
4. **Acceder a la documentación (Swagger UI):**
   `http://127.0.0.1:8000/docs`

## Pruebas de Calidad y Reto Final (TDD)
Se han implementado pruebas automáticas y endpoints de auditoría que cubren:
* **Seguridad:** Verificación de cabeceras CORS para acceso externo.
* **Dashboard de Auditoría:** Endpoint `/estaciones/stats` que calcula el total de estaciones, lecturas y el **Punto Crítico Máximo** del sistema.
* **Análisis de Riesgo:** Clasificación de niveles basada en telemetría en tiempo real.
* **Integridad:** Validación de relaciones 1:N entre estaciones y lecturas.

## Evidencia de Persistencia (Comandos cURL)
Para validar la persistencia real exigida en la evaluación, puede utilizar los siguientes comandos:

```bash
# Crear Estación
curl -X POST "[http://127.0.0.1:8000/estaciones/](http://127.0.0.1:8000/estaciones/)" -H "Content-Type: application/json" -d '{"id": 1, "nombre": "Misti-Alpha", "ubicacion": "Arequipa"}'

# Registrar Lectura
curl -X POST "[http://127.0.0.1:8000/lecturas/](http://127.0.0.1:8000/lecturas/)" -H "Content-Type: application/json" -d '{"estacion_id": 1, "valor": 35.8}'

# Consultar Estadísticas de Auditoría
curl -X GET "[http://127.0.0.1:8000/estaciones/stats](http://127.0.0.1:8000/estaciones/stats)"