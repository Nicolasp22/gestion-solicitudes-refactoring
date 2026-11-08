# Pruebas

Se usa solo `unittest` de la biblioteca estándar.

## Dos niveles

| Archivo | Tipo | Cantidad | Qué prueba |
|---|---|---|---|
| `tests/test_comportamiento.py` | Caja negra | 24 | Ejecuta `src/main.py` con un guion de teclado y revisa la salida y `datos.json`. Sirve igual para la versión inicial y la refactorizada |
| `tests/test_unitarias.py` | Unitarias | 27 | `Solicitud`, validaciones, `ServicioSolicitudes` y `RepositorioJSON` por separado |

Las de comportamiento se escribieron antes de refactorizar (commit 3) y son la red
de seguridad. Las unitarias solo se pudieron escribir después, porque el código
inicial no se podia probar por partes.

## Cómo se corre

    python -m unittest discover -s tests

Resultado actual: 51 pruebas, todas OK.

## Técnicas usadas en las unitarias
- Repositorio falso en memoria (`RepositorioEnMemoria`) que solo cuenta cuantas veces se guarda.
- Carpeta temporal para probar el repositorio real sin tocar `datos.json`.
- Se verifica también que ante un error no se modifica nada ni se guarda.

## Limitaciones
- La consola (`consola.py`) se prueba solo a traves de las pruebas de caja negra.
- No se mide cobertura.
