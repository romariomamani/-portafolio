import numpy as np

def gauss_jordan(x, y, verbose=0):
    m, n = x.shape
    augmented_mat = np.zeros(shape=(m, n + 1))
    augmented_mat[:m, :n] = x
    augmented_mat[:, m] = y
    np.set_printoptions(precision=2, suppress=True)
    if verbose > 0:
        print('# Matriz aumentada inicial:')
        print(augmented_mat)
    outer_loop = [[0, m - 1, 1], [m - 1, 0, -1]]
    for d in range(2):
        for i in range(outer_loop[d][0], outer_loop[d][1], outer_loop[d][2]):
            inner_loop = [[i + 1, m, 1], [i - 1, -1, -1]]
            for j in range(inner_loop[d][0], inner_loop[d][1], inner_loop[d][2]):
                k = (-1) * augmented_mat[j, i] / augmented_mat[i, i]
                temp_row = augmented_mat[i, :] * k
                if verbose > 1:
                    print('# Usar fila %2i para fila %2i' % (i + 1, j + 1))
                    print('k=%.2f' % k, '*', augmented_mat[i, :], '=', temp_row)
                augmented_mat[j, :] = augmented_mat[j, :] + temp_row
                if verbose > 1:
                    print(augmented_mat)
    for i in range(0, m):
        augmented_mat[i, :] = augmented_mat[i, :] / augmented_mat[i, i]
    if verbose > 0:
        print('# Normalizar las filas:')
        print(augmented_mat)
    return augmented_mat[:, n]

if __name__ == "__main__":
    print("Resolver un sistema de ecuaciones lineales usando Gauss-Jordan.")
    filas = int(input("Ingrese el número de ecuaciones (filas): "))
    columnas = int(input("Ingrese el número de incógnitas (columnas): "))
    
    print("\nIngrese los coeficientes de la matriz:")
    coeficientes = []
    for i in range(filas):
        fila = list(map(float, input(f"Fila {i + 1} (separada por espacios): ").split()))
        coeficientes.append(fila)
    coeficientes = np.array(coeficientes)
    
    print("\nIngrese los términos independientes:")
    lado_derecho = []
    for i in range(filas):
        valor = float(input(f"Término independiente para la ecuación {i + 1}: "))
        lado_derecho.append(valor)
    lado_derecho = np.array(lado_derecho)
    
    verbose = int(input("\nNivel de detalle (0: Sin pasos, 1: Con matriz aumentada inicial y final, 2: Todos los pasos): "))
    resultado = gauss_jordan(coeficientes, lado_derecho, verbose)
    
    print("\nEl resultado del sistema es:")
    print(resultado)
