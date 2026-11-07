# Refactorings aplicados

Después de cada paso se corrieron las 24 pruebas de comportamiento y pasaron.
Ninguno cambia lo que ve el usuario: mismos mensajes, mismo orden de preguntas
y mismo formato del archivo JSON.

| # | Commit | Refactoring | Smell que ataca | Qué cambió |
|---|---|---|---|---|
| R1 | 5 | Extract Method | Métodos largos y duplicados | Se separaron `buscar_*`, `leer_*` e impresión de la línea de solicitud |
| R2 | 6 | Replace Magic String with Constant | Strings mágicos | Clases `Estado`, `Tipo`, `Prioridad` con sus listas y `validar` |
| R3 | 7 | Introduce Parameter Object | Lista de parámetros larga | `crear_solicitud` de 7 parámetros pasa a recibir `NuevaSolicitud` |
| R4 | 8 | Replace Record with Class + Move Method | Primitivos, envidia de funcionalidad | Clases `Estudiante`, `Responsable`, `Solicitud`; las reglas de estado pasan a `Solicitud` |
| R5 | 9 | Extract Class | Clase Dios, persistencia mezclada | `RepositorioJSON` (carga y guarda) y `ErrorDeDatos` |
| R6 | 10 | Extract Class | Clase Dios, E/S mezclada con reglas | `ServicioSolicitudes` (reglas) y `Consola` (teclado y pantalla); `main.py` solo arma las piezas |

## Detalle

### R1 Extract Method
Antes, la busqueda de una solicitud por id estaba copiada en dos métodos.
Después hay un único `buscar_solicitud`.

### R2 Constantes
`"PENDIENTE"` aparecia escrito a mano en muchos lugares. Ahora existe
`Estado.PENDIENTE` y las listas `Estado.TODOS`, `Estado.DESTINOS`, `Estado.CERRADOS`.

### R3 Parameter Object
`NuevaSolicitud(legajo, tipo, descripcion, prioridad)` agrupa los datos de entrada.
El estado inicial y el responsable vacio ya no se pasan: son siempre iguales al crear.

### R4 Clases del dominio y Move Method
`Solicitud.cambiar_estado` decide si la transición es válida usando la tabla
`Estado.TRANSICIONES`. Para agregar un estado se edita la tabla, no el código.

### R5 Repositorio
Es el único lugar que conoce el formato JSON. Si se cambiara por otra fuente
de datos, el resto no se toca.

### R6 Capas
- `consola.py`: lee del teclado, imprime y atrapa `ErrorDeNegocio`.
- `servicio.py`: reglas, sin `input` ni `print`.
- `modelos.py`: datos y reglas propias de cada objeto.
- `repositorio.py`: persistencia.

## Decisiones que se mantienen a proposito
- La consola válida campo por campo antes de llamar al servicio. Esto hace que el
  orden de las preguntas sea el mismo que en la versión inicial; el servicio
  vuelve a validar. Es una repeticion consciente (ver revisión de código).
