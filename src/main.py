# Sistema de gestion de solicitudes academicas
# Punto de entrada: arma las piezas y arranca el menu.
from consola import Consola
from repositorio import ErrorDeDatos, RepositorioJSON
from servicio import ServicioSolicitudes

ARCHIVO = "datos.json"


def cargar_datos(repositorio):
    try:
        return repositorio.cargar()
    except ErrorDeDatos as error:
        print(error)
        return [], [], []


def main():
    repositorio = RepositorioJSON(ARCHIVO)
    estudiantes, responsables, solicitudes = cargar_datos(repositorio)
    servicio = ServicioSolicitudes(repositorio, estudiantes, responsables,
                                   solicitudes)
    Consola(servicio).ejecutar()


if __name__ == "__main__":
    main()
