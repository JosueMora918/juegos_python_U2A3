Este proyecto cuenta con una infraestructura de pruebas unitarias y de integración utilizando `unittest` para garantizar la integridad del sistema de gestión de videojuegos.



1\. Cobertura de Pruebas

La suite de pruebas se divide en tres áreas críticas para asegurar el funcionamiento correcto de la arquitectura:



Modelos (`test\_models.py`): Verifica la persistencia de datos mediante el ORM (SQLAlchemy).

&#x20;   Valida la creación correcta de la entidad `Juego` y la integridad de sus campos (nombre, descripción, precio).

Rutas y Navegación (`test\_routes.py`):

&#x20;   Comprueba el sistema de seguridad y autenticación (`flask-login`).

&#x20;   Verifica que las rutas protegidas (como el index `/`) redireccionen correctamente al login cuando no hay una sesión activa.

API RESTful (`test\_api.py`):

&#x20;   Valida los endpoints de `flask-restful`.

&#x20;   Asegura que la respuesta del endpoint `/api/juegos` sea un código 200 OK y que el cuerpo de la respuesta sea un formato JSON válido (lista de objetos).







2\. Retos Encontrados y Soluciones



Retos

Aislamiento de Datos: Las pruebas podrían ensuciar la base de datos MySQL de producción.

Contexto de Aplicación: Errores al intentar acceder a la base de datos fuera de la instancia de Flask.

Dependencia de `app.py`: Al no usar una factoría de aplicaciones (`create\\\_app`), las configuraciones de prueba chocaban con las de ejecución.



Soluciones

Se configuró una base de datos SQLite en memoria (`sqlite:///:memory:`) exclusiva para el entorno de pruebas, garantizando que cada test inicie con una base limpia.

Se utilizó el método `app.app\_context()` y `ctx.push()` en el `setUp` de cada clase para mantener vivo el contexto de la aplicación durante la ejecución.

Se sobrescribió el diccionario `app.config` dinámicamente dentro del `setUp` de los tests para forzar el modo `TESTING = True`.







3\. Ejecución

Para ejecutar todas las pruebas y visualizar el reporte detallado:



python -m unittest discover -v tests

