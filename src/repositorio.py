import json

from modelos import Estudiante, Responsable, Solicitud


class ErrorDeDatos(Exception):
    pass


class RepositorioJSON:
    # Lee y escribe los datos del sistema en un archivo JSON

    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self):
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            estudiantes = [Estudiante.desde_diccionario(dato)
                           for dato in datos["estudiantes"]]
            responsables = [Responsable.desde_diccionario(dato)
                            for dato in datos["responsables"]]
            solicitudes = [Solicitud.desde_diccionario(dato)
                           for dato in datos["solicitudes"]]
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise ErrorDeDatos("No se pudo leer el archivo de datos") from error
        return estudiantes, responsables, solicitudes

    def guardar(self, estudiantes, responsables, solicitudes):
        datos = {
            "estudiantes": [e.a_diccionario() for e in estudiantes],
            "responsables": [r.a_diccionario() for r in responsables],
            "solicitudes": [s.a_diccionario() for s in solicitudes],
        }
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
