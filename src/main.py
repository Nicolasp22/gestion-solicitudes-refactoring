# Sistema de gestion de solicitudes academicas
import json
from datetime import date

ARCHIVO = "datos.json"


class GestorSolicitudes:

    def __init__(self):
        self.datos = {"estudiantes": [], "responsables": [], "solicitudes": []}
        self.cargar()

    def cargar(self):
        try:
            f = open(ARCHIVO, "r", encoding="utf-8")
            self.datos = json.load(f)
            f.close()
        except:
            print("No se pudo leer el archivo de datos")

    def guardar(self):
        f = open(ARCHIVO, "w", encoding="utf-8")
        json.dump(self.datos, f, indent=2, ensure_ascii=False)
        f.close()

    def crear_solicitud(self, legajo, tipo, desc, prioridad, estado, resp, fecha):
        nuevo_id = 1
        for s in self.datos["solicitudes"]:
            if s["id"] >= nuevo_id:
                nuevo_id = s["id"] + 1
        s = {"id": nuevo_id, "legajo": legajo, "tipo": tipo, "descripcion": desc,
             "prioridad": prioridad, "estado": estado, "responsable": resp,
             "fecha": fecha}
        self.datos["solicitudes"].append(s)
        self.guardar()
        return nuevo_id

    def registrar_solicitud(self):
        legajo = input("Legajo del estudiante: ")
        e = None
        for x in self.datos["estudiantes"]:
            if x["legajo"] == legajo:
                e = x
        if e is None:
            print("Estudiante no encontrado")
            return
        tipo = input("Tipo (CERTIFICADO/EQUIVALENCIA/CONSULTA): ").upper()
        if tipo != "CERTIFICADO" and tipo != "EQUIVALENCIA" and tipo != "CONSULTA":
            print("Tipo invalido")
            return
        desc = input("Descripcion: ")
        if len(desc.strip()) == 0:
            print("La descripcion es obligatoria")
            return
        prioridad = input("Prioridad (ALTA/MEDIA/BAJA) [MEDIA]: ").upper()
        if prioridad == "":
            prioridad = "MEDIA"
        if prioridad != "ALTA" and prioridad != "MEDIA" and prioridad != "BAJA":
            print("Prioridad invalida")
            return
        nuevo_id = self.crear_solicitud(legajo, tipo, desc, prioridad, "PENDIENTE", None, str(date.today()))
        print("Solicitud registrada con id " + str(nuevo_id))

    def cambiar_estado(self):
        id_s = input("Id de la solicitud: ")
        try:
            id_s = int(id_s)
        except:
            print("Id invalido")
            return
        s = None
        for x in self.datos["solicitudes"]:
            if x["id"] == id_s:
                s = x
        if s is None:
            print("Solicitud no encontrada")
            return
        nuevo = input("Nuevo estado (EN_PROCESO/RESUELTA/RECHAZADA): ").upper()
        if s["estado"] == "PENDIENTE":
            if nuevo == "EN_PROCESO" or nuevo == "RECHAZADA":
                s["estado"] = nuevo
            else:
                print("Transicion no permitida")
                return
        elif s["estado"] == "EN_PROCESO":
            if nuevo == "RESUELTA" or nuevo == "RECHAZADA":
                s["estado"] = nuevo
            else:
                print("Transicion no permitida")
                return
        else:
            print("Transicion no permitida")
            return
        self.guardar()
        print("Estado actualizado a " + nuevo)

    def asignar_responsable(self):
        id_s = input("Id de la solicitud: ")
        try:
            id_s = int(id_s)
        except:
            print("Id invalido")
            return
        s = None
        for x in self.datos["solicitudes"]:
            if x["id"] == id_s:
                s = x
        if s is None:
            print("Solicitud no encontrada")
            return
        if s["estado"] == "RESUELTA" or s["estado"] == "RECHAZADA":
            print("La solicitud ya esta cerrada")
            return
        id_r = input("Id del responsable: ")
        r = None
        for x in self.datos["responsables"]:
            if x["id"] == id_r:
                r = x
        if r is None:
            print("Responsable no encontrado")
            return
        s["responsable"] = id_r
        self.guardar()
        print("Responsable asignado: " + r["nombre"])

    def buscar_solicitudes(self):
        print("Filtrar por: 1) estado  2) tipo  3) legajo")
        op = input("Opcion: ")
        if op == "1":
            valor = input("Estado: ").upper()
            res = []
            for s in self.datos["solicitudes"]:
                if s["estado"] == valor:
                    res.append(s)
        elif op == "2":
            valor = input("Tipo: ").upper()
            res = []
            for s in self.datos["solicitudes"]:
                if s["tipo"] == valor:
                    res.append(s)
        elif op == "3":
            valor = input("Legajo: ")
            res = []
            for s in self.datos["solicitudes"]:
                if s["legajo"] == valor:
                    res.append(s)
        else:
            print("Opcion invalida")
            return
        if len(res) == 0:
            print("No hay solicitudes para ese filtro")
        for s in res:
            print(str(s["id"]) + " | " + s["legajo"] + " | " + s["tipo"] + " | " + s["prioridad"] + " | " + s["estado"] + " | " + str(s["responsable"]))

    def reporte(self):
        total = len(self.datos["solicitudes"])
        pend = 0
        proc = 0
        res = 0
        rech = 0
        sin = 0
        for s in self.datos["solicitudes"]:
            if s["estado"] == "PENDIENTE":
                pend = pend + 1
            if s["estado"] == "EN_PROCESO":
                proc = proc + 1
            if s["estado"] == "RESUELTA":
                res = res + 1
            if s["estado"] == "RECHAZADA":
                rech = rech + 1
            if s["responsable"] == None:
                sin = sin + 1
        print("=== REPORTE ===")
        print("Total de solicitudes: " + str(total))
        print("PENDIENTE: " + str(pend))
        print("EN_PROCESO: " + str(proc))
        print("RESUELTA: " + str(res))
        print("RECHAZADA: " + str(rech))
        print("Sin responsable asignado: " + str(sin))
        print("--- Pendientes por prioridad ---")
        for p in ["ALTA", "MEDIA", "BAJA"]:
            for s in self.datos["solicitudes"]:
                if s["estado"] == "PENDIENTE" and s["prioridad"] == p:
                    print(str(s["id"]) + " | " + s["legajo"] + " | " + s["tipo"] + " | " + s["prioridad"] + " | " + s["estado"] + " | " + str(s["responsable"]))


def main():
    g = GestorSolicitudes()
    while True:
        print("")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar solicitudes")
        print("5. Reporte")
        print("0. Salir")
        op = input("Opcion: ")
        if op == "1":
            g.registrar_solicitud()
        elif op == "2":
            g.cambiar_estado()
        elif op == "3":
            g.asignar_responsable()
        elif op == "4":
            g.buscar_solicitudes()
        elif op == "5":
            g.reporte()
        elif op == "0":
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
