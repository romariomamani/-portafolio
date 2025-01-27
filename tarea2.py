import matplotlib.pyplot as plt

def precio_vivienda(area):
    m = 1500  # Costo por metro cuadrado
    b = 20000  # Costos fijos
    return m * area + b

def ganancia_mensual(num_predicciones):
    c = 10  # Ganancia por predicción
    b = 3000  # Ingresos fijos
    return c * num_predicciones + b

def tiempo_procesamiento(tamano_datos):
    k = 0.5  # Tiempo por unidad de datos
    c = 10  # Tiempo de configuración
    return k * tamano_datos + c

def costo_almacenamiento(datos):
    p = 0.1  # Costo por gigabyte
    f = 50  # Tarifas fijas
    return p * datos + f

def medicion_calibrada(medicion_cruda):
    a = 1.5  # Factor de ajuste
    b = 5  # Desplazamiento constante
    return a * medicion_cruda + b

def tiempo_respuesta(solicitudes):
    m = 0.02  # Tiempo incremental por solicitud
    b = 0.5  # Tiempo base
    return m * solicitudes + b

def ingresos_plataforma(suscriptores):
    p = 10  # Ingreso promedio por suscriptor
    b = 1000  # Ingresos adicionales
    return p * suscriptores + b

def energia_consumida(operaciones):
    k = 0.05  # Energía consumida por operación
    b = 50  # Energía base para encender el sistema
    return k * operaciones + b

def numero_likes(seguidores):
    m = 0.01  # Proporción promedio de interacción
    b = 100  # Nivel base de likes
    return m * seguidores + b

def costo_entrenamiento(iteraciones):
    p = 0.5  # Costo por iteración
    c = 100  # Costos iniciales
    return p * iteraciones + c

def mostrar_grafico(x, y, xlabel, ylabel, title):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

while True:
    print("\nSeleccione una opción:")
    print("1. Calcular precio de vivienda")
    print("2. Calcular ganancia mensual")
    print("3. Calcular tiempo de procesamiento")
    print("4. Calcular costo de almacenamiento")
    print("5. Calcular medición calibrada")
    print("6. Calcular tiempo de respuesta")
    print("7. Calcular ingresos de la plataforma")
    print("8. Calcular energía consumida")
    print("9. Calcular número de likes")
    print("10. Calcular costo de entrenamiento")
    print("11. Salir")

    opcion = input("Ingrese el número de su elección: ")

    if opcion == "1":
        area = float(input("Ingrese el área en metros cuadrados: "))
        print(f"El precio de la vivienda para un área de {area} m² es: ${precio_vivienda(area)}")
        areas = range(1, 1001)
        precios = [precio_vivienda(a) for a in areas]
        mostrar_grafico(areas, precios, "Área (m²)", "Precio ($)", "Precio de Vivienda vs Área")

    elif opcion == "2":
        predicciones = int(input("Ingrese el número de predicciones realizadas: "))
        print(f"La ganancia mensual para {predicciones} predicciones es: ${ganancia_mensual(predicciones)}")
        predicciones_range = range(1, 1001)
        ganancias = [ganancia_mensual(p) for p in predicciones_range]
        mostrar_grafico(predicciones_range, ganancias, "Número de Predicciones", "Ganancia Mensual ($)", "Ganancia Mensual vs Número de Predicciones")

    elif opcion == "3":
        tamano_datos = float(input("Ingrese el tamaño de los datos en unidades: "))
        print(f"El tiempo de procesamiento para un tamaño de datos de {tamano_datos} unidades es: {tiempo_procesamiento(tamano_datos)} segundos")
        tamanos_datos = range(1, 1001)
        tiempos = [tiempo_procesamiento(d) for d in tamanos_datos]
        mostrar_grafico(tamanos_datos, tiempos, "Tamaño de Datos (unidades)", "Tiempo de Procesamiento (s)", "Tiempo de Procesamiento vs Tamaño de Datos")

    elif opcion == "4":
        datos = float(input("Ingrese la cantidad de datos almacenados en GB: "))
        print(f"El costo de almacenamiento para {datos} GB es: ${costo_almacenamiento(datos)}")
        datos_range = range(1, 1001)
        costos = [costo_almacenamiento(d) for d in datos_range]
        mostrar_grafico(datos_range, costos, "Cantidad de Datos (GB)", "Costo de Almacenamiento ($)", "Costo de Almacenamiento vs Cantidad de Datos")

    elif opcion == "5":
        medicion_cruda = float(input("Ingrese la medición en crudo: "))
        print(f"La medición calibrada es: {medicion_calibrada(medicion_cruda)}")
        mediciones_crudas = range(1, 1001)
        mediciones_calibradas = [medicion_calibrada(m) for m in mediciones_crudas]
        mostrar_grafico(mediciones_crudas, mediciones_calibradas, "Medición en Crudo", "Medición Calibrada", "Medición Calibrada vs Medición en Crudo")

    elif opcion == "6":
        solicitudes = int(input("Ingrese el número de solicitudes simultáneas: "))
        print(f"El tiempo de respuesta promedio para {solicitudes} solicitudes es: {tiempo_respuesta(solicitudes)} segundos")
        solicitudes_range = range(1, 1001)
        tiempos_respuesta = [tiempo_respuesta(s) for s in solicitudes_range]
        mostrar_grafico(solicitudes_range, tiempos_respuesta, "Número de Solicitudes", "Tiempo de Respuesta (s)", "Tiempo de Respuesta vs Número de Solicitudes")

    elif opcion == "7":
        suscriptores = int(input("Ingrese el número de suscriptores: "))
        print(f"Los ingresos de la plataforma para {suscriptores} suscriptores son: ${ingresos_plataforma(suscriptores)}")
        suscriptores_range = range(1, 1001)
        ingresos = [ingresos_plataforma(s) for s in suscriptores_range]
        mostrar_grafico(suscriptores_range, ingresos, "Número de Suscriptores", "Ingresos ($)", "Ingresos vs Número de Suscriptores")

    elif opcion == "8":
        operaciones = int(input("Ingrese el número de operaciones realizadas: "))
        print(f"La energía consumida para {operaciones} operaciones es: {energia_consumida(operaciones)} unidades")
        operaciones_range = range(1, 1001)
        energias = [energia_consumida(o) for o in operaciones_range]
        mostrar_grafico(operaciones_range, energias, "Número de Operaciones", "Energía Consumida (unidades)", "Energía Consumida vs Número de Operaciones")

    elif opcion == "9":
        seguidores = int(input("Ingrese el número de seguidores: "))
        print(f"El número de likes para {seguidores} seguidores es: {numero_likes(seguidores)}")
        seguidores_range = range(1, 1001)
        likes = [numero_likes(f) for f in seguidores_range]
        mostrar_grafico(seguidores_range, likes, "Número de Seguidores", "Número de Likes", "Número de Likes vs Número de Seguidores")

    elif opcion == "10":
        iteraciones = int(input("Ingrese el número de iteraciones: "))
        print(f"El costo de entrenamiento para {iteraciones} iteraciones es: ${costo_entrenamiento(iteraciones)}")
        iteraciones_range = range(1, 1001)
        costos_entrenamiento = [costo_entrenamiento(i) for i in iteraciones_range]
        mostrar_grafico(iteraciones_range, costos_entrenamiento, "Número de Iteraciones", "Costo de Entrenamiento ($)", "Costo de Entrenamiento vs Número de Iteraciones")

    elif opcion == "11":
        print("Saliendo del programa. ¡Hasta luego!")
        break

    else:
        print("Opción no válida. Intente nuevamente.")
