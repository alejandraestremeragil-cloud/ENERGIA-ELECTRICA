import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math

# ─────────────────────────────────────────────
#   BASE DE DATOS: 47 PROVINCIAS PENINSULARES
# ─────────────────────────────────────────────

provincias_peninsula = {
    # Aragón
    "Zaragoza":     (41.6488, -0.8891),
    "Huesca":       (42.1401, -0.4089),
    "Teruel":       (40.3456, -1.1065),

    # Cataluña
    "Barcelona":    (41.3874,  2.1686),
    "Girona":       (41.9794,  2.8214),
    "Lleida":       (41.6176,  0.6200),
    "Tarragona":    (41.1189,  1.2445),

    # Comunidad Valenciana
    "Valencia":     (39.4699, -0.3763),
    "Castellon":    (39.9864, -0.0513),
    "Alicante":     (38.3452, -0.4810),

    # Madrid
    "Madrid":       (40.4168, -3.7038),

    # Castilla-La Mancha
    "Guadalajara":  (40.6334, -3.1674),
    "Cuenca":       (40.0704, -2.1374),
    "Toledo":       (39.8628, -4.0273),
    "Ciudad_Real":  (38.9848, -3.9274),
    "Albacete":     (38.9943, -1.8585),

    # Castilla y León
    "Soria":        (41.7640, -2.4650),
    "Segovia":      (40.9429, -4.1088),
    "Avila":        (40.6567, -4.6976),
    "Salamanca":    (40.9701, -5.6635),
    "Zamora":       (41.5034, -5.7447),
    "Valladolid":   (41.6523, -4.7245),
    "Palencia":     (42.0097, -4.5288),
    "Leon":         (42.5987, -5.5671),
    "Burgos":       (42.3439, -3.6970),

    # La Rioja
    "Logrono":      (42.4627, -2.4449),

    # Navarra
    "Pamplona":     (42.8125, -1.6458),

    # País Vasco
    "Bilbao":       (43.2630, -2.9350),
    "San_Sebastian":(43.3183, -1.9812),
    "Vitoria":      (42.8467, -2.6727),

    # Cantabria
    "Santander":    (43.4623, -3.8099),

    # Asturias
    "Oviedo":       (43.3614, -5.8593),

    # Galicia
    "Lugo":         (43.0097, -7.5560),
    "Ourense":      (42.3354, -7.8639),
    "Pontevedra":   (42.4336, -8.6488),
    "A_Coruna":     (43.3623, -8.4115),

    # Extremadura
    "Caceres":      (39.4753, -6.3724),
    "Badajoz":      (38.8794, -6.9706),

    # Andalucía
    "Huelva":       (37.2614, -6.9447),
    "Sevilla":      (37.3891, -5.9845),
    "Cadiz":        (36.5271, -6.2886),
    "Malaga":       (36.7213, -4.4214),
    "Cordoba":      (37.8882, -4.7794),
    "Jaen":         (37.7796, -3.7849),
    "Granada":      (37.1773, -3.5986),
    "Almeria":      (36.8340, -2.4637),

    # Murcia
    "Murcia":       (37.9922, -1.1307),
}

# ─────────────────────────────────────────────
#   VECINDADES REALES ENTRE PROVINCIAS
#   (basadas en la geografía española)
# ─────────────────────────────────────────────

