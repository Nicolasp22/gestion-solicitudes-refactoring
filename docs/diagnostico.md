# Diagnóstico del código inicial

Código analizado: `src/main.py` (216 líneas, tag `estado-inicial`).
Las líneas citadas son las de ese archivo en ese commit.

## Calidad externa (lo que ve el usuario)

| Atributo | Estado | Cómo se comprobó |
|---|---|---|
| Correctitud | Cumple los casos del menú | 24 pruebas de comportamiento (`tests/test_comportamiento.py`) |
| Usabilidad | Menú simple, mensajes claros | Prueba manual de los 5 flujos |
| Robustez | Regular: si falta `datos.json` informa y sigue con datos vacios | Pruebas de archivo inexistente y corrupto |
| Rendimiento | Sin problemas para el volumen del prototipo | No se midió, el volumen es chico |

El programa funciona. El problema no está en lo que hace sino en cómo está escrito.

## Calidad interna (lo que ve quien mantiene el código)

| Atributo | Estado | Motivo |
|---|---|---|
| Mantenibilidad | Mala | Una sola clase hace todo y hay código repetido |
| Testabilidad | Mala | Los métodos leen con `input` y escriben con `print`; no se pueden probar sin simular el teclado |
| Legibilidad | Regular | Nombres de una letra (`s`, `x`, `e`, `r`), líneas de más de 150 caracteres |
| Extensibilidad | Mala | Agregar un estado o un filtro obliga a tocar varios `if/elif` |

## Code smells detectados

### 1. Clase Dios

- Ubicación: GestorSolicitudes (líneas 8-185)
- Evidencia: Una clase de 178 líneas con 6 responsabilidades: datos, reglas, archivo JSON, teclado, pantalla y reporte
- Impacto: Todo cambio toca la misma clase y no se puede probar por partes
- Riesgo de mantenimiento: Alto: un cambio de pantalla puede romper una regla
- Prioridad de corrección: Alta
- Refactoring previsto: Extract Class (repositorio, servicio, consola)

### 2. Métodos largos y complejos

- Ubicación: registrar_solicitud (39-63), cambiar_estado (65-96), asignar_responsable (98-125), buscar_solicitudes (127-154), reporte (156-185)
- Evidencia: Entre 25 y 32 líneas cada uno; flake8 C901 con complejidad de 8 a 12
- Impacto: Difíciles de leer y de modificar sin error
- Riesgo de mantenimiento: Alto: cada cambio obliga a releer todo el método
- Prioridad de corrección: Alta
- Refactoring previsto: Extract Method

### 3. Strings mágicos

- Ubicación: Todo el archivo (24 literales de estado, tipo y prioridad)
- Evidencia: "PENDIENTE" aparece 4 veces, "RECHAZADA" 4 y "MEDIA" 3, escritos a mano
- Impacto: Un error de tipeo no da ningún aviso y rompe la regla en silencio
- Riesgo de mantenimiento: Medio: crece con cada estado o tipo nuevo
- Prioridad de corrección: Media
- Refactoring previsto: Replace Magic String with Constant

### 4. Código duplicado

- Ubicación: Búsqueda por id (66-78 y 99-111), búsquedas en listas (42-44, 73-75, 106-108, 117-119), filtros (130-147), línea de listado (154 y 185)
- Evidencia: Los mismos bloques copiados de 2 a 4 veces
- Impacto: Un cambio hay que hacerlo en varios lugares
- Riesgo de mantenimiento: Alto: es fácil corregir una copia y olvidar la otra
- Prioridad de corrección: Alta
- Refactoring previsto: Extract Method, tabla FILTROS, resumen()

### 5. Lista de parámetros larga

- Ubicación: crear_solicitud (línea 27)
- Evidencia: 7 parámetros; el estado inicial y el responsable vacío se pasan siempre igual
- Impacto: Es fácil confundir el orden al llamar
- Riesgo de mantenimiento: Medio
- Prioridad de corrección: Media
- Refactoring previsto: Introduce Parameter Object

### 6. Obsesión por primitivos

- Ubicación: Solicitud, estudiante y responsable como diccionarios (todo el archivo)
- Evidencia: Claves como strings sueltos: s["estado"], x["legajo"]
- Impacto: Sin validación y sin lugar donde poner el comportamiento
- Riesgo de mantenimiento: Medio: una clave mal escrita falla recién al ejecutar
- Prioridad de corrección: Media
- Refactoring previsto: Replace Record with Class

### 7. Envidia de funcionalidad

- Ubicación: cambiar_estado (80-94) y asignar_responsable (112-114)
- Evidencia: La gestión decide reglas que son propias de la solicitud (si está cerrada, si puede cambiar de estado)
- Impacto: La regla queda lejos del dato que gobierna
- Riesgo de mantenimiento: Medio
- Prioridad de corrección: Media
- Refactoring previsto: Move Method

### 8. Condicional largo

- Ubicación: cambiar_estado (80-94)
- Evidencia: if/elif por estado con ramas casi iguales
- Impacto: Agregar un estado obliga a editar el if
- Riesgo de mantenimiento: Medio: no cumple el principio abierto/cerrado
- Prioridad de corrección: Media
- Refactoring previsto: Tabla de transiciones (OCP)

### 9. Manejo de errores deficiente

- Ubicación: except sin tipo (19, 69, 102); == None (172)
- Evidencia: El except pelado atrapa cualquier error, hasta uno de programación; los errores se informan con print y return
- Impacto: Un fallo real queda oculto detrás de un mensaje genérico
- Riesgo de mantenimiento: Alto
- Prioridad de corrección: Alta
- Refactoring previsto: Excepciones propias y except específico

### 10. Nombres poco claros

- Ubicación: s, x, e, r, g, op, res, pend, proc, rech, sin
- Evidencia: Nombres de una letra o abreviados en todo el archivo
- Impacto: Hay que leer todo el código para entender cada variable
- Riesgo de mantenimiento: Bajo a medio
- Prioridad de corrección: Baja
- Refactoring previsto: Rename

## Resultado de flake8

Ver `docs/evidencias/flake8-antes.txt`. En el código inicial hay 17 avisos:
3 de `except` sin tipo (E722), 1 comparación con `None` (E711),
7 líneas largas (E501) y 6 funciones con complejidad mayor a 7 (C901).
Comando: `python -m flake8 src --max-complexity=7`.

## Orden de trabajo

Primero pruebas de comportamiento (commit 3), después los refactorings de a uno,
corriendo las pruebas después de cada uno.
