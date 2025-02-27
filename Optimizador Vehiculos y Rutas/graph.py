import streamlit as st
import networkx as nx
import pandas as pd

def crear_grafo():
    graph = nx.DiGraph()
    
    # Definir nodos con coordenadas reales del sur de Perú, centrado en Juliaca
    nodes = {
        "Juliaca": (-15.500060871723104, -70.12876822242285),  # Centro
        "Puno": (-15.84206715081413, -70.02148324949029),
        "Arequipa": (-16.409047, -71.537451),
        "Cusco": (-13.532, -71.967),
        "Tacna": (-18.0066, -70.2463)
    }
    
    # Definir conexiones entre nodos con costos ficticios (distancias aproximadas en km)
    edges = {
        ("Juliaca", "Puno"): 60, 
        ("Juliaca", "Arequipa"): 280, 
        ("Juliaca", "Cusco"): 350,
        ("Juliaca", "Tacna"): 600,
        ("Puno", "Cusco"): 380, 
        ("Arequipa", "Tacna"): 380, 
        ("Cusco", "Tacna"): 800
    }
    
    # Agregar nodos al grafo
    for node, coord in nodes.items():
        graph.add_node(node, pos=coord)
    
    # Agregar conexiones entre nodos (edges)
    for edge, cost in edges.items():
        graph.add_edge(edge[0], edge[1], weight=cost)
    
    return graph, nodes, edges

def cargar_datos_csv(archivo_csv):
    df = pd.read_csv(archivo_csv)
    
    # Leer nodos (clientes) con sus coordenadas
    nodes = {row['Cliente']: (row['X'], row['Y']) for _, row in df.iterrows()}
    print("Nodos cargados:", nodes)  # Mensaje de depuración
    # Leer las conexiones con costos
    edges = {(row['Origen'], row['Destino']): row['Costo'] for _, row in df.iterrows()}
    print("Conexiones cargadas:", edges)  # Mensaje de depuración
    
    # Verificar que todos los nodos en las conexiones tengan coordenadas
    for edge in edges:
        origen, destino = edge
        if origen not in nodes:
            print(f"Advertencia: El nodo {origen} no tiene coordenadas asignadas.")
        if destino not in nodes:
            print(f"Advertencia: El nodo {destino} no tiene coordenadas asignadas.")

    
    return nodes, edges
