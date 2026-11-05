# Gestión de Solicitudes Académicas - Refactoring

Trabajo Práctico Integrador de Metodología de Sistemas II (UTN, Tecnicatura
Universitaria en Programación a Distancia).

Integrantes: Matías Orellana y Nicolás Pagola.

## Descripción

Módulo simple, por consola, para gestionar solicitudes académicas de
estudiantes. Es un prototipo construido por el equipo para este trabajo. La
versión inicial (tag `estado-inicial`) está escrita como queda un código
hecho con apuro, con problemas de diseño que después se diagnostican y se
corrigen con refactorings seguros (tag `estado-refactorizado`).

## Funcionalidades

- Registrar una solicitud de un estudiante (tipo, descripción y prioridad).
- Cambiar el estado de una solicitud (PENDIENTE, EN_PROCESO, RESUELTA,
  RECHAZADA) respetando las transiciones permitidas.
- Asignar un responsable a una solicitud abierta.
- Buscar solicitudes por estado, tipo o legajo.
- Ver un reporte básico con cantidades por estado y pendientes por prioridad.

Los datos se guardan en un archivo JSON. Todos los datos de ejemplo son
sintéticos.

## Instalación y uso

Requiere Python 3.9 o superior. No usa librerías externas.

```
cp datos/datos_ejemplo.json datos.json      # en Windows: copy datos\datos_ejemplo.json datos.json
python src/main.py
```

El programa lee y escribe `datos.json` en la carpeta desde donde se ejecuta.

## Tecnologías

Python 3, biblioteca estándar (json, datetime, unittest).
