# Decisiones técnicas

## Estructura final

    src/main.py         arma las piezas y arranca
    src/consola.py      menu, teclado y pantalla
    src/servicio.py     reglas de negocio
    src/modelos.py      Estado, Tipo, Prioridad, Solicitud, Estudiante, Responsable
    src/repositorio.py  lectura y escritura del JSON
    tests/              pruebas de comportamiento y unitarias

La consola depende del servicio y el servicio del repositorio. Los modelos no dependen de nadie.

## Principios SOLID

| Principio | Cómo se aplica |
|---|---|
| SRP, una sola razón para cambiar | Cada archivo tiene un único motivo de cambio: formato de pantalla, reglas, datos o persistencia |
| OCP, abierto a extensión | Un estado nuevo se agrega en `Estado.TRANSICIONES`; un filtro nuevo en `FILTROS`; sin tocar la lógica |
| LSP, sustitucion | No aplica: no hay herencia en el proyecto. Las clases son independientes |
| ISP, interfaces chicas | No aplica en sentido estricto: no hay interfaces. El servicio solo exige que el repositorio tenga `guardar` |
| DIP, depender de abstracciones | El servicio recibe el repositorio por parámetro. Las pruebas le pasan uno falso en memoria |

## Clean Code
- Nombres que dicen que hacen (`puede_pasar_a`, `contar_sin_responsable`).
- Funciones cortas y sin efectos escondidos.
- Sin comentarios que repitan el código.
- Errores con excepciones propias en lugar de `print` y `return` en medio de la lógica.
- Sin código repetido.

## Lo que se dejo afuera a proposito
- Base de datos, interfaz gráfica y librerías externas: el trabajo pide refactoring, no más funcionalidad.
- Clases abstractas o herencia: no hacen falta y no mejorarian este código.
- Validaciones de unicidad de claves y manejo de error al guardar (ver revisión de código).
