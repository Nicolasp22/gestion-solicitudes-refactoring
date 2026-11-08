"""Pruebas unitarias del codigo refactorizado.

Prueban las piezas por separado: modelos, servicio y repositorio. Existen
recien despues del refactoring porque el codigo inicial era una sola clase
que mezclaba todo y no se podia probar por partes.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))

from modelos import (ErrorDeNegocio, Estado, Estudiante,  # noqa: E402
                     NuevaSolicitud, Prioridad, Responsable, Solicitud, Tipo)
from repositorio import ErrorDeDatos, RepositorioJSON  # noqa: E402
from servicio import ServicioSolicitudes  # noqa: E402

DATOS_EJEMPLO = os.path.join(RAIZ, "datos", "datos_ejemplo.json")


class RepositorioEnMemoria:
    # Reemplaza al repositorio real en las pruebas: no toca el disco

    def __init__(self):
        self.guardados = 0

    def guardar(self, estudiantes, responsables, solicitudes):
        self.guardados = self.guardados + 1


def crear_solicitud(id_solicitud=1, estado=Estado.PENDIENTE,
                    prioridad=Prioridad.MEDIA, legajo="1001"):
    return Solicitud(id_solicitud, legajo, Tipo.CONSULTA, "Una consulta",
                     prioridad, estado, None, "2026-10-01")


def crear_servicio(solicitudes=None):
    if solicitudes is None:
        solicitudes = [crear_solicitud(1, Estado.PENDIENTE),
                       crear_solicitud(2, Estado.EN_PROCESO),
                       crear_solicitud(3, Estado.RESUELTA)]
    estudiantes = [Estudiante("1001", "Ana Perez", "ana@example.com")]
    responsables = [Responsable("R1", "Laura Gomez", "Alumnado"),
                    Responsable("R2", "Marcos Silva", "Tesoreria")]
    repositorio = RepositorioEnMemoria()
    servicio = ServicioSolicitudes(repositorio, estudiantes, responsables,
                                   solicitudes)
    return servicio, repositorio


class PruebasSolicitud(unittest.TestCase):

    def test_transiciones_permitidas(self):
        permitidas = [(Estado.PENDIENTE, Estado.EN_PROCESO),
                      (Estado.PENDIENTE, Estado.RECHAZADA),
                      (Estado.EN_PROCESO, Estado.RESUELTA),
                      (Estado.EN_PROCESO, Estado.RECHAZADA)]
        for origen, destino in permitidas:
            solicitud = crear_solicitud(estado=origen)
            self.assertTrue(solicitud.puede_pasar_a(destino))

    def test_transiciones_no_permitidas(self):
        prohibidas = [(Estado.PENDIENTE, Estado.RESUELTA),
                      (Estado.EN_PROCESO, Estado.PENDIENTE),
                      (Estado.RESUELTA, Estado.EN_PROCESO),
                      (Estado.RECHAZADA, Estado.EN_PROCESO),
                      (Estado.PENDIENTE, "INVENTADO")]
        for origen, destino in prohibidas:
            solicitud = crear_solicitud(estado=origen)
            self.assertFalse(solicitud.puede_pasar_a(destino))

    def test_cambiar_estado_actualiza_el_estado(self):
        solicitud = crear_solicitud(estado=Estado.PENDIENTE)
        solicitud.cambiar_estado(Estado.EN_PROCESO)
        self.assertEqual(solicitud.estado, Estado.EN_PROCESO)

    def test_cambiar_estado_no_permitido_lanza_error_y_no_cambia(self):
        solicitud = crear_solicitud(estado=Estado.PENDIENTE)
        with self.assertRaises(ErrorDeNegocio):
            solicitud.cambiar_estado(Estado.RESUELTA)
        self.assertEqual(solicitud.estado, Estado.PENDIENTE)

    def test_esta_cerrada(self):
        for estado in (Estado.RESUELTA, Estado.RECHAZADA):
            self.assertTrue(crear_solicitud(estado=estado).esta_cerrada())
        for estado in (Estado.PENDIENTE, Estado.EN_PROCESO):
            self.assertFalse(crear_solicitud(estado=estado).esta_cerrada())

    def test_asignar_responsable_en_solicitud_cerrada_lanza_error(self):
        solicitud = crear_solicitud(estado=Estado.RESUELTA)
        with self.assertRaises(ErrorDeNegocio):
            solicitud.asignar_responsable("R1")
        self.assertIsNone(solicitud.responsable)

    def test_resumen_tiene_el_formato_del_listado(self):
        self.assertEqual(
            crear_solicitud().resumen(),
            "1 | 1001 | CONSULTA | MEDIA | PENDIENTE | None")

    def test_ida_y_vuelta_con_diccionario(self):
        datos = crear_solicitud(7, Estado.EN_PROCESO).a_diccionario()
        self.assertEqual(Solicitud.desde_diccionario(datos).a_diccionario(),
                         datos)


class PruebasValidaciones(unittest.TestCase):

    def test_tipo_valido_e_invalido(self):
        Tipo.validar(Tipo.CERTIFICADO)
        with self.assertRaises(ErrorDeNegocio):
            Tipo.validar("OTRO")

    def test_prioridad_valida_e_invalida(self):
        Prioridad.validar(Prioridad.ALTA)
        with self.assertRaises(ErrorDeNegocio):
            Prioridad.validar("URGENTE")

    def test_descripcion_vacia_o_con_solo_espacios(self):
        NuevaSolicitud.validar_descripcion("Algo")
        with self.assertRaises(ErrorDeNegocio):
            NuevaSolicitud.validar_descripcion("")
        with self.assertRaises(ErrorDeNegocio):
            NuevaSolicitud.validar_descripcion("   ")


class PruebasServicio(unittest.TestCase):

    def test_registrar_asigna_el_id_siguiente_y_guarda(self):
        servicio, repositorio = crear_servicio()
        nueva = NuevaSolicitud("1001", Tipo.CERTIFICADO, "Constancia",
                               Prioridad.ALTA)
        solicitud = servicio.registrar_solicitud(nueva)
        self.assertEqual(solicitud.id, 4)
        self.assertEqual(solicitud.estado, Estado.PENDIENTE)
        self.assertIsNone(solicitud.responsable)
        self.assertEqual(servicio.total(), 4)
        self.assertEqual(repositorio.guardados, 1)

    def test_registrar_con_estudiante_inexistente_lanza_error(self):
        servicio, repositorio = crear_servicio()
        nueva = NuevaSolicitud("9999", Tipo.CONSULTA, "Algo", Prioridad.MEDIA)
        with self.assertRaises(ErrorDeNegocio):
            servicio.registrar_solicitud(nueva)
        self.assertEqual(servicio.total(), 3)
        self.assertEqual(repositorio.guardados, 0)

    def test_registrar_con_tipo_invalido_no_agrega_nada(self):
        servicio, repositorio = crear_servicio()
        nueva = NuevaSolicitud("1001", "OTRO", "Algo", Prioridad.MEDIA)
        with self.assertRaises(ErrorDeNegocio):
            servicio.registrar_solicitud(nueva)
        self.assertEqual(servicio.total(), 3)
        self.assertEqual(repositorio.guardados, 0)

    def test_siguiente_id_sin_solicitudes_es_uno(self):
        servicio, _ = crear_servicio(solicitudes=[])
        self.assertEqual(servicio.siguiente_id(), 1)

    def test_cambiar_estado_guarda(self):
        servicio, repositorio = crear_servicio()
        solicitud = servicio.buscar_solicitud(1)
        servicio.cambiar_estado(solicitud, Estado.EN_PROCESO)
        self.assertEqual(solicitud.estado, Estado.EN_PROCESO)
        self.assertEqual(repositorio.guardados, 1)

    def test_asignar_responsable_valido(self):
        servicio, repositorio = crear_servicio()
        solicitud = servicio.buscar_solicitud(1)
        responsable = servicio.asignar_responsable(solicitud, "R2")
        self.assertEqual(responsable.nombre, "Marcos Silva")
        self.assertEqual(solicitud.responsable, "R2")
        self.assertEqual(repositorio.guardados, 1)

    def test_asignar_responsable_inexistente_lanza_error(self):
        servicio, repositorio = crear_servicio()
        solicitud = servicio.buscar_solicitud(1)
        with self.assertRaises(ErrorDeNegocio):
            servicio.asignar_responsable(solicitud, "R9")
        self.assertIsNone(solicitud.responsable)
        self.assertEqual(repositorio.guardados, 0)

    def test_asignar_responsable_a_solicitud_cerrada_lanza_error(self):
        servicio, _ = crear_servicio()
        solicitud = servicio.buscar_solicitud(3)
        with self.assertRaises(ErrorDeNegocio):
            servicio.asignar_responsable(solicitud, "R1")

    def test_buscar_solicitud_inexistente_lanza_error(self):
        servicio, _ = crear_servicio()
        with self.assertRaises(ErrorDeNegocio):
            servicio.buscar_solicitud(99)

    def test_filtrar_por_estado_y_por_legajo(self):
        servicio, _ = crear_servicio()
        pendientes = servicio.filtrar("estado", Estado.PENDIENTE)
        self.assertEqual([s.id for s in pendientes], [1])
        del_estudiante = servicio.filtrar("legajo", "1001")
        self.assertEqual(len(del_estudiante), 3)
        self.assertEqual(servicio.filtrar("legajo", "0000"), [])

    def test_contar_por_estado_incluye_todos_los_estados(self):
        servicio, _ = crear_servicio()
        self.assertEqual(servicio.contar_por_estado(),
                         {Estado.PENDIENTE: 1, Estado.EN_PROCESO: 1,
                          Estado.RESUELTA: 1, Estado.RECHAZADA: 0})

    def test_contar_sin_responsable(self):
        servicio, _ = crear_servicio()
        self.assertEqual(servicio.contar_sin_responsable(), 3)
        servicio.asignar_responsable(servicio.buscar_solicitud(1), "R1")
        self.assertEqual(servicio.contar_sin_responsable(), 2)

    def test_pendientes_se_ordenan_por_prioridad(self):
        servicio, _ = crear_servicio(solicitudes=[
            crear_solicitud(1, prioridad=Prioridad.BAJA),
            crear_solicitud(2, prioridad=Prioridad.ALTA),
            crear_solicitud(3, prioridad=Prioridad.MEDIA),
            crear_solicitud(4, Estado.RESUELTA, Prioridad.ALTA)])
        ids = [s.id for s in servicio.pendientes_por_prioridad()]
        self.assertEqual(ids, [2, 3, 1])


class PruebasRepositorio(unittest.TestCase):

    def setUp(self):
        self.carpeta = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.carpeta)

    def test_cargar_archivo_inexistente_lanza_error_de_datos(self):
        repositorio = RepositorioJSON(os.path.join(self.carpeta, "no.json"))
        with self.assertRaises(ErrorDeDatos):
            repositorio.cargar()

    def test_cargar_json_invalido_lanza_error_de_datos(self):
        ruta = os.path.join(self.carpeta, "roto.json")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("esto no es json")
        with self.assertRaises(ErrorDeDatos):
            RepositorioJSON(ruta).cargar()

    def test_guardar_y_cargar_conserva_los_datos(self):
        ruta = os.path.join(self.carpeta, "copia.json")
        original = RepositorioJSON(DATOS_EJEMPLO)
        RepositorioJSON(ruta).guardar(*original.cargar())
        with open(DATOS_EJEMPLO, encoding="utf-8") as archivo:
            esperado = json.load(archivo)
        with open(ruta, encoding="utf-8") as archivo:
            obtenido = json.load(archivo)
        self.assertEqual(obtenido, esperado)


if __name__ == "__main__":
    unittest.main()
