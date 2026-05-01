import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math

ciudades_españa = {
    "Madrid": (40.4168, -3.7038),
    "Barcelona": (41.3874, 2.1686),
    "Sevilla": (37.3891, -5.9845),
    "Valencia": (39.4699, -0.3763),
    "Zaragoza": (41.6488, -0.8891),
    "Bilbao": (43.2630, -2.9350),
    "Málaga": (36.7213, -4.4214),
    "Murcia": (37.9922, -1.1307),
    "Valladolid": (41.6523, -4.7245),
    "Gijón": (43.5322, -5.6611),
    "A Coruña": (43.3623, -8.4115),
    "Granada": (37.1773, -3.5986),
    "Cádiz": (36.5271, -6.2886),
    "Pamplona": (42.8125, -1.6458),
    "San_Sebastian": (43.3183, -1.9812)
}

def distancia_geo(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


#   DEFINICIÓN DEL GRAFO

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


#     ALGORITMO DIJKSTRA

def dijkstra(grafo, origen):
    """
    Calcula la distancia mínima desde 'origen' a todos los nodos del grafo.

    Retorna:
        distancias: diccionario {ciudad: distancia_minima}
        previos: diccionario {ciudad: nodo_anterior_en_el_camino}
    """
    distancias = {ciudad: float('inf') for ciudad in grafo.adyacencia}
    distancias[origen] = 0

    previos = {ciudad: None for ciudad in grafo.adyacencia}

    cola = [(0, origen)]  # (distancia, ciudad)

    while cola:
        distancia_actual, ciudad_actual = heapq.heappop(cola)

        if distancia_actual > distancias[ciudad_actual]:
            continue

        for vecino, peso in grafo.obtener_vecinos(ciudad_actual):
            nueva_distancia = distancia_actual + peso

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                previos[vecino] = ciudad_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, previos


def reconstruir_camino(previos, destino):
    """
    Reconstruye el camino óptimo desde el origen hasta 'destino'
    usando el diccionario de previos generado por Dijkstra.
    """
    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        actual = previos[actual]

    camino.reverse()
    return camino


def calcular_energia(distancia_total, energia_inicial, perdida_por_km):
    """
    Calcula la energía restante después de recorrer una distancia.
        energía_final = energía_inicial - (distancia_total * pérdida_por_km)
    """
    energia_final = energia_inicial - (distancia_total * perdida_por_km)
    return max(energia_final, 0)


#        SIMULACIÓN

def ejecutar_simulacion(grafo, origen, energia_inicial, perdida_por_km):
    """
    Ejecuta la simulación completa:
    - Calcula distancias mínimas con Dijkstra
    - Reconstruye caminos óptimos
    - Calcula energía que llega a cada ciudad
    """
    distancias, previos = dijkstra(grafo, origen)

    resultados = []

    for ciudad, distancia in distancias.items():
        camino = reconstruir_camino(previos, ciudad)
        energia_final = calcular_energia(distancia, energia_inicial, perdida_por_km)

        resultados.append({
            "ciudad": ciudad,
            "distancia": distancia,
            "camino": camino,
            "energia_final": energia_final
        })

    return resultados


def imprimir_tabla_resultados(resultados):
    """
    Imprime una tabla con:
    - Ciudad
    - Distancia mínima
    - Energía que llega
    """
    print("\n RESULTADOS DE LA SIMULACIÓN \n")
    print(f"{'Ciudad':15} {'Distancia (km)':15} {'Energía Final (MWh)':20}")
    print("-" * 55)

    for r in resultados:
        print(f"{r['ciudad']:15} {r['distancia']:15.2f} {r['energia_final']:20.2f}")

    print("\n")

def ciudad_mas_cercana(ciudad_usuario, ciudades_españa, grafo):
    coord_usuario = ciudades_españa[ciudad_usuario]

    mejor_ciudad = None
    mejor_distancia = float("inf")

    for ciudad in grafo.adyacencia.keys():
        if ciudad not in ciudades_españa:
            continue
        coord_ciudad = ciudades_españa[ciudad]
        d = distancia_geo(coord_usuario, coord_ciudad)

        if d < mejor_distancia:
            mejor_distancia = d
            mejor_ciudad = ciudad

    return mejor_ciudad, mejor_distancia

def crear_conexion_nueva(grafo, ciudad_grafo, ciudad_usuario, ciudades_españa):
    # Distancia geográfica real
    distancia = distancia_geo(ciudades_españa[ciudad_grafo], ciudades_españa[ciudad_usuario])

    # Coste estimado de construcción (ejemplo: 1 millón por km)
    coste_construccion = distancia * 1_000_000  

    # Añadimos la conexión al grafo como una arista nueva
    grafo.agregar_conexion(ciudad_grafo, ciudad_usuario, distancia)

    return distancia, coste_construccion


def explicar_mejor_ruta(resultados, origen):
    destinos = [r for r in resultados if r["ciudad"] != origen]
    mejor = max(destinos, key=lambda r: r["energia_final"])

    ciudad = mejor["ciudad"]
    energia = mejor["energia_final"]
    distancia = mejor["distancia"]
    camino = " → ".join(mejor["camino"])

    print("\n ANÁLISIS DE LA RUTA MÁS EFICIENTE \n")
    print(f"La ciudad que recibe más energía final es {ciudad}.")
    print(f"Esto ocurre porque su ruta desde {origen} presenta:")
    print(f" - Una distancia total de {distancia:.2f} km")
    print(f" - Un consumo energético menor que el resto de rutas")
    print(f" - Camino óptimo según Dijkstra: {camino}")
    print(f"\nEnergía que llega a {ciudad}: {energia:.2f} MWh\n")

    return mejor


#      VISUALIZACIÓN

def construir_grafo_networkx(grafo):
    """
    Convierte nuestro grafo propio en un grafo de NetworkX.
    """
    G = nx.DiGraph()

    for origen, vecinos in grafo.adyacencia.items():
        for destino, distancia in vecinos:
            G.add_edge(origen, destino, weight=distancia)

    return G


def dibujar_grafo_general(grafo, resultados):
    import matplotlib.pyplot as plt
    import networkx as nx

    G = construir_grafo_networkx(grafo)
    pos = nx.spring_layout(G, seed=42)

    energia_por_ciudad = {r["ciudad"]: r["energia_final"] for r in resultados}
    energias = [energia_por_ciudad[n] for n in G.nodes()]

    # Crear figura y ejes explícitamente
    fig, ax = plt.subplots(figsize=(10, 7))

    # Dibujar nodos
    nodos = nx.draw_networkx_nodes(
        G, pos,
        node_size=800,
        node_color=energias,
        cmap=plt.cm.plasma,
        ax=ax
    )

        # --- NUEVA CONEXIÓN ARTIFICIAL (si existe) ---
    if hasattr(grafo, "conexion_nueva"):
        ciudad_grafo, ciudad_usuario = grafo.conexion_nueva

        if ciudad_usuario in G.nodes():
            nx.draw_networkx_edges(
                G, pos,
                edgelist=[(ciudad_grafo, ciudad_usuario)],
                edge_color="green",
                width=3,
                arrowstyle="->",
                arrowsize=20,
                ax=ax
            )


    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, ax=ax)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "weight"),
        font_size=8,
        ax=ax
    )

    # Colorbar correctamente asociado al eje
    cbar = fig.colorbar(nodos, ax=ax, shrink=0.8)
    cbar.set_label("Energía final aproximada (MWh)")

    ax.set_title("Red de distribución eléctrica – Energía en cada ciudad")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()



