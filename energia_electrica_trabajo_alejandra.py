import heapq
import networkx as nx
import matplotlib.pyplot as plt

# =========================
#   DEFINICIÓN DEL GRAFO
# =========================

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


# =========================
#     ALGORITMO DIJKSTRA
# =========================

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


# =========================
#        SIMULACIÓN
# =========================

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
    print("\n=== RESULTADOS DE LA SIMULACIÓN ===\n")
    print(f"{'Ciudad':15} {'Distancia (km)':15} {'Energía Final (MWh)':20}")
    print("-" * 55)

    for r in resultados:
        print(f"{r['ciudad']:15} {r['distancia']:15.2f} {r['energia_final']:20.2f}")

    print("\n")


# =========================
#      VISUALIZACIÓN
# =========================

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


# =========================
#          MAIN
# =========================

ENERGIA_INICIAL = 1000
PERDIDA_POR_KM = 0.15
ORIGEN = "Zaragoza"


def main():
    grafo = construir_grafo_base()

    resultados = ejecutar_simulacion(grafo, ORIGEN, ENERGIA_INICIAL, PERDIDA_POR_KM)
    imprimir_tabla_resultados(resultados)

    # Visualización general
    dibujar_grafo_general(grafo, resultados)

    # Ejemplo: resaltar camino óptimo a Barcelona
    dibujar_camino_optimo(grafo, resultados, "Barcelona")


if __name__ == "__main__":
    main()
