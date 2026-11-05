"""Pruebas de comportamiento externo.

Ejecutan el programa completo por consola (src/main.py), le envian entradas
y comprueban lo que muestra y lo que queda guardado en datos.json. No miran
el codigo interno, asi que valen igual para la version inicial y para la
refactorizada.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAMA = os.path.join(RAIZ, "src", "main.py")
DATOS_EJEMPLO = os.path.join(RAIZ, "datos", "datos_ejemplo.json")

LINEA_1 = "1 | 1001 | CERTIFICADO | ALTA | PENDIENTE | None"
LINEA_2 = "2 | 1002 | EQUIVALENCIA | MEDIA | EN_PROCESO | R3"
LINEA_4 = "4 | 1001 | CONSULTA | MEDIA | PENDIENTE | None"


class PruebasComportamiento(unittest.TestCase):

    def setUp(self):
        self.carpeta = tempfile.mkdtemp()
        self.archivo = os.path.join(self.carpeta, "datos.json")
        shutil.copy(DATOS_EJEMPLO, self.archivo)

    def tearDown(self):
        shutil.rmtree(self.carpeta)

    def ejecutar(self, *entradas):
        texto = "".join(entrada + "\n" for entrada in entradas) + "0\n"
        entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
        resultado = subprocess.run(
            [sys.executable, PROGRAMA], input=texto, capture_output=True,
            text=True, encoding="utf-8", cwd=self.carpeta, env=entorno,
            timeout=30)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        return resultado.stdout

    def leer_datos(self):
        with open(self.archivo, encoding="utf-8") as archivo:
            return json.load(archivo)

    def solicitud(self, id_solicitud):
        for solicitud in self.leer_datos()["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                return solicitud
        return None

    # --- arranque y menu ---

    def test_menu_se_muestra_y_sale(self):
        salida = self.ejecutar()
        for linea in ["1. Registrar solicitud", "2. Cambiar estado",
                      "3. Asignar responsable", "4. Buscar solicitudes",
                      "5. Reporte", "0. Salir"]:
            self.assertIn(linea, salida)

    def test_opcion_invalida_del_menu(self):
        salida = self.ejecutar("9")
        self.assertIn("Opcion invalida", salida)

    def test_archivo_inexistente_avisa_y_sigue(self):
        os.remove(self.archivo)
        salida = self.ejecutar()
        self.assertIn("No se pudo leer el archivo de datos", salida)

    # --- registrar solicitud ---

    def test_registrar_solicitud_valida(self):
        salida = self.ejecutar("1", "1001", "certificado",
                               "Necesito constancia", "alta")
        self.assertIn("Solicitud registrada con id 6", salida)
        nueva = self.solicitud(6)
        self.assertEqual(nueva["legajo"], "1001")
        self.assertEqual(nueva["tipo"], "CERTIFICADO")
        self.assertEqual(nueva["descripcion"], "Necesito constancia")
        self.assertEqual(nueva["prioridad"], "ALTA")
        self.assertEqual(nueva["estado"], "PENDIENTE")
        self.assertIsNone(nueva["responsable"])
        self.assertEqual(len(self.leer_datos()["solicitudes"]), 6)

    def test_registrar_usa_prioridad_media_por_defecto(self):
        self.ejecutar("1", "1003", "CONSULTA", "Horarios de cursada", "")
        self.assertEqual(self.solicitud(6)["prioridad"], "MEDIA")

    def test_registrar_con_legajo_inexistente(self):
        salida = self.ejecutar("1", "9999")
        self.assertIn("Estudiante no encontrado", salida)
        self.assertEqual(len(self.leer_datos()["solicitudes"]), 5)

    def test_registrar_con_tipo_invalido(self):
        salida = self.ejecutar("1", "1001", "OTRO")
        self.assertIn("Tipo invalido", salida)
        self.assertEqual(len(self.leer_datos()["solicitudes"]), 5)

    def test_registrar_con_descripcion_vacia(self):
        salida = self.ejecutar("1", "1001", "CONSULTA", "   ")
        self.assertIn("La descripcion es obligatoria", salida)
        self.assertEqual(len(self.leer_datos()["solicitudes"]), 5)

    def test_registrar_con_prioridad_invalida(self):
        salida = self.ejecutar("1", "1001", "CONSULTA", "Algo", "URGENTE")
        self.assertIn("Prioridad invalida", salida)
        self.assertEqual(len(self.leer_datos()["solicitudes"]), 5)

    # --- cambiar estado ---

    def test_cambiar_estado_valido(self):
        salida = self.ejecutar("2", "1", "en_proceso")
        self.assertIn("Estado actualizado a EN_PROCESO", salida)
        self.assertEqual(self.solicitud(1)["estado"], "EN_PROCESO")

    def test_cambiar_estado_con_transicion_no_permitida(self):
        salida = self.ejecutar("2", "1", "RESUELTA")
        self.assertIn("Transicion no permitida", salida)
        self.assertEqual(self.solicitud(1)["estado"], "PENDIENTE")

    def test_cambiar_estado_de_solicitud_cerrada(self):
        salida = self.ejecutar("2", "3", "EN_PROCESO")
        self.assertIn("Transicion no permitida", salida)
        self.assertEqual(self.solicitud(3)["estado"], "RESUELTA")

    def test_cambiar_estado_con_id_no_numerico(self):
        salida = self.ejecutar("2", "abc")
        self.assertIn("Id invalido", salida)

    def test_cambiar_estado_de_solicitud_inexistente(self):
        salida = self.ejecutar("2", "99")
        self.assertIn("Solicitud no encontrada", salida)

    # --- asignar responsable ---

    def test_asignar_responsable_valido(self):
        salida = self.ejecutar("3", "1", "R2")
        self.assertIn("Responsable asignado: Marcos Silva", salida)
        self.assertEqual(self.solicitud(1)["responsable"], "R2")

    def test_asignar_responsable_a_solicitud_cerrada(self):
        salida = self.ejecutar("3", "3")
        self.assertIn("La solicitud ya esta cerrada", salida)
        self.assertNotIn("Id del responsable", salida)
        self.assertEqual(self.solicitud(3)["responsable"], "R1")

    def test_asignar_responsable_inexistente(self):
        salida = self.ejecutar("3", "1", "R9")
        self.assertIn("Responsable no encontrado", salida)
        self.assertIsNone(self.solicitud(1)["responsable"])

    # --- buscar solicitudes ---

    def test_buscar_por_estado(self):
        salida = self.ejecutar("4", "1", "pendiente")
        self.assertIn(LINEA_1, salida)
        self.assertIn(LINEA_4, salida)
        self.assertNotIn(LINEA_2, salida)

    def test_buscar_por_tipo(self):
        salida = self.ejecutar("4", "2", "equivalencia")
        self.assertIn(LINEA_2, salida)
        self.assertNotIn(LINEA_1, salida)

    def test_buscar_por_legajo(self):
        salida = self.ejecutar("4", "3", "1001")
        self.assertIn(LINEA_1, salida)
        self.assertIn(LINEA_4, salida)
        self.assertNotIn(LINEA_2, salida)

    def test_buscar_sin_resultados(self):
        salida = self.ejecutar("4", "3", "5555")
        self.assertIn("No hay solicitudes para ese filtro", salida)

    def test_buscar_con_opcion_invalida(self):
        salida = self.ejecutar("4", "7")
        self.assertIn("Opcion invalida", salida)

    # --- reporte ---

    def test_reporte_basico(self):
        salida = self.ejecutar("5")
        self.assertIn("=== REPORTE ===", salida)
        self.assertIn("Total de solicitudes: 5", salida)
        self.assertIn("PENDIENTE: 2", salida)
        self.assertIn("EN_PROCESO: 1", salida)
        self.assertIn("RESUELTA: 1", salida)
        self.assertIn("RECHAZADA: 1", salida)
        self.assertIn("Sin responsable asignado: 2", salida)
        pendientes = salida.split("--- Pendientes por prioridad ---")[1]
        self.assertLess(pendientes.index(LINEA_1), pendientes.index(LINEA_4))

    # --- flujo completo ---

    def test_flujo_completo_de_una_solicitud(self):
        self.ejecutar("1", "1002", "EQUIVALENCIA",
                      "Equivalencia de Matematica", "",
                      "2", "6", "EN_PROCESO", "3", "6", "R2",
                      "2", "6", "RESUELTA")
        final = self.solicitud(6)
        self.assertEqual(final["estado"], "RESUELTA")
        self.assertEqual(final["responsable"], "R2")
        self.assertEqual(final["prioridad"], "MEDIA")


if __name__ == "__main__":
    unittest.main()