vecindades = {
    "Zaragoza":     ["Huesca", "Teruel", "Lleida", "Tarragona", "Guadalajara",
                     "Soria", "Logrono", "Navarra_via_Pamplona", "Pamplona"],
    "Huesca":       ["Zaragoza", "Lleida", "Pamplona"],
    "Teruel":       ["Zaragoza", "Cuenca", "Valencia", "Castellon", "Lleida"],
    "Barcelona":    ["Girona", "Lleida", "Tarragona"],
    "Girona":       ["Barcelona", "Lleida"],
    "Lleida":       ["Huesca", "Zaragoza", "Tarragona", "Barcelona", "Girona", "Teruel"],
    "Tarragona":    ["Lleida", "Barcelona", "Zaragoza", "Castellon"],
    "Valencia":     ["Castellon", "Teruel", "Cuenca", "Albacete", "Alicante"],
    "Castellon":    ["Tarragona", "Teruel", "Valencia"],
    "Alicante":     ["Valencia", "Albacete", "Murcia"],
    "Madrid":       ["Guadalajara", "Segovia", "Avila", "Toledo", "Cuenca"],
    "Guadalajara":  ["Zaragoza", "Soria", "Madrid", "Cuenca", "Segovia"],
    "Cuenca":       ["Guadalajara", "Teruel", "Valencia", "Albacete", "Toledo", "Madrid"],
    "Toledo":       ["Madrid", "Cuenca", "Ciudad_Real", "Avila", "Caceres"],
    "Ciudad_Real":  ["Toledo", "Cuenca", "Albacete", "Cordoba", "Badajoz", "Caceres"],
    "Albacete":     ["Cuenca", "Valencia", "Alicante", "Murcia", "Jaen", "Ciudad_Real"],
    "Soria":        ["Zaragoza", "Logrono", "Burgos", "Segovia", "Guadalajara"],
    "Segovia":      ["Soria", "Burgos", "Valladolid", "Avila", "Madrid", "Guadalajara"],
    "Avila":        ["Segovia", "Valladolid", "Salamanca", "Caceres", "Toledo", "Madrid"],
    "Salamanca":    ["Zamora", "Valladolid", "Avila", "Caceres"],
    "Zamora":       ["Leon", "Valladolid", "Salamanca", "Ourense"],
    "Valladolid":   ["Palencia", "Burgos", "Soria", "Segovia", "Avila", "Zamora", "Salamanca"],
    "Palencia":     ["Leon", "Burgos", "Valladolid"],
    "Leon":         ["Oviedo", "Lugo", "Ourense", "Zamora", "Palencia", "Burgos", "Santander"],
    "Burgos":       ["Santander", "Bilbao", "Vitoria", "Logrono", "Soria",
                     "Valladolid", "Palencia", "Leon"],
    "Logrono":      ["Zaragoza", "Pamplona", "Vitoria", "Burgos", "Soria"],
    "Pamplona":     ["Huesca", "Zaragoza", "Logrono", "San_Sebastian", "Vitoria"],
    "Bilbao":       ["Santander", "Burgos", "Vitoria", "San_Sebastian"],
    "San_Sebastian":["Pamplona", "Bilbao"],
    "Vitoria":      ["Bilbao", "San_Sebastian", "Pamplona", "Logrono", "Burgos"],
    "Santander":    ["Bilbao", "Burgos", "Leon", "Oviedo"],
    "Oviedo":       ["Santander", "Leon", "Lugo"],
    "Lugo":         ["Oviedo", "Leon", "Ourense", "A_Coruna", "Pontevedra"],
    "Ourense":      ["Lugo", "Zamora", "Pontevedra", "A_Coruna"],
    "Pontevedra":   ["Lugo", "Ourense", "A_Coruna"],
    "A_Coruna":     ["Lugo", "Ourense", "Pontevedra"],
    "Caceres":      ["Salamanca", "Avila", "Toledo", "Ciudad_Real", "Badajoz"],
    "Badajoz":      ["Caceres", "Ciudad_Real", "Cordoba", "Huelva", "Sevilla"],
    "Huelva":       ["Badajoz", "Sevilla"],
    "Sevilla":      ["Huelva", "Badajoz", "Cordoba", "Malaga", "Cadiz"],
    "Cadiz":        ["Sevilla", "Malaga"],
    "Malaga":       ["Cadiz", "Sevilla", "Cordoba", "Granada"],
    "Cordoba":      ["Badajoz", "Ciudad_Real", "Albacete", "Jaen", "Sevilla", "Malaga"],
    "Jaen":         ["Cordoba", "Albacete", "Granada", "Ciudad_Real"],
    "Granada":      ["Jaen", "Malaga", "Almeria"],
    "Almeria":      ["Granada", "Murcia"],
    "Murcia":       ["Albacete", "Alicante", "Almeria"],
}


