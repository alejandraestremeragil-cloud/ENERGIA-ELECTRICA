# Red de Distribución Eléctrica – Aragón y la Península Ibérica

Simulación de la distribución de energía eléctrica desde **Zaragoza** hacia las 47 provincias peninsulares de España, usando estructuras de datos y el algoritmo de **Dijkstra**.

---

## 🌬️ Motivación

Aragón es la segunda comunidad autónoma de España en potencia eólica instalada. El **cierzo**, un viento del noroeste que recorre el Valle del Ebro con intensidad y regularidad excepcionales, convierte a la región en un territorio con un potencial eólico único. Como resultado, Aragón genera casi el doble de energía de la que consume, exportando el excedente al resto del país.

Zaragoza actúa como **nodo central de distribución** por su posición estratégica: a menos de 320 km de Madrid, Barcelona, Valencia, Bilbao y San Sebastián, y conectada directamente con Huesca y Teruel.

Este proyecto modela esa red real para estudiar cómo se distribuye la energía y qué ocurre cuando falla una línea.

---

## 🗂️ Estructura del proyecto

```
red_electrica.py     # Código principal
red_electrica_*.xlsx # Excel generado automáticamente al ejecutar
README.md            # Este archivo
```

---

## ⚙️ Funcionamiento

El programa modela la red eléctrica peninsular como un **grafo dirigido y ponderado**:

- Cada **nodo** representa una capital de provincia.
- Cada **arista** representa una línea de alta tensión entre provincias vecinas.
- El **peso** de cada arista es la distancia geodésica en km entre ambas capitales.
- El flujo de energía parte siempre desde **Zaragoza**.

### Algoritmo de Dijkstra

Se aplica Dijkstra para calcular la **ruta de menor pérdida energética** desde Zaragoza hasta cualquier provincia. Minimizar la distancia acumulada equivale a minimizar la energía perdida en el transporte.

### Pérdida energética

```
Pérdida = (distancia_km / 100) × 4% × 1000 MWh
Energía final = 1000 MWh − pérdida
```

Valor orientativo para líneas de alta tensión de 400 kV.

### Simulación de avería

Una vez elegido el destino, el programa selecciona aleatoriamente un tramo de la ruta óptima y lo elimina del grafo. Dijkstra recalcula la mejor ruta alternativa y muestra el impacto en distancia y energía recibida.

---

## 🚀 Cómo ejecutarlo

### 1. Instalar dependencias

```bash
pip install networkx matplotlib openpyxl
```

### 2. Ejecutar

```bash
python red_electrica.py
```

### 3. Flujo del programa

1. Se muestra el mapa general de la red con los nodos coloreados por Comunidad Autónoma.
2. El programa pregunta a qué provincia quieres enviar la energía.
3. Muestra la **ruta óptima** (Dijkstra sin averías).
4. Simula una **avería aleatoria** en esa ruta y calcula la alternativa.
5. Genera dos mapas comparativos: ruta óptima vs. ruta tras la avería.
6. Exporta un **Excel** con todos los resultados.
7. Opcionalmente, lanza una **animación en tiempo real** que muestra cómo viaja la energía salto a salto, con pausa dramática en el punto de avería.

---

## ✨ Funcionalidades principales

| Funcionalidad | Descripción |
|---|---|
| 🗺️ Mapa de la red | Grafo geográfico con 47 provincias, coloreado por CCAA |
| 🔍 Dijkstra | Ruta de menor pérdida energética hasta cualquier destino |
| ⚡ Cálculo energético | MWh recibidos y pérdida por distancia en cada ruta |
| 💶 Coste estimado | Coste de construcción de línea a 500.000 €/km |
| 🔌 Simulación de avería | Fallo aleatorio en la ruta óptima y recálculo automático |
| 🎬 Animación en tiempo real | La energía viaja nodo a nodo con barra de progreso |
| 📊 Exportación Excel | Resultados completos con formato, colores y comparativa |

---

## 🗺️ Colores por Comunidad Autónoma

Cada comunidad tiene un color propio en el mapa para facilitar la lectura:

| Comunidad | Color |
|---|---|
| Aragón | 🔴 Rojo ladrillo |
| Cataluña | 🟡 Ámbar dorado |
| C. Valenciana | 🟢 Verde esmeralda |
| Madrid | 🟣 Lavanda |
| País Vasco | 🩵 Turquesa |
| Andalucía | 🔴 Rojo vivo |
| Galicia | 🔵 Índigo |
| ... | ... |

---

## 📦 Dependencias

| Librería | Uso |
|---|---|
| `heapq` | Min-heap para el algoritmo de Dijkstra |
| `networkx` | Construcción y dibujo del grafo |
| `matplotlib` | Visualización y animación |
| `openpyxl` | Generación del Excel formateado |
| `math` | Cálculo de distancias geodésicas (fórmula de Haversine) |
| `random` | Selección aleatoria del tramo en avería |

---

## 👤 Autor

Proyecto de la asignatura **Estructuras de Datos y Algoritmos**.  
Universidad Alfonso X el Sabio — curso 2024/2025.