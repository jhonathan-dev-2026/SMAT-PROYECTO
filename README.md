# SMAT - Sistema de Monitoreo Ambiental Profesional
**Autor:** Jhonathan Gomez
**Materia:** Desarrollo Basado en Plataformas (Laboratorio 3) - Backend

## Descripción del Proyecto
Este sistema es una evolución del monitor ambiental SMAT, migrado de almacenamiento en memoria a **persistencia real mediante una base de datos SQL**. Utiliza **SQLAlchemy** como ORM para gestionar la comunicación con una base de datos SQLite de forma eficiente y segura.

## Tecnologías Utilizadas
* **FastAPI:** Framework de alto rendimiento para la construcción de la API.
* **SQLAlchemy:** Mapeo objeto-relacional (ORM) para la persistencia.
* **SQLite:** Motor de base de datos relacional ligero.
* **Pytest:** Suite de pruebas para garantizar la integridad del sistema (TDD).
* **Pydantic:** Validación de esquemas de datos.

## Cómo Ejecutar el Proyecto
1. **Activar el entorno virtual:**
   `.\venv\Scripts\activate`
2. **Instalar dependencias:**
   `pip install -r requirements.txt`
3. **Iniciar el servidor:**
   `uvicorn main:app --reload`
4. **Acceder a la documentación (Swagger):**
   `http://127.0.0.1:8000/docs`

## Pruebas Realizadas (TDD)
Se han implementado pruebas automáticas que cubren:
* Creación de estaciones ambientales.
* Prevención de duplicados de ID.
* Cálculo exacto de promedios históricos.
* Clasificación de niveles de riesgo (NORMAL, ALERTA, PELIGRO).