# ─────────────────────────────────────────────
#   FUNCIONES DE DISTANCIA Y GRAFO
# ─────────────────────────────────────────────

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


class Grafo:
    def __init__(self):
        self.adyacencia = {}

    def agregar_ciudad(self, ciudad):
        if ciudad not in self.adyacencia:
            self.adyacencia[ciudad] = []

    def agregar_conexion(self, origen, destino, distancia):
        self.agregar_ciudad(origen)
        self.agregar_ciudad(destino)
        self.adyacencia[origen].append((destino, round(distancia)))

    def obtener_vecinos(self, ciudad):
        return self.adyacencia.get(ciudad, [])

    def __str__(self):
        return str(self.adyacencia)


def construir_grafo_peninsula():
    """
    Construye un grafo dirigido con todas las provincias peninsulares.
    Las conexiones se basan en vecindades reales y el peso es la
    distancia geodésica entre capitales de provincia.
    """
    g = Grafo()

    for origen, vecinos in vecindades.items():
        if origen not in provincias_peninsula:
            continue
        for destino in vecinos:
            if destino not in provincias_peninsula:
                continue
            dist = distancia_geo(
                provincias_peninsula[origen],
                provincias_peninsula[destino]
            )
            g.agregar_conexion(origen, destino, dist)

    return g


# ─────────────────────────────────────────────
#   ALGORITMO DIJKSTRA
# ─────────────────────────────────────────────

def dijkstra(grafo, origen):
    """
    Calcula la distancia mínima desde 'origen' a todos los nodos.
    Retorna:
        distancias: {ciudad: distancia_minima}
        previos:    {ciudad: nodo_anterior}
    """
    distancias = {ciudad: float('inf') for ciudad in grafo.adyacencia}
    distancias[origen] = 0
    previos = {ciudad: None for ciudad in grafo.adyacencia}
    cola = [(0, origen)]

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
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = previos[actual]
    camino.reverse()
    return camino


# ─────────────────────────────────────────────
#   CÁLCULO DE ENERGÍA Y COSTE
# ─────────────────────────────────────────────

def calcular_energia(distancia_total, energia_inicial, perdida_por_km):
    """Energía restante tras recorrer la distancia con pérdidas constantes."""
    energia_final = energia_inicial - (distancia_total * perdida_por_km)
    return max(energia_final, 0)


def calcular_coste(distancia_km, coste_por_km=500_000):
    """
    Coste estimado de construcción de la línea de alta tensión.
    Referencia orientativa: ~500.000 €/km para líneas de 400 kV.
    """
    return distancia_km * coste_por_km


# ─────────────────────────────────────────────
#   SIMULACIÓN Y RESULTADOS
# ─────────────────────────────────────────────

def ejecutar_simulacion(grafo, origen, energia_inicial, perdida_por_km):
    distancias, previos = dijkstra(grafo, origen)
    resultados = []

    for ciudad, distancia in distancias.items():
        camino = reconstruir_camino(previos, ciudad)
        energia_final = calcular_energia(distancia, energia_inicial, perdida_por_km)
        coste = calcular_coste(distancia)
        resultados.append({
            "ciudad":        ciudad,
            "distancia":     distancia,
            "camino":        camino,
            "energia_final": energia_final,
            "coste":         coste,
        })

    return resultados


def imprimir_tabla_resultados(resultados):
    print("\n" + "=" * 80)
    print(" RESULTADOS DE LA SIMULACIÓN – RED ELÉCTRICA PENINSULAR")
    print("=" * 80)
    print(f"{'Ciudad':20} {'Distancia (km)':16} {'Energía final (MWh)':22} {'Coste línea (€)':20}")
    print("-" * 80)

    for r in sorted(resultados, key=lambda x: x["distancia"]):
        if r["distancia"] == float("inf"):
            continue
        print(f"{r['ciudad']:20} {r['distancia']:16.0f} {r['energia_final']:22.2f} {r['coste']:>20,.0f}")
    print()


