# Revisión de código (checklist)

Código revisado: estado luego de las pruebas unitarias (commit 11).
Herramienta de apoyo: `python -m flake8 src tests --max-complexity=7`.
Antes de esta revisión flake8 daba 2 avisos en `src` (E501). Después, 0.

## Checklist

| # | Punto | Resultado | Observación y acción |
|---|---|---|---|
| 1 | Nombres claros y consistentes | Corregido | Quedaban e, r, s en listas por comprensión de repositorio.guardar; ahora estudiante, responsable, solicitud |
| 2 | Funciones cortas, una responsabilidad | OK | La más larga tiene 13 líneas; complejidad menor a 7 |
| 3 | Sin código duplicado | Corregido | contar_por_estado y pendientes_por_prioridad repetían el filtro por estado; ahora usan filtrar |
| 4 | Sin strings ni números mágicos | Corregido | El mensaje de ErrorDeDatos pasó a la constante MENSAJE_ERROR |
| 5 | Largo de línea (PEP 8) | Corregido | Los 2 avisos E501 de repositorio.py y servicio.py |
| 6 | Manejo de errores sin except pelado | OK | Se capturan ErrorDeNegocio, ErrorDeDatos y tipos concretos |
| 7 | Comentarios solo donde explican | Corregido | Se agregó comentario a ErrorDeDatos; el resto se explica por los nombres |
| 8 | Separación de capas | OK | El servicio no usa input ni print; los modelos no conocen JSON |
| 9 | Pruebas que cubren las reglas | OK | 51 pruebas, con casos válidos e inválidos |
| 10 | Comportamiento externo sin cambios | OK | Las 24 pruebas de comportamiento pasan en todos los commits |
| 11 | Validación repetida entre consola y servicio | Aceptado | La consola valida primero para mantener el orden de preguntas; el servicio vuelve a validar. Repetición consciente |
| 12 | Solicitud.__init__ con 8 parámetros | Aceptado | Son los 8 campos del registro; agrupar más complicaría el prototipo sin ganancia |
| 13 | Error al escribir el archivo | Límite | Si guardar falla por permisos o disco lleno, el programa termina con error. El código inicial se comportaba igual |
| 14 | Ids y legajos únicos | Supuesto | Se asume que el archivo no repite claves; no se valida al cargar |

## Criterios de aceptación técnica

- flake8 con complejidad máxima 7 sin avisos en `src` y `tests`.
- Las 51 pruebas pasan.
- Ningún `except` sin tipo ni comparación con `None` usando `==`.
- Ninguna función de `src` con más de 15 líneas.
- El comportamiento externo coincide con el del estado inicial.

## Resumen

Cinco correcciones de forma (1, 3, 4, 5 y 7), dos decisiones aceptadas (11 y 12) y dos límites declarados (13 y 14). Ninguna cambia el comportamiento.
