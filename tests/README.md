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

## Estructura

```
src/            codigo (main, consola, servicio, modelos, repositorio)
tests/          pruebas de comportamiento y unitarias
datos/          datos de ejemplo (sinteticos)
docs/           diagnostico, refactorings, pruebas, revision y decisiones
```

## Pruebas y calidad

```
python -m unittest discover -s tests
python -m flake8 src tests --max-complexity=7     # opcional, requiere flake8
```

## Historia del trabajo

Tags para recorrer el repositorio:

| Tag | Que muestra |
|---|---|
| `estado-inicial` | Codigo original con problemas de diseno |
| `etapa-diagnostico` | Diagnostico y code smells |
| `etapa-refactoring` | Refactorings aplicados |
| `etapa-pruebas` | Pruebas unitarias |
| `etapa-docs` | Revision y documentacion final |
| `estado-refactorizado` | Version final |

Documentacion: `docs/diagnostico.md`, `docs/refactorings.md`, `docs/pruebas.md`,
`docs/checklist-code-review.md`, `docs/decisiones-tecnicas.md`.

## Tecnologías

Python 3, biblioteca estándar (json, datetime, unittest). flake8 solo como apoyo de revisión.
