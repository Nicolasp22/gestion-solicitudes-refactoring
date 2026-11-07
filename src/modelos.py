# Modelo del dominio de solicitudes academicas


class ErrorDeNegocio(Exception):
    # Error que se le muestra al usuario, por ejemplo "Tipo invalido"
    pass


class Estado:
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    RECHAZADA = "RECHAZADA"
    TODOS = [PENDIENTE, EN_PROCESO, RESUELTA, RECHAZADA]
    DESTINOS = [EN_PROCESO, RESUELTA, RECHAZADA]
    CERRADOS = [RESUELTA, RECHAZADA]
    TRANSICIONES = {
        PENDIENTE: [EN_PROCESO, RECHAZADA],
        EN_PROCESO: [RESUELTA, RECHAZADA],
    }


class Tipo:
    CERTIFICADO = "CERTIFICADO"
    EQUIVALENCIA = "EQUIVALENCIA"
    CONSULTA = "CONSULTA"
    TODOS = [CERTIFICADO, EQUIVALENCIA, CONSULTA]

    @staticmethod
    def validar(tipo):
        if tipo not in Tipo.TODOS:
            raise ErrorDeNegocio("Tipo invalido")


class Prioridad:
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"
    TODAS = [ALTA, MEDIA, BAJA]
    POR_DEFECTO = MEDIA

    @staticmethod
    def validar(prioridad):
        if prioridad not in Prioridad.TODAS:
            raise ErrorDeNegocio("Prioridad invalida")


class NuevaSolicitud:
    # Datos que se piden para registrar una solicitud

    def __init__(self, legajo, tipo, descripcion, prioridad):
        self.legajo = legajo
        self.tipo = tipo
        self.descripcion = descripcion
        self.prioridad = prioridad

    @staticmethod
    def validar_descripcion(descripcion):
        if len(descripcion.strip()) == 0:
            raise ErrorDeNegocio("La descripcion es obligatoria")


class Estudiante:

    def __init__(self, legajo, nombre, email):
        self.legajo = legajo
        self.nombre = nombre
        self.email = email

    @staticmethod
    def desde_diccionario(datos):
        return Estudiante(datos["legajo"], datos["nombre"], datos["email"])

    def a_diccionario(self):
        return {"legajo": self.legajo, "nombre": self.nombre,
                "email": self.email}


class Responsable:

    def __init__(self, id_responsable, nombre, area):
        self.id = id_responsable
        self.nombre = nombre
        self.area = area

    @staticmethod
    def desde_diccionario(datos):
        return Responsable(datos["id"], datos["nombre"], datos["area"])

    def a_diccionario(self):
        return {"id": self.id, "nombre": self.nombre, "area": self.area}


class Solicitud:

    def __init__(self, id_solicitud, legajo, tipo, descripcion, prioridad,
                 estado, responsable, fecha):
        self.id = id_solicitud
        self.legajo = legajo
        self.tipo = tipo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.responsable = responsable
        self.fecha = fecha

    @staticmethod
    def desde_nueva(id_solicitud, nueva, fecha):
        return Solicitud(id_solicitud, nueva.legajo, nueva.tipo,
                         nueva.descripcion, nueva.prioridad,
                         Estado.PENDIENTE, None, fecha)

    @staticmethod
    def desde_diccionario(datos):
        return Solicitud(datos["id"], datos["legajo"], datos["tipo"],
                         datos["descripcion"], datos["prioridad"],
                         datos["estado"], datos["responsable"],
                         datos["fecha"])

    def a_diccionario(self):
        return {"id": self.id, "legajo": self.legajo, "tipo": self.tipo,
                "descripcion": self.descripcion, "prioridad": self.prioridad,
                "estado": self.estado, "responsable": self.responsable,
                "fecha": self.fecha}

    def esta_cerrada(self):
        return self.estado in Estado.CERRADOS

    def verificar_abierta(self):
        if self.esta_cerrada():
            raise ErrorDeNegocio("La solicitud ya esta cerrada")

    def puede_pasar_a(self, nuevo_estado):
        return nuevo_estado in Estado.TRANSICIONES.get(self.estado, [])

    def cambiar_estado(self, nuevo_estado):
        if not self.puede_pasar_a(nuevo_estado):
            raise ErrorDeNegocio("Transicion no permitida")
        self.estado = nuevo_estado

    def asignar_responsable(self, id_responsable):
        self.verificar_abierta()
        self.responsable = id_responsable

    def resumen(self):
        return " | ".join([str(self.id), self.legajo, self.tipo,
                           self.prioridad, self.estado,
                           str(self.responsable)])
