import json

from modelos import Estudiante, Responsable, Solicitud


class ErrorDeDatos(Exception):
    # El archivo de datos no existe o tiene un formato que no se entiende
    pass


MENSAJE_ERROR = "No se pudo leer el archivo de datos"


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
            raise ErrorDeDatos(MENSAJE_ERROR) from error
        return estudiantes, responsables, solicitudes

    def guardar(self, estudiantes, responsables, solicitudes):
        datos = {
            "estudiantes": [estudiante.a_diccionario()
                            for estudiante in estudiantes],
            "responsables": [responsable.a_diccionario()
                             for responsable in responsables],
            "solicitudes": [solicitud.a_diccionario()
                            for solicitud in solicitudes],
        }
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