def analizar_destino(resultados, origen, destino):
    """
    Muestra el análisis completo de la ruta óptima desde origen hasta destino:
    distancia, energía que llega, coste estimado y camino paso a paso.
    """
    dato = next((r for r in resultados if r["ciudad"] == destino), None)

    if dato is None or dato["distancia"] == float("inf"):
        print(f"\n No hay ruta disponible desde {origen} hasta {destino}.")
        return None

    camino_str = " → ".join(dato["camino"])

    print("\n" + "=" * 60)
    print(f" ANÁLISIS DE RUTA: {origen} → {destino}")
    print("=" * 60)
    print(f"  Distancia total:          {dato['distancia']:.0f} km")
    print(f"  Energía que llega:        {dato['energia_final']:.2f} MWh")
    print(f"  Coste estimado de línea:  {dato['coste']:,.0f} €")
    print(f"  Nodos intermedios:        {len(dato['camino']) - 2}")
    print(f"\n  Ruta óptima:")
    print(f"    {camino_str}\n")

    return dato


# ─────────────────────────────────────────────
#   VISUALIZACIÓN
# ─────────────────────────────────────────────

def construir_grafo_networkx(grafo):
    G = nx.DiGraph()
    for origen, vecinos in grafo.adyacencia.items():
        for destino, distancia in vecinos:
            G.add_edge(origen, destino, weight=distancia)
    return G


def dibujar_grafo_general(grafo, resultados):
    """Dibuja toda la red con los nodos coloreados según la energía recibida,
    mostrando los km en cada arista y la energía acumulada en cada nodo."""
    G = construir_grafo_networkx(grafo)

    # Posiciones geográficas reales (lon, lat) → (x, y)
    pos = {ciudad: (coord[1], coord[0])
           for ciudad, coord in provincias_peninsula.items()
           if ciudad in G.nodes()}

    energia_por_ciudad = {r["ciudad"]: r["energia_final"] for r in resultados}
    energias = [energia_por_ciudad.get(n, 0) for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(18, 11))

    nodos = nx.draw_networkx_nodes(
        G, pos, node_size=500,
        node_color=energias, cmap=plt.cm.RdYlGn,
        ax=ax
    )

    # Etiquetas de nodo: nombre + energía acumulada
    etiquetas_nodos = {
        n: f"{n}\n{energia_por_ciudad.get(n, 0):.0f} MWh"
        for n in G.nodes()
    }
    nx.draw_networkx_labels(G, pos, labels=etiquetas_nodos, font_size=5.5, ax=ax)

    nx.draw_networkx_edges(
        G, pos, arrowstyle="->", arrowsize=8,
        edge_color="#aaaaaa", width=0.6, ax=ax
    )

    # Etiquetas de aristas: distancia en km
    edge_labels = {(u, v): f"{d['weight']} km"
                   for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels,
        font_size=4.5, label_pos=0.3,
        bbox=dict(boxstyle="round,pad=0.1", fc="white", alpha=0.5),
        ax=ax
    )

    cbar = fig.colorbar(nodos, ax=ax, shrink=0.7)
    cbar.set_label("Energía final aproximada (MWh)")
    ax.set_title("Red de distribución eléctrica peninsular – km por tramo · MWh en cada provincia")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


