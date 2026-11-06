# Constantes del dominio de solicitudes academicas


class Estado:
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    RECHAZADA = "RECHAZADA"
    TODOS = [PENDIENTE, EN_PROCESO, RESUELTA, RECHAZADA]
    DESTINOS = [EN_PROCESO, RESUELTA, RECHAZADA]
    CERRADOS = [RESUELTA, RECHAZADA]


class Tipo:
    CERTIFICADO = "CERTIFICADO"
    EQUIVALENCIA = "EQUIVALENCIA"
    CONSULTA = "CONSULTA"
    TODOS = [CERTIFICADO, EQUIVALENCIA, CONSULTA]


class Prioridad:
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"
    TODAS = [ALTA, MEDIA, BAJA]
    POR_DEFECTO = MEDIA


class NuevaSolicitud:
    # Datos que se piden para registrar una solicitud

    def __init__(self, legajo, tipo, descripcion, prioridad):
        self.legajo = legajo
        self.tipo = tipo
        self.descripcion = descripcion
        self.prioridad = prioridad
