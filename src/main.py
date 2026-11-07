# Sistema de gestion de solicitudes academicas
from datetime import date

from modelos import Estado, NuevaSolicitud, Prioridad, Solicitud, Tipo
from repositorio import ErrorDeDatos, RepositorioJSON

ARCHIVO = "datos.json"


class GestorSolicitudes:

    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.estudiantes = []
        self.responsables = []
        self.solicitudes = []
        self.cargar()

    def cargar(self):
        try:
            datos = self.repositorio.cargar()
        except ErrorDeDatos as error:
            print(error)
            return
        self.estudiantes, self.responsables, self.solicitudes = datos

    def guardar(self):
        self.repositorio.guardar(self.estudiantes, self.responsables,
                                 self.solicitudes)

    # --- busquedas y calculos ---

    def buscar_estudiante(self, legajo):
        for estudiante in self.estudiantes:
            if estudiante.legajo == legajo:
                return estudiante
        return None

    def buscar_solicitud(self, id_solicitud):
        for solicitud in self.solicitudes:
            if solicitud.id == id_solicitud:
                return solicitud
        return None

    def buscar_responsable(self, id_responsable):
        for responsable in self.responsables:
            if responsable.id == id_responsable:
                return responsable
        return None

    def siguiente_id(self):
        siguiente = 1
        for solicitud in self.solicitudes:
            if solicitud.id >= siguiente:
                siguiente = solicitud.id + 1
        return siguiente

    def contar_por_estado(self, estado):
        cantidad = 0
        for solicitud in self.solicitudes:
            if solicitud.estado == estado:
                cantidad = cantidad + 1
        return cantidad

    def contar_sin_responsable(self):
        cantidad = 0
        for solicitud in self.solicitudes:
            if solicitud.responsable is None:
                cantidad = cantidad + 1
        return cantidad

    def filtrar(self, campo, valor):
        return [solicitud for solicitud in self.solicitudes
                if getattr(solicitud, campo) == valor]

    # --- presentacion ---

    def mostrar_lista(self, solicitudes):
        if len(solicitudes) == 0:
            print("No hay solicitudes para ese filtro")
        for solicitud in solicitudes:
            print(solicitud.resumen())

    # --- lectura y validacion de datos ingresados ---

    def leer_id_solicitud(self):
        texto = input("Id de la solicitud: ")
        try:
            return int(texto)
        except ValueError:
            print("Id invalido")
            return None

    def leer_tipo(self):
        tipo = input("Tipo (" + "/".join(Tipo.TODOS) + "): ").upper()
        if tipo not in Tipo.TODOS:
            print("Tipo invalido")
            return None
        return tipo

    def leer_descripcion(self):
        descripcion = input("Descripcion: ")
        if len(descripcion.strip()) == 0:
            print("La descripcion es obligatoria")
            return None
        return descripcion

    def leer_prioridad(self):
        prioridad = input("Prioridad (" + "/".join(Prioridad.TODAS) + ") [" +
                          Prioridad.POR_DEFECTO + "]: ").upper()
        if prioridad == "":
            prioridad = Prioridad.POR_DEFECTO
        if prioridad not in Prioridad.TODAS:
            print("Prioridad invalida")
            return None
        return prioridad

    # --- operaciones del sistema ---

    def crear_solicitud(self, nueva):
        solicitud = Solicitud.desde_nueva(self.siguiente_id(), nueva,
                                          str(date.today()))
        self.solicitudes.append(solicitud)
        self.guardar()
        return solicitud.id

    def registrar_solicitud(self):
        legajo = input("Legajo del estudiante: ")
        if self.buscar_estudiante(legajo) is None:
            print("Estudiante no encontrado")
            return
        tipo = self.leer_tipo()
        if tipo is None:
            return
        descripcion = self.leer_descripcion()
        if descripcion is None:
            return
        prioridad = self.leer_prioridad()
        if prioridad is None:
            return
        nueva = NuevaSolicitud(legajo, tipo, descripcion, prioridad)
        nuevo_id = self.crear_solicitud(nueva)
        print("Solicitud registrada con id " + str(nuevo_id))

    def cambiar_estado(self):
        id_solicitud = self.leer_id_solicitud()
        if id_solicitud is None:
            return
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Solicitud no encontrada")
            return
        nuevo = input("Nuevo estado (" + "/".join(Estado.DESTINOS) + "): ").upper()
        if not solicitud.cambiar_estado(nuevo):
            print("Transicion no permitida")
            return
        self.guardar()
        print("Estado actualizado a " + nuevo)

    def asignar_responsable(self):
        id_solicitud = self.leer_id_solicitud()
        if id_solicitud is None:
            return
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Solicitud no encontrada")
            return
        if solicitud.esta_cerrada():
            print("La solicitud ya esta cerrada")
            return
        id_responsable = input("Id del responsable: ")
        responsable = self.buscar_responsable(id_responsable)
        if responsable is None:
            print("Responsable no encontrado")
            return
        solicitud.asignar_responsable(responsable.id)
        self.guardar()
        print("Responsable asignado: " + responsable.nombre)

    def buscar_solicitudes(self):
        print("Filtrar por: 1) estado  2) tipo  3) legajo")
        opcion = input("Opcion: ")
        if opcion == "1":
            resultados = self.filtrar("estado", input("Estado: ").upper())
        elif opcion == "2":
            resultados = self.filtrar("tipo", input("Tipo: ").upper())
        elif opcion == "3":
            resultados = self.filtrar("legajo", input("Legajo: "))
        else:
            print("Opcion invalida")
            return
        self.mostrar_lista(resultados)

    def reporte(self):
        print("=== REPORTE ===")
        print("Total de solicitudes: " + str(len(self.solicitudes)))
        for estado in Estado.TODOS:
            print(estado + ": " + str(self.contar_por_estado(estado)))
        print("Sin responsable asignado: " + str(self.contar_sin_responsable()))
        print("--- Pendientes por prioridad ---")
        for prioridad in Prioridad.TODAS:
            for solicitud in self.solicitudes:
                if solicitud.estado == Estado.PENDIENTE and solicitud.prioridad == prioridad:
                    print(solicitud.resumen())


def main():
    gestor = GestorSolicitudes(RepositorioJSON(ARCHIVO))
    while True:
        print("")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar solicitudes")
        print("5. Reporte")
        print("0. Salir")
        opcion = input("Opcion: ")
        if opcion == "1":
            gestor.registrar_solicitud()
        elif opcion == "2":
            gestor.cambiar_estado()
        elif opcion == "3":
            gestor.asignar_responsable()
        elif opcion == "4":
            gestor.buscar_solicitudes()
        elif opcion == "5":
            gestor.reporte()
        elif opcion == "0":
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