def dibujar_camino_optimo(grafo, resultados, destino, origen="Zaragoza"):
    """Dibuja la red resaltando la ruta óptima hacia el destino indicado,
    mostrando los km en cada arista y la energía acumulada en cada nodo del camino."""
    G = construir_grafo_networkx(grafo)

    pos = {ciudad: (coord[1], coord[0])
           for ciudad, coord in provincias_peninsula.items()
           if ciudad in G.nodes()}

    dato = next((r for r in resultados if r["ciudad"] == destino), None)
    if dato is None:
        print("Ciudad no encontrada en resultados.")
        return

    camino = dato["camino"]
    aristas_camino = list(zip(camino[:-1], camino[1:]))
    nodos_camino = set(camino)

    energia_por_ciudad = {r["ciudad"]: r["energia_final"] for r in resultados}

    fig, ax = plt.subplots(figsize=(18, 11))

    # Todos los nodos en gris
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[n for n in G.nodes() if n not in nodos_camino],
        node_size=200, node_color="#cccccc", ax=ax
    )
    # Nodos del camino en naranja
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[n for n in nodos_camino if n != origen and n != destino],
        node_size=500, node_color="#ff8c00", ax=ax
    )
    # Origen en verde, destino en rojo
    nx.draw_networkx_nodes(G, pos, nodelist=[origen],
                           node_size=600, node_color="green", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=[destino],
                           node_size=600, node_color="red", ax=ax)

    # Etiquetas: nombre + MWh solo para nodos del camino
    etiquetas_camino = {
        n: f"{n}\n{energia_por_ciudad.get(n, 0):.0f} MWh"
        for n in nodos_camino
    }
    etiquetas_resto = {n: n for n in G.nodes() if n not in nodos_camino}

    nx.draw_networkx_labels(G, pos, labels=etiquetas_resto, font_size=5.5, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=etiquetas_camino,
                            font_size=6.5, font_weight="bold", ax=ax)

    # Aristas normales
    nx.draw_networkx_edges(
        G, pos, arrowstyle="->", arrowsize=8,
        edge_color="#dddddd", width=0.5, ax=ax
    )
    # Aristas del camino en rojo
    nx.draw_networkx_edges(
        G, pos, edgelist=aristas_camino,
        edge_color="red", width=2.5,
        arrowstyle="->", arrowsize=15, ax=ax
    )

    # Km solo en las aristas del camino óptimo
    edge_labels_camino = {
        (u, v): f"{G[u][v]['weight']} km"
        for u, v in aristas_camino
    }
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels_camino,
        font_size=7, font_color="darkred", label_pos=0.4,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8),
        ax=ax
    )

    ax.set_title(f"Ruta óptima: {origen} → {destino}  |  "
                 f"{dato['distancia']:.0f} km  ·  "
                 f"{dato['energia_final']:.1f} MWh  ·  "
                 f"{dato['coste']:,.0f} €")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
#   MAIN
# ─────────────────────────────────────────────

ENERGIA_INICIAL  = 1000   # MWh en origen
PERDIDA_POR_KM   = 0.15   # MWh/km
ORIGEN           = "Zaragoza"


def main():
    grafo = construir_grafo_peninsula()

    print("\n Red eléctrica peninsular cargada con", len(grafo.adyacencia), "provincias.")

    # Ejecutar Dijkstra desde Zaragoza una sola vez
    resultados = ejecutar_simulacion(grafo, ORIGEN, ENERGIA_INICIAL, PERDIDA_POR_KM)

    # Mostrar tabla completa
    imprimir_tabla_resultados(resultados)

    # El usuario elige el destino que le interesa
    print("Provincias disponibles:")
    disponibles = sorted(
        r["ciudad"] for r in resultados
        if r["distancia"] not in (0, float("inf"))
    )
    print(", ".join(disponibles))

    destino = input("\n¿Hasta qué provincia quieres analizar la ruta? ").strip()

    if destino not in grafo.adyacencia:
        print(f"'{destino}' no está en el grafo. Comprueba el nombre exacto.")
        return

    # Análisis detallado de esa ruta
    dato = analizar_destino(resultados, ORIGEN, destino)

    if dato:
        # Visualizaciones
        dibujar_grafo_general(grafo, resultados)
        dibujar_camino_optimo(grafo, resultados, destino)


if __name__ == "__main__":
    main()