def dibujar_camino_optimo(grafo, resultados, ciudad_destino):
    """
    Dibuja el grafo resaltando el camino óptimo hacia una ciudad destino.
    """
    G = construir_grafo_networkx(grafo)
    pos = nx.spring_layout(G, seed=42)

    destino_data = next((r for r in resultados if r["ciudad"] == ciudad_destino), None)
    if destino_data is None:
        print(f"No se encontró información para la ciudad: {ciudad_destino}")
        return

    camino = destino_data["camino"]
    aristas_camino = list(zip(camino[:-1], camino[1:]))

    plt.figure(figsize=(10, 7))

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color="lightgray")
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    nx.draw_networkx_edges(G, pos, edge_color="lightgray", arrowstyle="->", arrowsize=15)

    nx.draw_networkx_edges(
        G, pos,
        edgelist=aristas_camino,
        edge_color="red",
        width=2.5,
        arrowstyle="->",
        arrowsize=18
    )

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "weight"),
        font_size=8
    )

    plt.title(f"Camino óptimo desde Zaragoza hasta {ciudad_destino}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def explicar_rentabilidad(distancia, coste, energia_final):
    print("\n=== ANÁLISIS DE RENTABILIDAD ===\n")
    print(f"Distancia de la nueva línea: {distancia:.2f} km")
    print(f"Coste estimado de construcción: {coste:,.0f} €")
    print(f"Energía que llegaría a la ciudad destino: {energia_final:.2f} MWh")

    if energia_final < 500:
        print("\nConclusión: NO sería rentable construir esta línea.")
    else:
        print("\nConclusión: Podría ser rentable dependiendo de la demanda.")


# =========================
#          MAIN
# =========================

ENERGIA_INICIAL = 1000
PERDIDA_POR_KM = 0.15
ORIGEN = "Zaragoza"


def main():
    grafo = construir_grafo_base()

    ciudad_usuario = input("¿En qué ciudad vives? (Ej: Sevilla): ")

    if ciudad_usuario not in ciudades_españa:
        print("Esa ciudad no está en la base de datos.")
        return

    ciudad_cercana, distancia_cercana = ciudad_mas_cercana(ciudad_usuario, ciudades_españa, grafo)

    print(f"\nLa ciudad del sistema eléctrico más cercana a {ciudad_usuario} es {ciudad_cercana}, a {distancia_cercana:.2f} km.")
    print("La energía se transportará desde Zaragoza hasta ese nodo.\n")

    resultados = ejecutar_simulacion(grafo, ORIGEN, ENERGIA_INICIAL, PERDIDA_POR_KM)
    imprimir_tabla_resultados(resultados)

    explicar_mejor_ruta(resultados, ORIGEN)

    dibujar_grafo_general(grafo, resultados)
    dibujar_camino_optimo(grafo, resultados, ciudad_cercana)

if __name__ == "__main__":
    main()
