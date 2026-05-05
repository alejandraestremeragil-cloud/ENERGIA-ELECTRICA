import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import csv
import os

# =============================================================================
#   RED DE DISTRIBUCIÓN ELÉCTRICA – ARAGÓN Y PENÍNSULA IBÉRICA
#   Algoritmo: Dijkstra (rutas de menor pérdida energética)
#   Incluye: modo fallo aleatorio, exportación CSV, input de ciudad destino
# =============================================================================

MENSAJE_CIERZO = """
╔══════════════════════════════════════════════════════════════════════════════╗
║         RED DE DISTRIBUCIÓN ELÉCTRICA – ZARAGOZA COMO NODO CENTRAL           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Zaragoza se sitúa en el Valle del Ebro, donde el CIERZO —un viento fuerte   ║
║  y constante del noroeste— convierte a Aragón en uno de los territorios con  ║
║  mayor potencial eólico de España.                                           ║
║                                                                              ║
║  Gracias a esta ventaja geográfica, Aragón genera más electricidad de la     ║
║  que consume, exportando el excedente a otras regiones. Zaragoza actúa como  ║
║  nodo central de distribución por su posición estratégica: equidistante de   ║
║  Madrid, Barcelona, Valencia, Bilbao y San Sebastián, y conectada con las    ║
║  capitales aragonesas de Huesca y Teruel.                                    ║
║                                                                              ║
║  Este programa simula esa red usando un GRAFO DIRIGIDO Y PONDERADO donde     ║
║  cada arista representa una línea de alta tensión. El algoritmo de DIJKSTRA  ║
║  calcula la ruta de menor pérdida energética desde Zaragoza hasta cualquier  ║
║  provincia peninsular.                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
#   BASE DE DATOS: COORDENADAS DE LAS 47 PROVINCIAS PENINSULARES
# ─────────────────────────────────────────────────────────────────────────────

coordenadas = {
    "Zaragoza":      (41.6488, -0.8891),
    "Huesca":        (42.1401, -0.4089),
    "Teruel":        (40.3456, -1.1065),
    "Barcelona":     (41.3874,  2.1686),
    "Girona":        (41.9794,  2.8214),
    "Lleida":        (41.6176,  0.6200),
    "Tarragona":     (41.1189,  1.2445),
    "Valencia":      (39.4699, -0.3763),
    "Castellon":     (39.9864, -0.0513),
    "Alicante":      (38.3452, -0.4810),
    "Madrid":        (40.4168, -3.7038),
    "Guadalajara":   (40.6334, -3.1674),
    "Cuenca":        (40.0704, -2.1374),
    "Toledo":        (39.8628, -4.0273),
    "Ciudad_Real":   (38.9848, -3.9274),
    "Albacete":      (38.9943, -1.8585),
    "Soria":         (41.7640, -2.4650),
    "Segovia":       (40.9429, -4.1088),
    "Avila":         (40.6567, -4.6976),
    "Salamanca":     (40.9701, -5.6635),
    "Zamora":        (41.5034, -5.7447),
    "Valladolid":    (41.6523, -4.7245),
    "Palencia":      (42.0097, -4.5288),
    "Leon":          (42.5987, -5.5671),
    "Burgos":        (42.3439, -3.6970),
    "Logrono":       (42.4627, -2.4449),
    "Pamplona":      (42.8125, -1.6458),
    "Bilbao":        (43.2630, -2.9350),
    "San_Sebastian": (43.3183, -1.9812),
    "Vitoria":       (42.8467, -2.6727),
    "Santander":     (43.4623, -3.8099),
    "Oviedo":        (43.3614, -5.8593),
    "Lugo":          (43.0097, -7.5560),
    "Ourense":       (42.3354, -7.8639),
    "Pontevedra":    (42.4336, -8.6488),
    "A_Coruna":      (43.3623, -8.4115),
    "Caceres":       (39.4753, -6.3724),
    "Badajoz":       (38.8794, -6.9706),
    "Huelva":        (37.2614, -6.9447),
    "Sevilla":       (37.3891, -5.9845),
    "Cadiz":         (36.5271, -6.2886),
    "Malaga":        (36.7213, -4.4214),
    "Cordoba":       (37.8882, -4.7794),
    "Jaen":          (37.7796, -3.7849),
    "Granada":       (37.1773, -3.5986),
    "Almeria":       (36.8340, -2.4637),
    "Murcia":        (37.9922, -1.1307),
}

# ─────────────────────────────────────────────────────────────────────────────
#   VECINDADES REALES (conexiones entre provincias limítrofes)
# ─────────────────────────────────────────────────────────────────────────────

vecindades = {
    "Zaragoza":    ["Huesca","Teruel","Lleida","Tarragona","Guadalajara",
                    "Soria","Logrono","Pamplona","San_Sebastian"],
    "Huesca":      ["Zaragoza","Lleida","Pamplona"],
    "Teruel":      ["Zaragoza","Cuenca","Valencia","Castellon","Lleida"],
    "Barcelona":   ["Girona","Lleida","Tarragona"],
    "Girona":      ["Barcelona","Lleida"],
    "Lleida":      ["Huesca","Zaragoza","Tarragona","Barcelona","Girona","Teruel"],
    "Tarragona":   ["Lleida","Barcelona","Zaragoza","Castellon"],
    "Valencia":    ["Castellon","Teruel","Cuenca","Albacete","Alicante"],
    "Castellon":   ["Tarragona","Teruel","Valencia"],
    "Alicante":    ["Valencia","Albacete","Murcia"],
    "Madrid":      ["Guadalajara","Segovia","Avila","Toledo","Cuenca"],
    "Guadalajara": ["Zaragoza","Soria","Madrid","Cuenca","Segovia"],
    "Cuenca":      ["Guadalajara","Teruel","Valencia","Albacete","Toledo","Madrid"],
    "Toledo":      ["Madrid","Cuenca","Ciudad_Real","Avila","Caceres"],
    "Ciudad_Real": ["Toledo","Cuenca","Albacete","Cordoba","Badajoz","Caceres"],
    "Albacete":    ["Cuenca","Valencia","Alicante","Murcia","Jaen","Ciudad_Real"],
    "Soria":       ["Zaragoza","Logrono","Burgos","Segovia","Guadalajara"],
    "Segovia":     ["Soria","Burgos","Valladolid","Avila","Madrid","Guadalajara"],
    "Avila":       ["Segovia","Valladolid","Salamanca","Caceres","Toledo","Madrid"],
    "Salamanca":   ["Zamora","Valladolid","Avila","Caceres"],
    "Zamora":      ["Leon","Valladolid","Salamanca","Ourense"],
    "Valladolid":  ["Palencia","Burgos","Soria","Segovia","Avila","Zamora","Salamanca"],
    "Palencia":    ["Leon","Burgos","Valladolid"],
    "Leon":        ["Oviedo","Lugo","Ourense","Zamora","Palencia","Burgos","Santander"],
    "Burgos":      ["Santander","Bilbao","Vitoria","Logrono","Soria",
                    "Valladolid","Palencia","Leon"],
    "Logrono":     ["Zaragoza","Pamplona","Vitoria","Burgos","Soria"],
    "Pamplona":    ["Huesca","Zaragoza","Logrono","San_Sebastian","Vitoria"],
    "Bilbao":      ["Santander","Burgos","Vitoria","San_Sebastian"],
    "San_Sebastian":["Pamplona","Bilbao","Zaragoza"],
    "Vitoria":     ["Bilbao","San_Sebastian","Pamplona","Logrono","Burgos"],
    "Santander":   ["Bilbao","Burgos","Leon","Oviedo"],
    "Oviedo":      ["Santander","Leon","Lugo"],
    "Lugo":        ["Oviedo","Leon","Ourense","A_Coruna","Pontevedra"],
    "Ourense":     ["Lugo","Zamora","Pontevedra","A_Coruna"],
    "Pontevedra":  ["Lugo","Ourense","A_Coruna"],
    "A_Coruna":    ["Lugo","Ourense","Pontevedra"],
    "Caceres":     ["Salamanca","Avila","Toledo","Ciudad_Real","Badajoz"],
    "Badajoz":     ["Caceres","Ciudad_Real","Cordoba","Huelva","Sevilla"],
    "Huelva":      ["Badajoz","Sevilla"],
    "Sevilla":     ["Huelva","Badajoz","Cordoba","Malaga","Cadiz"],
    "Cadiz":       ["Sevilla","Malaga"],
    "Malaga":      ["Cadiz","Sevilla","Cordoba","Granada"],
    "Cordoba":     ["Badajoz","Ciudad_Real","Albacete","Jaen","Sevilla","Malaga"],
    "Jaen":        ["Cordoba","Albacete","Granada","Ciudad_Real"],
    "Granada":     ["Jaen","Malaga","Almeria"],
    "Almeria":     ["Granada","Murcia"],
    "Murcia":      ["Albacete","Alicante","Almeria"],
}

# ─────────────────────────────────────────────────────────────────────────────
#   PARÁMETROS ENERGÉTICOS
#   Pérdida: 4% de la energía inicial por cada 100 km recorridos.
#   Referencia orientativa para líneas de alta tensión de 400 kV.
# ─────────────────────────────────────────────────────────────────────────────

ENERGIA_INICIAL    = 1000.0   # MWh disponibles en Zaragoza
PERDIDA_CADA_100KM = 4.0      # % de ENERGIA_INICIAL perdido por cada 100 km
COSTE_POR_KM       = 500_000  # € por km de línea de alta tensión (ref. orientativa)
ORIGEN = "Zaragoza"


def distancia_geo(c1, c2):
    """Distancia geodésica en km entre dos pares (lat, lon)."""
    R = 6371
    lat1, lon1 = c1; lat2, lon2 = c2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def calcular_energia_final(distancia_km):
    """E_final = E_inicial − (dist/100) × (P%/100) × E_inicial"""
    perdida = (distancia_km / 100.0) * (PERDIDA_CADA_100KM / 100.0) * ENERGIA_INICIAL
    return max(ENERGIA_INICIAL - perdida, 0.0)


def calcular_coste(distancia_km):
    return distancia_km * COSTE_POR_KM


# ─────────────────────────────────────────────────────────────────────────────
#   CLASE GRAFO
# ─────────────────────────────────────────────────────────────────────────────

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

    def eliminar_conexion(self, origen, destino):
        if origen in self.adyacencia:
            self.adyacencia[origen] = [
                (v, p) for v, p in self.adyacencia[origen] if v != destino
            ]

    def obtener_vecinos(self, ciudad):
        return self.adyacencia.get(ciudad, [])

    def listar_conexiones(self):
        return [(o, d, p) for o, vs in self.adyacencia.items() for d, p in vs]


def construir_grafo():
    g = Grafo()
    for origen, vecinos in vecindades.items():
        if origen not in coordenadas:
            continue
        for destino in vecinos:
            if destino not in coordenadas:
                continue
            dist = distancia_geo(coordenadas[origen], coordenadas[destino])
            g.agregar_conexion(origen, destino, dist)
    return g


# ─────────────────────────────────────────────────────────────────────────────
#   DIJKSTRA
# ─────────────────────────────────────────────────────────────────────────────

def dijkstra(grafo, origen):
    """
    Calcula la ruta de menor distancia acumulada (= menor pérdida energética)
    desde 'origen' a todos los nodos alcanzables, usando un min-heap.

    Retorna:
        distancias: {ciudad: km_mínimos}
        previos:    {ciudad: nodo_anterior}
    """
    distancias = {c: float('inf') for c in grafo.adyacencia}
    distancias[origen] = 0
    previos = {c: None for c in grafo.adyacencia}
    cola = [(0, origen)]

    while cola:
        dist_actual, actual = heapq.heappop(cola)
        if dist_actual > distancias[actual]:
            continue
        for vecino, peso in grafo.obtener_vecinos(actual):
            nueva = dist_actual + peso
            if nueva < distancias[vecino]:
                distancias[vecino] = nueva
                previos[vecino] = actual
                heapq.heappush(cola, (nueva, vecino))

    return distancias, previos


def reconstruir_camino(previos, destino):
    camino, actual = [], destino
    while actual is not None:
        camino.append(actual)
        actual = previos[actual]
    camino.reverse()
    return camino


# ─────────────────────────────────────────────────────────────────────────────
#   SIMULACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def ejecutar_simulacion(grafo):
    distancias, previos = dijkstra(grafo, ORIGEN)
    resultados = []
    for ciudad in grafo.adyacencia:
        dist   = distancias[ciudad]
        camino = reconstruir_camino(previos, ciudad)
        energia = calcular_energia_final(dist) if dist != float('inf') else 0.0
        coste   = calcular_coste(dist)         if dist != float('inf') else 0.0
        resultados.append({
            "ciudad":    ciudad,
            "distancia": dist,
            "energia":   energia,
            "coste":     coste,
            "camino":    camino,
            "saltos":    len(camino) - 1,
        })
    return resultados


def imprimir_resultados(resultados, titulo="SITUACIÓN NORMAL"):
    print(f"\n{'='*72}")
    print(f"  {titulo}")
    print(f"  Pérdida: {PERDIDA_CADA_100KM}% de {ENERGIA_INICIAL:.0f} MWh por cada 100 km")
    print(f"{'='*72}")
    print(f"  {'Provincia':18} {'Dist (km)':>10} {'Energía (MWh)':>14} {'Coste línea (€)':>18}  Ruta")
    print(f"  {'-'*70}")
    for r in sorted(resultados, key=lambda x: x["distancia"]):
        if r["distancia"] == 0:
            continue
        if r["distancia"] == float('inf'):
            print(f"  {r['ciudad']:18} {'SIN RUTA':>10} {'0.0':>14} {'-':>18}")
            continue
        ruta = " → ".join(r["camino"])
        print(f"  {r['ciudad']:18} {r['distancia']:>10.0f} "
              f"{r['energia']:>14.1f} "
              f"{r['coste']:>18,.0f}  {ruta}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
#   EXPORTACIÓN A CSV
# ─────────────────────────────────────────────────────────────────────────────

def exportar_csv(resultados_normal, resultados_fallo, fallo, ruta_archivo="red_electrica.csv"):
    """
    Guarda en un CSV todas las provincias con:
      - Distancia y energía en situación normal
      - Distancia y energía tras el fallo
      - Diferencias y ruta óptima en cada caso
    """
    origen_f, destino_f, km_f = fallo
    norm_d  = {r["ciudad"]: r for r in resultados_normal}
    fallo_d = {r["ciudad"]: r for r in resultados_fallo}

    with open(ruta_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Cabecera informativa
        writer.writerow(["RED DE DISTRIBUCIÓN ELÉCTRICA – SIMULACIÓN DIJKSTRA"])
        writer.writerow([f"Nodo origen: {ORIGEN}"])
        writer.writerow([f"Energía inicial: {ENERGIA_INICIAL} MWh"])
        writer.writerow([f"Pérdida energética: {PERDIDA_CADA_100KM}% por cada 100 km"])
        writer.writerow([f"Línea en fallo simulado: {origen_f} → {destino_f} ({km_f} km)"])
        writer.writerow([])

        # Cabecera de datos
        writer.writerow([
            "Provincia",
            "Dist. normal (km)", "Energía normal (MWh)", "Coste línea (€)", "Saltos normal", "Ruta normal",
            "Dist. fallo (km)",  "Energía fallo (MWh)",  "Saltos fallo",    "Ruta fallo",
            "Δ Distancia (km)",  "Δ Energía (MWh)",      "Estado tras fallo"
        ])

        for ciudad in sorted(norm_d.keys()):
            if ciudad == ORIGEN:
                continue
            rn = norm_d[ciudad]
            rf = fallo_d.get(ciudad, rn)

            dist_n   = rn["distancia"]
            dist_f   = rf["distancia"]
            en_n     = rn["energia"]
            en_f     = rf["energia"]
            delta_km = (dist_f - dist_n) if dist_f != float('inf') else "—"
            delta_en = (en_n - en_f)     if dist_f != float('inf') else "—"

            if dist_f == float('inf'):
                estado = "SIN SUMINISTRO"
            elif isinstance(delta_km, float) and delta_km > 0:
                estado = "Ruta alternativa"
            else:
                estado = "Sin cambios"

            writer.writerow([
                ciudad,
                f"{dist_n:.0f}" if dist_n != float('inf') else "SIN RUTA",
                f"{en_n:.1f}"   if dist_n != float('inf') else "0",
                f"{rn['coste']:,.0f}" if dist_n != float('inf') else "0",
                rn["saltos"],
                " → ".join(rn["camino"]),
                f"{dist_f:.0f}" if dist_f != float('inf') else "SIN RUTA",
                f"{en_f:.1f}"   if dist_f != float('inf') else "0",
                rf["saltos"],
                " → ".join(rf["camino"]),
                f"{delta_km:.0f}" if isinstance(delta_km, float) else delta_km,
                f"{delta_en:.1f}" if isinstance(delta_en, float) else delta_en,
                estado,
            ])

    print(f"  ✓  Datos exportados a: {os.path.abspath(ruta_archivo)}\n")


# ─────────────────────────────────────────────────────────────────────────────
#   MODO FALLO ALEATORIO
# ─────────────────────────────────────────────────────────────────────────────

def simular_fallo_aleatorio(grafo):
    aristas = grafo.listar_conexiones()
    fallo   = random.choice(aristas)
    grafo.eliminar_conexion(fallo[0], fallo[1])
    return fallo


def analizar_impacto_fallo(res_normal, res_fallo, fallo):
    origen_f, destino_f, km_f = fallo
    print(f"\n{'='*72}")
    print(f"  ⚡ FALLO ALEATORIO SIMULADO")
    print(f"  Línea cortada: {origen_f} → {destino_f}  ({km_f} km)")
    print(f"{'='*72}")

    norm_d  = {r["ciudad"]: r for r in res_normal}
    fallo_d = {r["ciudad"]: r for r in res_fallo}

    sin_sum = []
    alternativas = []

    for ciudad, rf in fallo_d.items():
        if ciudad == ORIGEN:
            continue
        rn = norm_d[ciudad]
        if rf["distancia"] == float('inf'):
            sin_sum.append(ciudad)
        elif rf["distancia"] > rn["distancia"]:
            alternativas.append((ciudad, rf,
                                 rf["distancia"] - rn["distancia"],
                                 rn["energia"]   - rf["energia"]))

    if sin_sum:
        print(f"\n  ⚠  Provincias SIN SUMINISTRO:")
        for c in sin_sum:
            print(f"       • {c}")
    else:
        print(f"\n  ✓  Todas las provincias conservan ruta alternativa.")

    if alternativas:
        print(f"\n  Provincias con ruta alternativa (mayor pérdida):")
        print(f"  {'Provincia':18} {'Dist. nueva':>11} {'Energía':>10} {'Δ km':>8} {'Δ pérdida':>11}")
        print(f"  {'-'*62}")
        for ciudad, rf, aum, perd in sorted(alternativas, key=lambda x: -x[2]):
            ruta = " → ".join(rf["camino"])
            print(f"  {ciudad:18} {rf['distancia']:>8.0f} km "
                  f"{rf['energia']:>8.1f} MWh "
                  f"{aum:>+7.0f} km  {perd:>+9.1f} MWh")
            print(f"    Ruta alternativa: {ruta}")
    else:
        print(f"\n  Ninguna provincia ve empeorada su ruta.")
    print()


# ─────────────────────────────────────────────────────────────────────────────
#   VISUALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def _pos():
    return {c: (coord[1], coord[0]) for c, coord in coordenadas.items()}


def _nx(grafo):
    G = nx.DiGraph()
    for o, vs in grafo.adyacencia.items():
        for d, p in vs:
            G.add_edge(o, d, weight=p)
    return G


def _dibujar(ax, G, G_ref, pos, e_dict, sin_sum, titulo, arista_fallo=None):
    nodos_ok  = [n for n in G.nodes() if n not in sin_sum]
    nodos_sin = list(sin_sum)
    vals = [e_dict.get(n, ENERGIA_INICIAL) for n in nodos_ok]

    sc = nx.draw_networkx_nodes(G, pos, nodelist=nodos_ok,
                                node_size=500, node_color=vals,
                                cmap=plt.cm.RdYlGn,
                                vmin=0, vmax=ENERGIA_INICIAL, ax=ax)
    if nodos_sin:
        nx.draw_networkx_nodes(G, pos, nodelist=nodos_sin,
                               node_size=500, node_color="black", ax=ax)

    for n in G.nodes():
        color = "white" if n in sin_sum else "black"
        label = (f"{n}\nSIN SUMINISTRO" if n in sin_sum
                 else f"{n}\n{e_dict.get(n, ENERGIA_INICIAL):.0f} MWh")
        nx.draw_networkx_labels(G, pos, labels={n: label},
                                font_size=5.5, font_weight="bold",
                                font_color=color, ax=ax)

    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10,
                           edge_color="#555555", width=0.7, ax=ax)

    edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=4.5, label_pos=0.35,
                                 bbox=dict(boxstyle="round,pad=0.1",
                                           fc="white", alpha=0.7),
                                 ax=ax)

    if arista_fallo and arista_fallo in G_ref.edges():
        nx.draw_networkx_edges(G_ref, pos, edgelist=[arista_fallo],
                               edge_color="red", width=2.5, style="dashed",
                               arrowstyle="->", arrowsize=15, ax=ax)

    ax.set_title(titulo, fontsize=9, fontweight="bold")
    ax.set_axis_off()
    return sc


def dibujar_red_normal(grafo, resultados):
    G, pos = _nx(grafo), _pos()
    e = {r["ciudad"]: r["energia"] for r in resultados}
    fig, ax = plt.subplots(figsize=(16, 10))
    sc = _dibujar(ax, G, G, pos, e, set(),
                  f"Red eléctrica peninsular – situación normal\n"
                  f"Pérdida: {PERDIDA_CADA_100KM}% por cada 100 km  |  "
                  f"Energía inicial en {ORIGEN}: {ENERGIA_INICIAL:.0f} MWh")
    fig.colorbar(sc, ax=ax, shrink=0.7).set_label("Energía recibida (MWh)")
    plt.tight_layout()
    plt.show()


def dibujar_comparacion_fallo(g_orig, g_fallo, res_norm, res_fallo, fallo):
    orig_f, dest_f, km_f = fallo
    pos    = _pos()
    G_orig = _nx(g_orig)
    G_fall = _nx(g_fallo)
    e_n    = {r["ciudad"]: r["energia"] for r in res_norm}
    e_f    = {r["ciudad"]: r["energia"] for r in res_fallo}
    sin_sum = {r["ciudad"] for r in res_fallo
               if r["distancia"] == float('inf') and r["ciudad"] != ORIGEN}

    fig, axes = plt.subplots(1, 2, figsize=(26, 11))
    sc1 = _dibujar(axes[0], G_orig, G_orig, pos, e_n, set(), "Situación NORMAL")
    sc2 = _dibujar(axes[1], G_fall, G_orig, pos, e_f, sin_sum,
                   f"FALLO: {orig_f} → {dest_f} ({km_f} km) cortada",
                   arista_fallo=(orig_f, dest_f))
    for sc, ax in [(sc1, axes[0]), (sc2, axes[1])]:
        fig.colorbar(sc, ax=ax, shrink=0.7).set_label("Energía recibida (MWh)")
    plt.suptitle("Red eléctrica peninsular: normal vs. fallo de línea",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def dibujar_ruta_destino(grafo, resultados, destino):
    """Resalta la ruta óptima desde Zaragoza hasta el destino elegido."""
    G, pos = _nx(grafo), _pos()
    dato = next((r for r in resultados if r["ciudad"] == destino), None)
    if dato is None or dato["distancia"] == float('inf'):
        print(f"  No hay ruta disponible hasta {destino}.")
        return

    camino = dato["camino"]
    aristas_camino = list(zip(camino[:-1], camino[1:]))
    nodos_camino   = set(camino)
    e_dict = {r["ciudad"]: r["energia"] for r in resultados}

    fig, ax = plt.subplots(figsize=(16, 10))

    # Nodos fuera del camino
    nx.draw_networkx_nodes(G, pos,
                           nodelist=[n for n in G.nodes() if n not in nodos_camino],
                           node_size=300, node_color="#cccccc", ax=ax)
    # Nodos del camino
    nx.draw_networkx_nodes(G, pos,
                           nodelist=[n for n in nodos_camino if n not in (ORIGEN, destino)],
                           node_size=550, node_color="#ff8c00", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=[ORIGEN],
                           node_size=650, node_color="green", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=[destino],
                           node_size=650, node_color="red", ax=ax)

    # Etiquetas
    for n in G.nodes():
        bold = "bold" if n in nodos_camino else "normal"
        label = (f"{n}\n{e_dict.get(n, ENERGIA_INICIAL):.0f} MWh"
                 if n in nodos_camino else n)
        nx.draw_networkx_labels(G, pos, labels={n: label},
                                font_size=5.5 if n not in nodos_camino else 7,
                                font_weight=bold, ax=ax)

    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=8,
                           edge_color="#dddddd", width=0.5, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=aristas_camino,
                           edge_color="red", width=2.5,
                           arrowstyle="->", arrowsize=16, ax=ax)

    # Km solo en aristas del camino
    edge_labels_camino = {(u, v): f"{G[u][v]['weight']} km"
                          for u, v in aristas_camino}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_camino,
                                 font_size=7.5, font_color="darkred",
                                 label_pos=0.4,
                                 bbox=dict(boxstyle="round,pad=0.2",
                                           fc="white", alpha=0.85),
                                 ax=ax)

    ax.set_title(
        f"Ruta óptima: {ORIGEN} → {destino}\n"
        f"{dato['distancia']:.0f} km  ·  "
        f"{dato['energia']:.1f} MWh recibidos  ·  "
        f"{dato['coste']:,.0f} € coste estimado de línea  ·  "
        f"{dato['saltos']} salto(s)",
        fontsize=10, fontweight="bold"
    )
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
#   ANÁLISIS COMBINADO: RUTA ÓPTIMA + FALLO EN ESA RUTA + ALTERNATIVA
# ─────────────────────────────────────────────────────────────────────────────

def analizar_destino_con_fallo(grafo_original, destino):
    """
    Flujo principal centrado en un destino concreto:
      1. Calcula la ruta óptima hasta el destino (Dijkstra normal)
      2. Elige aleatoriamente un tramo de ESA ruta y lo rompe
      3. Recalcula Dijkstra sin ese tramo
      4. Muestra la comparación: ruta ideal vs. ruta alternativa tras avería
      5. Exporta el CSV con ambas situaciones
    """
    # ── Paso 1: ruta óptima sin averías ──────────────────────────────────────
    res_normal = ejecutar_simulacion(grafo_original)
    dato_normal = next((r for r in res_normal if r["ciudad"] == destino), None)

    if dato_normal is None or dato_normal["distancia"] == float('inf'):
        print(f"\n  No existe ruta desde {ORIGEN} hasta {destino}.")
        return

    camino_optimo = dato_normal["camino"]
    tramos_ruta   = list(zip(camino_optimo[:-1], camino_optimo[1:]))

    print(f"\n{'='*68}")
    print(f"  RUTA ÓPTIMA SIN AVERÍAS: {ORIGEN} → {destino}")
    print(f"{'='*68}")
    print(f"  Recorrido:          {' → '.join(camino_optimo)}")
    print(f"  Distancia total:    {dato_normal['distancia']:.0f} km")
    print(f"  Energía que llega:  {dato_normal['energia']:.1f} MWh")
    print(f"  Pérdida energética: {ENERGIA_INICIAL - dato_normal['energia']:.1f} MWh")
    print(f"  Saltos:             {dato_normal['saltos']}")

    # ── Paso 2: fallo aleatorio en un tramo de la ruta óptima ────────────────
    tramo_fallo = random.choice(tramos_ruta)
    origen_f, destino_f = tramo_fallo
    km_fallo = next(p for v, p in grafo_original.obtener_vecinos(origen_f)
                    if v == destino_f)

    print(f"\n{'='*68}")
    print(f"  ⚡ AVERÍA SIMULADA EN LA RUTA")
    print(f"  Tramo cortado: {origen_f} → {destino_f}  ({km_fallo} km)")
    print(f"  Este tramo forma parte del recorrido óptimo.")
    print(f"{'='*68}")

    # ── Paso 3: recalcular con la línea rota ─────────────────────────────────
    grafo_averia = construir_grafo()
    grafo_averia.eliminar_conexion(origen_f, destino_f)
    res_averia   = ejecutar_simulacion(grafo_averia)
    dato_averia  = next((r for r in res_averia if r["ciudad"] == destino), None)

    fallo = (origen_f, destino_f, km_fallo)

    # ── Paso 4: mostrar impacto ───────────────────────────────────────────────
    print(f"\n  RESULTADO TRAS LA AVERÍA:")
    if dato_averia is None or dato_averia["distancia"] == float('inf'):
        print(f"\n  ✗  {destino} queda SIN SUMINISTRO.")
        print(f"     No existe ninguna ruta alternativa con la línea cortada.")
    else:
        aumento_km   = dato_averia["distancia"] - dato_normal["distancia"]
        perdida_mwh  = dato_normal["energia"]   - dato_averia["energia"]
        print(f"\n  Ruta alternativa:   {' → '.join(dato_averia['camino'])}")
        print(f"  Distancia nueva:    {dato_averia['distancia']:.0f} km  "
              f"({aumento_km:+.0f} km respecto a la ruta óptima)")
        print(f"  Energía que llega:  {dato_averia['energia']:.1f} MWh  "
              f"({perdida_mwh:+.1f} MWh de pérdida adicional)")
        print(f"  Pérdida total:      {ENERGIA_INICIAL - dato_averia['energia']:.1f} MWh")
        print(f"  Saltos:             {dato_averia['saltos']}")

    # ── Paso 5: exportar CSV ──────────────────────────────────────────────────
    exportar_csv(res_normal, res_averia, fallo, "red_electrica.csv")

    # ── Paso 6: visualizaciones ───────────────────────────────────────────────
    # Mapa general con la ruta óptima resaltada
    dibujar_ruta_destino(grafo_original, res_normal, destino)

    # Comparación normal vs. avería centrada en el destino
    dibujar_comparacion_destino(grafo_original, grafo_averia,
                                 dato_normal, dato_averia,
                                 fallo, destino)


def dibujar_comparacion_destino(g_orig, g_averia,
                                 dato_normal, dato_averia,
                                 fallo, destino):
    """
    Dos mapas lado a lado mostrando únicamente las rutas relevantes:
      izquierda → ruta óptima normal
      derecha   → ruta alternativa tras la avería (o sin suministro)
    """
    origen_f, destino_f, km_f = fallo
    pos = _pos()
    G_orig   = _nx(g_orig)
    G_averia = _nx(g_averia)

    def _resaltar_camino(ax, G, G_ref, camino, titulo,
                         color_camino="red", arista_cortada=None):
        aristas_c  = list(zip(camino[:-1], camino[1:]))
        nodos_c    = set(camino)

        # Todos los nodos en gris
        nx.draw_networkx_nodes(G_ref, pos,
                               nodelist=[n for n in G_ref.nodes() if n not in nodos_c],
                               node_size=250, node_color="#dddddd", ax=ax)
        # Nodos del camino
        nx.draw_networkx_nodes(G_ref, pos,
                               nodelist=[n for n in nodos_c
                                         if n not in (ORIGEN, destino)],
                               node_size=500, node_color="#ff8c00", ax=ax)
        nx.draw_networkx_nodes(G_ref, pos, nodelist=[ORIGEN],
                               node_size=600, node_color="green", ax=ax)

        if destino in G_ref.nodes():
            color_dest = "black" if dato_averia is None else "red"
            nx.draw_networkx_nodes(G_ref, pos, nodelist=[destino],
                                   node_size=600, node_color=color_dest, ax=ax)

        # Etiquetas
        for n in G_ref.nodes():
            en_camino = n in nodos_c
            label = f"{n}\n{dato_normal['energia']:.0f} MWh" if n == destino and dato_averia is None else n
            if n == destino and dato_averia is not None:
                label = (f"{n}\n{dato_averia['energia']:.0f} MWh"
                         if ax.get_title().startswith("AVERÍA") or "alternativa" in ax.get_title().lower()
                         else f"{n}\n{dato_normal['energia']:.0f} MWh")
            nx.draw_networkx_labels(G_ref, pos, labels={n: label},
                                    font_size=5.5 if not en_camino else 7,
                                    font_weight="bold" if en_camino else "normal",
                                    ax=ax)

        # Todas las aristas en gris
        nx.draw_networkx_edges(G_ref, pos, arrowstyle="->", arrowsize=8,
                               edge_color="#dddddd", width=0.5, ax=ax)
        # Aristas del camino resaltadas
        if aristas_c:
            nx.draw_networkx_edges(G_ref, pos, edgelist=aristas_c,
                                   edge_color=color_camino, width=2.5,
                                   arrowstyle="->", arrowsize=16, ax=ax)

        # Tramo cortado en rojo discontinuo (solo en el mapa de avería)
        if arista_cortada and arista_cortada in G_orig.edges():
            nx.draw_networkx_edges(G_orig, pos, edgelist=[arista_cortada],
                                   edge_color="crimson", width=3, style="dashed",
                                   arrowstyle="->", arrowsize=18, ax=ax)

        # Km en las aristas del camino
        if aristas_c:
            ek = {(u, v): f"{G_ref[u][v]['weight']} km"
                  for u, v in aristas_c if G_ref.has_edge(u, v)}
            nx.draw_networkx_edge_labels(G_ref, pos, edge_labels=ek,
                                         font_size=7, font_color="darkred",
                                         label_pos=0.4,
                                         bbox=dict(boxstyle="round,pad=0.2",
                                                   fc="white", alpha=0.85),
                                         ax=ax)
        ax.set_title(titulo, fontsize=9, fontweight="bold")
        ax.set_axis_off()

    fig, axes = plt.subplots(1, 2, figsize=(26, 11))

    # Mapa izquierdo: ruta óptima normal
    _resaltar_camino(
        axes[0], G_orig, G_orig,
        dato_normal["camino"],
        f"RUTA ÓPTIMA: {ORIGEN} → {destino}\n"
        f"{dato_normal['distancia']:.0f} km  ·  {dato_normal['energia']:.1f} MWh recibidos",
        color_camino="green"
    )

    # Mapa derecho: ruta alternativa tras avería
    if dato_averia is None or dato_averia["distancia"] == float('inf'):
        # Sin suministro
        _resaltar_camino(
            axes[1], G_averia, G_orig,
            [],
            f"AVERÍA {origen_f} → {destino_f} ({km_f} km)\n"
            f"⚠ {destino} queda SIN SUMINISTRO",
            color_camino="red",
            arista_cortada=(origen_f, destino_f)
        )
    else:
        _resaltar_camino(
            axes[1], G_averia, G_orig,
            dato_averia["camino"],
            f"AVERÍA {origen_f} → {destino_f} ({km_f} km)  →  Ruta alternativa\n"
            f"{dato_averia['distancia']:.0f} km  ·  {dato_averia['energia']:.1f} MWh  "
            f"({dato_normal['energia']-dato_averia['energia']:+.1f} MWh)",
            color_camino="red",
            arista_cortada=(origen_f, destino_f)
        )

    plt.suptitle(
        f"Distribución eléctrica: {ORIGEN} → {destino}  |  "
        f"Avería simulada en tramo {origen_f} → {destino_f}",
        fontsize=12, fontweight="bold"
    )
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
#   MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(MENSAJE_CIERZO)

    # Mostrar red general en situación normal
    grafo_original = construir_grafo()
    res_normal     = ejecutar_simulacion(grafo_original)
    dibujar_red_normal(grafo_original, res_normal)

    # Pedir ciudad destino al usuario
    disponibles = sorted(
        r["ciudad"] for r in res_normal
        if r["distancia"] not in (0, float('inf'))
    )
    print("Provincias disponibles:")
    print(", ".join(disponibles))

    destino = input(
        "\n¿A qué provincia quieres enviar la energía desde Zaragoza? "
    ).strip()

    if destino not in grafo_original.adyacencia:
        print(f"\n  '{destino}' no está en el grafo. Comprueba el nombre exacto.")
        return

    # Análisis completo: ruta óptima + avería en esa ruta + alternativa
    analizar_destino_con_fallo(grafo_original, destino)


if __name__ == "__main__":
    main()
