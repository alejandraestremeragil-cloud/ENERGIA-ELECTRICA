ciudades = [
    "Zaragoza", "Huesca", "Teruel", "Madrid",
    "Barcelona", "Valencia", "Bilbao", "San_Sebastian"
]

conexiones = {
    "Zaragoza": [("Huesca", 74), ("Teruel", 171), ("Madrid", 314),
                 ("Barcelona", 296), ("Valencia", 309), ("Bilbao", 304)],
    "Bilbao": [("San_Sebastian", 99)],
    "Huesca": [],
    "Teruel": [],
    "Madrid": [],
    "Barcelona": [],
    "Valencia": [],
    "San_Sebastian": []
}

ENERGIA_INICIAL = 1000  # MWh
PERDIDA_POR_KM = 0.15  # MWh por km


class Grafo:
    def __init__(self):
        self.adyacencia = {}

    def agregar_ciudad(self, ciudad):
        if ciudad not in self.adyacencia:
            self.adyacencia[ciudad] = []

    def agregar_conexion(self, origen, destino, distancia):
        """
        Agrega una arista dirigida desde origen hacia destino.
        El peso representa la distancia o pérdida energética.
        """
        self.agregar_ciudad(origen)
        self.agregar_ciudad(destino)
        self.adyacencia[origen].append((destino, distancia))

    def obtener_vecinos(self, ciudad):
        return self.adyacencia.get(ciudad, [])

    def __str__(self):
        return str(self.adyacencia)


def construir_grafo_base():
    g = Grafo()

    conexiones = {
        "Zaragoza": [("Huesca", 74), ("Teruel", 171), ("Madrid", 314),
                     ("Barcelona", 296), ("Valencia", 309), ("Bilbao", 304)],
        "Bilbao": [("San_Sebastian", 99)],
        "Huesca": [],
        "Teruel": [],
        "Madrid": [],
        "Barcelona": [],
        "Valencia": [],
        "San_Sebastian": []
    }

    for origen, destinos in conexiones.items():
        for destino, distancia in destinos:
            g.agregar_conexion(origen, destino, distancia)

    return g
