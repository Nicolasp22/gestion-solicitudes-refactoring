from modelos import (ErrorDeNegocio, Estado, NuevaSolicitud, Prioridad,
                     Tipo)

# Opciones del menu de busqueda: campo, pregunta y si se pasa a mayusculas
FILTROS = {
    "1": ("estado", "Estado: ", True),
    "2": ("tipo", "Tipo: ", True),
    "3": ("legajo", "Legajo: ", False),
}


class Consola:
    # Menu por consola. Pide datos, llama al servicio y muestra resultados.

    def __init__(self, servicio):
        self.servicio = servicio
        self.acciones = {
            "1": self.registrar_solicitud,
            "2": self.cambiar_estado,
            "3": self.asignar_responsable,
            "4": self.buscar_solicitudes,
            "5": self.reporte,
        }

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Opcion: ")
            if opcion == "0":
                break
            self.ejecutar_opcion(opcion)

    def mostrar_menu(self):
        print("")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar solicitudes")
        print("5. Reporte")
        print("0. Salir")

    def ejecutar_opcion(self, opcion):
        accion = self.acciones.get(opcion)
        if accion is None:
            print("Opcion invalida")
            return
        try:
            accion()
        except ErrorDeNegocio as error:
            print(error)

    # --- lectura de datos ---

    def leer_solicitud(self):
        texto = input("Id de la solicitud: ")
        try:
            id_solicitud = int(texto)
        except ValueError:
            raise ErrorDeNegocio("Id invalido")
        return self.servicio.buscar_solicitud(id_solicitud)

    def leer_prioridad(self):
        pregunta = ("Prioridad (" + "/".join(Prioridad.TODAS) + ") [" +
                    Prioridad.POR_DEFECTO + "]: ")
        prioridad = input(pregunta).upper() or Prioridad.POR_DEFECTO
        Prioridad.validar(prioridad)
        return prioridad

    # --- acciones del menu ---

    def registrar_solicitud(self):
        legajo = input("Legajo del estudiante: ")
        self.servicio.buscar_estudiante(legajo)
        tipo = input("Tipo (" + "/".join(Tipo.TODOS) + "): ").upper()
        Tipo.validar(tipo)
        descripcion = input("Descripcion: ")
        NuevaSolicitud.validar_descripcion(descripcion)
        prioridad = self.leer_prioridad()
        nueva = NuevaSolicitud(legajo, tipo, descripcion, prioridad)
        solicitud = self.servicio.registrar_solicitud(nueva)
        print("Solicitud registrada con id " + str(solicitud.id))

    def cambiar_estado(self):
        solicitud = self.leer_solicitud()
        nuevo = input("Nuevo estado (" + "/".join(Estado.DESTINOS) + "): ")
        nuevo = nuevo.upper()
        self.servicio.cambiar_estado(solicitud, nuevo)
        print("Estado actualizado a " + nuevo)

    def asignar_responsable(self):
        solicitud = self.leer_solicitud()
        solicitud.verificar_abierta()
        id_responsable = input("Id del responsable: ")
        responsable = self.servicio.asignar_responsable(solicitud,
                                                        id_responsable)
        print("Responsable asignado: " + responsable.nombre)

    def buscar_solicitudes(self):
        print("Filtrar por: 1) estado  2) tipo  3) legajo")
        opcion = input("Opcion: ")
        if opcion not in FILTROS:
            raise ErrorDeNegocio("Opcion invalida")
        campo, pregunta, a_mayusculas = FILTROS[opcion]
        valor = input(pregunta)
        if a_mayusculas:
            valor = valor.upper()
        self.mostrar_lista(self.servicio.filtrar(campo, valor))

    def reporte(self):
        print("=== REPORTE ===")
        print("Total de solicitudes: " + str(self.servicio.total()))
        for estado, cantidad in self.servicio.contar_por_estado().items():
            print(estado + ": " + str(cantidad))
        sin_responsable = self.servicio.contar_sin_responsable()
        print("Sin responsable asignado: " + str(sin_responsable))
        print("--- Pendientes por prioridad ---")
        for solicitud in self.servicio.pendientes_por_prioridad():
            print(solicitud.resumen())

    # --- salida ---

    def mostrar_lista(self, solicitudes):
        if len(solicitudes) == 0:
            print("No hay solicitudes para ese filtro")
        for solicitud in solicitudes:
            print(solicitud.resumen())
