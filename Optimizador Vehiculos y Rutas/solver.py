import pulp as lp
import random

def convertir_a_minutos(tiempo):
    return tiempo.hour * 60 + tiempo.minute

def resolver_vrp_multiobjetivo(nodes, edges, num_vehiculos, capacidades, ventanas_tiempo, demanda, satisfaccion, tiempo_viaje_ponderado, satisfaccion_cliente_ponderado):
    model = lp.LpProblem("Vehicle_Objetive_VRP", lp.LpMinimize)
    x = lp.LpVariable.dicts("Route", edges, cat=lp.LpBinary)

    # Variables de tiempo para cada nodo
    tiempo_llegada = lp.LpVariable.dicts("TiempoLlegada", nodes, lowBound=0, cat='Continuous')

    # Función objetivo ponderada
    model += lp.lpSum(tiempo_viaje_ponderado * x[edge] * cost for edge, cost in edges.items()) - \
             lp.lpSum(satisfaccion_cliente_ponderado * satisfaccion[edge] for edge in edges)

    # Restricciones de entrada y salida
    for node in nodes:
        if node != "depot":
            model += lp.lpSum(x[(i, node)] for i in nodes if (i, node) in edges) == 1
            model += lp.lpSum(x[(node, j)] for j in nodes if (node, j) in edges) == 1

    # Restricciones de capacidad
    for v in range(num_vehiculos):
        model += lp.lpSum(x[(i, j)] * demanda[j] for (i, j) in edges if i == f"vehiculo_{v+1}") <= capacidades[v]

    # Restricciones de tiempo
    for node in nodes:
        if node != "depot":
            inicio, fin = ventanas_tiempo[node]
            inicio_minutos = convertir_a_minutos(inicio)
            fin_minutos = convertir_a_minutos(fin)
            model += tiempo_llegada[node] >= inicio_minutos
            model += tiempo_llegada[node] <= fin_minutos

    # Restricciones de tiempo de viaje (simplificado)
    for (i, j) in edges:
        if i != "depot" and j != "depot":
            model += tiempo_llegada[j] >= tiempo_llegada[i] + x[(i, j)] * edges[(i, j)] - (1 - x[(i, j)]) * 100000

    model.solve()
    return model, x
