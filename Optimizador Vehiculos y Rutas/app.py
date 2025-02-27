import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import folium
import random
import pandas as pd
from streamlit_folium import st_folium
from solver import resolver_vrp_multiobjetivo
from graph import crear_grafo, cargar_datos_csv
from folium.plugins import AntPath
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Inicializar el geocodificador
geolocator = Nominatim(user_agent="Optimización de Ruteo de Vehículos")

st.set_page_config(page_title="Optimización de Ruteo de Vehículos", layout="wide")

st.title("🚚 Optimización de Ruteo de Vehículos")
st.markdown("---")

# Inicializar el estado de sesión
if 'resultados' not in st.session_state:
    st.session_state.resultados = None

def mostrar_guia_usuario():
    st.subheader("📚 Guía del Usuario")
    st.markdown("""
    **Bienvenido a la aplicación de Optimización de Ruteo de Vehículos.**

    **1. Cargar Datos:**
    - Utiliza el botón en la barra lateral para cargar un archivo CSV con los datos de los clientes.
    - El archivo debe contener columnas para el origen, destino y costo.

    **2. Ingresar Clientes Manualmente:**
    - Puedes ingresar clientes manualmente usando los campos en la barra lateral.
    - Proporciona el origen, destino y costo para cada cliente.

    **3. Seleccionar Vehículos:**
    - Define el número de vehículos y sus capacidades en la barra lateral.

    **4. Restricciones de Tiempo:**
    - Establece ventanas de tiempo para cada nodo (excepto el depósito).

    **5. Ejecutar la Optimización:**
    - Una vez que todos los datos estén ingresados, la aplicación calculará las rutas óptimas.
    - Los resultados se mostrarán en el mapa y en el grafo de conexiones.

    **6. Mensajes de Error:**
    - Si encuentras algún error, revisa los mensajes de error para obtener más información.
    """)

def mostrar_formulario_feedback():
    st.subheader("📝 Formulario de Feedback")
    feedback = st.text_area("Por favor, proporciona tu feedback sobre la aplicación:")

    if st.button("Enviar Feedback"):
        if feedback.strip():
            guardar_feedback(feedback)
            st.success("¡Gracias por tu feedback!")
        else:
            st.warning("Por favor, ingresa algún comentario antes de enviar.")

def guardar_feedback(feedback):
    with open("feedback.txt", "a") as file:
        file.write(feedback + "\n")

# Botón para mostrar la guía del usuario
if st.sidebar.button("📚 Mostrar Guía del Usuario"):
    mostrar_guia_usuario()

# Botón para mostrar el formulario de feedback
if st.sidebar.button("📝 Proporcionar Feedback"):
    mostrar_formulario_feedback()

# Cargar datos desde archivo CSV
archivo_csv = st.sidebar.file_uploader("📂 Cargar archivo CSV de clientes", type=["csv"])

# Configuración de clientes y costos en la barra lateral
st.sidebar.header("Datos de Clientes y Costos")

# Número de clientes
num_clientes = st.sidebar.number_input("Número de clientes", min_value=1, value=1)

# Ingresar datos de clientes
client_data = []
for i in range(num_clientes):
    with st.sidebar.expander(f"Cliente {i+1}"):
        st.write(f"### Detalles del Cliente {i+1}")
        origen = st.text_input(f"Origen (Cliente {i+1})", f"Origen_{i+1}")
        destino = st.text_input(f"Destino (Cliente {i+1})", f"Destino_{i+1}")
        costo = st.number_input(f"Costo (Cliente {i+1})", min_value=0, value=100)

        try:
            # Obtener coordenadas para el origen y destino
            location_origen = geolocator.geocode(origen)
            location_destino = geolocator.geocode(destino)
            x_origen, y_origen = location_origen.latitude, location_origen.longitude
            x_destino, y_destino = location_destino.latitude, location_destino.longitude

        except GeocoderTimedOut:
            st.sidebar.error("Error: El servicio de geocodificación está tardando demasiado. Inténtalo de nuevo.")
            continue
        except GeocoderServiceError as e:
            st.sidebar.error(f"Error de servicio de geocodificación: {e}. Por favor, inténtalo de nuevo más tarde.")
            continue

        if st.sidebar.button(f"Agregar Cliente {i+1}"):
            client_data.append((origen, destino, costo, (x_origen, y_origen), (x_destino, y_destino)))

# Configuración de vehículos en la barra lateral
st.sidebar.header("Configuración de Vehículos")
num_vehiculos = st.sidebar.number_input("Número de vehículos", min_value=1, value=1)
capacidades = [st.sidebar.number_input(f"Capacidad del vehículo {i+1}", min_value=1, value=100) for i in range(num_vehiculos)]

# Selección de ciudades para restricciones de tiempo
st.sidebar.header("Selección de Ciudades para Restricciones de Tiempo")
ciudades = ["Juliaca", "Puno", "Arequipa", "Cusco", "Tacna"]
ciudades_seleccionadas = st.sidebar.multiselect("Selecciona ciudades para restricciones de tiempo:", ciudades)

# Inicialización de ventanas_tiempo con valores predeterminados
ventanas_tiempo = {ciudad: (pd.to_datetime("09:00").time(), pd.to_datetime("17:00").time()) for ciudad in ciudades}

