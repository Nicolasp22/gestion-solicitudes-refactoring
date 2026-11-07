from datetime import date

from modelos import (ErrorDeNegocio, Estado, NuevaSolicitud, Prioridad,
                     Solicitud, Tipo)


class ServicioSolicitudes:
    # Reglas de negocio de las solicitudes. No lee del teclado ni imprime.

    def __init__(self, repositorio, estudiantes, responsables, solicitudes):
        self.repositorio = repositorio
        self.estudiantes = estudiantes
        self.responsables = responsables
        self.solicitudes = solicitudes

    def guardar(self):
        self.repositorio.guardar(self.estudiantes, self.responsables,
                                 self.solicitudes)

    # --- busquedas ---

    def buscar_estudiante(self, legajo):
        for estudiante in self.estudiantes:
            if estudiante.legajo == legajo:
                return estudiante
        raise ErrorDeNegocio("Estudiante no encontrado")

    def buscar_solicitud(self, id_solicitud):
        for solicitud in self.solicitudes:
            if solicitud.id == id_solicitud:
                return solicitud
        raise ErrorDeNegocio("Solicitud no encontrada")

    def buscar_responsable(self, id_responsable):
        for responsable in self.responsables:
            if responsable.id == id_responsable:
                return responsable
        raise ErrorDeNegocio("Responsable no encontrado")

    def filtrar(self, campo, valor):
        return [solicitud for solicitud in self.solicitudes
                if getattr(solicitud, campo) == valor]

    # --- operaciones ---

    def siguiente_id(self):
        return max([solicitud.id for solicitud in self.solicitudes],
                   default=0) + 1

    def registrar_solicitud(self, nueva):
        self.buscar_estudiante(nueva.legajo)
        Tipo.validar(nueva.tipo)
        NuevaSolicitud.validar_descripcion(nueva.descripcion)
        Prioridad.validar(nueva.prioridad)
        solicitud = Solicitud.desde_nueva(self.siguiente_id(), nueva,
                                          date.today().isoformat())
        self.solicitudes.append(solicitud)
        self.guardar()
        return solicitud

    def cambiar_estado(self, solicitud, nuevo_estado):
        solicitud.cambiar_estado(nuevo_estado)
        self.guardar()

    def asignar_responsable(self, solicitud, id_responsable):
        solicitud.verificar_abierta()
        responsable = self.buscar_responsable(id_responsable)
        solicitud.asignar_responsable(responsable.id)
        self.guardar()
        return responsable

    # --- datos para el reporte ---

    def total(self):
        return len(self.solicitudes)

    def contar_por_estado(self):
        cantidades = {}
        for estado in Estado.TODOS:
            cantidades[estado] = len([solicitud for solicitud in self.solicitudes
                                      if solicitud.estado == estado])
        return cantidades

    def contar_sin_responsable(self):
        return len([solicitud for solicitud in self.solicitudes
                    if solicitud.responsable is None])

    def pendientes_por_prioridad(self):
        pendientes = []
        for prioridad in Prioridad.TODAS:
            for solicitud in self.solicitudes:
                if (solicitud.estado == Estado.PENDIENTE and
                        solicitud.prioridad == prioridad):
                    pendientes.append(solicitud)
        return pendientes
