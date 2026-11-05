# Evidencias

En esta carpeta van las salidas reales de las herramientas y de las pruebas,
guardadas por el equipo al ejecutarlas sobre cada estado del código.

| Archivo | Se genera con | Sobre qué estado |
|---|---|---|
| `pruebas-antes.txt` | `python -m unittest discover -s tests -v` | tag `estado-inicial` |
| `flake8-antes.txt` | `python -m flake8 src --max-complexity=7` | tag `estado-inicial` |
| `pruebas-despues.txt` | `python -m unittest discover -s tests -v` | tag `estado-refactorizado` |
| `flake8-despues.txt` | `python -m flake8 src --max-complexity=7` | tag `estado-refactorizado` |

Las capturas de pantalla de la ejecución del programa se guardan acá también.