# Configuración de restricciones de tiempo para ciudades seleccionadas
for ciudad in ciudades_seleccionadas:
    with st.sidebar.expander(f"{ciudad}"):
        inicio = st.time_input(f"Hora de inicio para {ciudad}", value=ventanas_tiempo[ciudad][0])
        fin = st.time_input(f"Hora de fin para {ciudad}", value=ventanas_tiempo[ciudad][1])
        ventanas_tiempo[ciudad] = (inicio, fin)

# Pesos de los objetivos en la barra lateral
tiempo_viaje_ponderado = st.sidebar.number_input("Peso para minimizar tiempo de viaje", min_value=0.0, max_value=1.0, value=0.7)
satisfaccion_cliente_ponderado = st.sidebar.number_input("Peso para maximizar satisfacción del cliente", min_value=0.0, max_value=1.0, value=0.3)

# Botón de optimización
if st.sidebar.button("Optimizar"):
    # Procesar datos de clientes
    nodes = {}
    edges = {}

    if archivo_csv is not None:
        nodes, edges = cargar_datos_csv(archivo_csv)
        graph = nx.DiGraph()
        for node, coord in nodes.items():
            graph.add_node(node, pos=coord)
        for edge, cost in edges.items():
            graph.add_edge(edge[0], edge[1], weight=cost)
    else:
        graph, nodes, edges = crear_grafo()

    # Agregar datos de clientes ingresados manualmente
    for data in client_data:
        origen, destino, costo, coord_origen, coord_destino = data
        if origen in ciudades_seleccionadas and destino in ciudades_seleccionadas:
            nodes[origen] = coord_origen
            nodes[destino] = coord_destino
            edges[(origen, destino)] = costo
            graph.add_node(origen, pos=coord_origen)
            graph.add_node(destino, pos=coord_destino)
            graph.add_edge(origen, destino, weight=costo)

    # Definir la demanda para cada nodo
    demanda = {node: 10 for node in nodes}

    # Ejemplo de satisfacción del cliente (puede ser una función de la puntualidad)
    satisfaccion = {edge: random.uniform(0, 1) for edge in edges}

    # Antes de llamar a la función de resolución
    print("Ventanas de tiempo:", ventanas_tiempo)

    # Llamar a la función de resolución
    model, x = resolver_vrp_multiobjetivo(nodes, edges, num_vehiculos, capacidades, ventanas_tiempo, demanda, satisfaccion, tiempo_viaje_ponderado, satisfaccion_cliente_ponderado)

    # Guardar resultados en el estado de sesión
    st.session_state.resultados = {
        "model": model,
        "x": x,
        "nodes": nodes,
        "edges": edges,
        "graph": graph
    }

# Mostrar resultados si están disponibles
if st.session_state.resultados:
    resultados = st.session_state.resultados
    model = resultados["model"]
    x = resultados["x"]
    nodes = resultados["nodes"]
    edges = resultados["edges"]
    graph = resultados["graph"]

    # Mostrar resultados de la optimización
    st.subheader("Resultados de Optimización")
    st.write("### Estado de optimización:", model.status)
    for edge in edges:
        if x[edge].varValue == 1:
            st.write(f"✅ Ruta seleccionada: {edge} con costo {edges[edge]}")

    # Mapa interactivo con Folium centrado en Juliaca
    st.subheader("🌍 Mapa de Rutas Optimizadas")
    mapa = folium.Map(location=[-15.500060871723104, -70.12876822242285], zoom_start=10)

    # Colores para diferentes vehículos
    colores = ['blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']

    # Agregar marcadores de nodos
    for node, coord in nodes.items():
        folium.Marker([coord[0], coord[1]], popup=node).add_to(mapa)

    # Agregar rutas animadas
    for v in range(num_vehiculos):
        ruta = [edge for edge in edges if x[edge].varValue == 1 and edge[0] == f"vehiculo_{v+1}"]
        if ruta:
            puntos = [nodes[edge[0]] for edge in ruta] + [nodes[ruta[-1][1]]]
            AntPath(locations=[list(reversed(punto)) for punto in puntos], color=colores[v % len(colores)]).add_to(mapa)

    st_folium(mapa, width=700, height=500)

    # Visualización del grafo
    st.subheader("📌 Grafo de Conexiones")
    fig, ax = plt.subplots()
    pos = {node: coord for node, coord in nodes.items()}

    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightblue', ax=ax)
    edge_labels = {(i, j): f"{cost}" for (i, j), cost in edges.items()}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

    st.pyplot(fig)

    # Gráficos de barras para costos y distancias
    st.subheader("📈 Análisis de Costos y Distancias")
    costos = [edges[edge] for edge in edges if x[edge].varValue == 1]
    distancias = [graph[edge[0]][edge[1]]['weight'] for edge in edges if x[edge].varValue == 1]

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    ax[0].bar(range(len(costos)), costos, color='skyblue')
    ax[0].set_title('Costos de las Rutas')
    ax[0].set_xlabel('Rutas')
    ax[0].set_ylabel('Costo')

    ax[1].bar(range(len(distancias)), distancias, color='lightgreen')
    ax[1].set_title('Distancias de las Rutas')
    ax[1].set_xlabel('Rutas')
    ax[1].set_ylabel('Distancia')

    st.pyplot(fig)

    # Tabla interactiva de resultados
    st.subheader("🗒️ Tabla de Resultados")
    resultados_tabla = pd.DataFrame({
        "Ruta": [f"{edge[0]} -> {edge[1]}" for edge in edges if x[edge].varValue == 1],
        "Costo": costos,
        "Distancia": distancias
    })
    st.dataframe(resultados_tabla)
