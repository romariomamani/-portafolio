import numpy as np
import tkinter as tk
from tkinter import messagebox

def regla_de_cramer(A, b):
    try:
        det_A = np.linalg.det(A)
        if det_A == 0:
            return "El sistema no tiene solución única."

        soluciones = []
        n = len(b)
        for i in range(n):
            Ai = A.copy()
            Ai[:, i] = b
            soluciones.append(np.linalg.det(Ai) / det_A)

        return soluciones
    except Exception as e:
        return f"Error: {str(e)}"

def gauss_jordan(A, b):
    try:
        n = len(b)
        augmented_matrix = np.hstack((A, b.reshape(-1, 1)))

        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r, i]))
            augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
            pivot = augmented_matrix[i, i]
            augmented_matrix[i] = augmented_matrix[i] / pivot

            for j in range(n):
                if j != i:
                    augmented_matrix[j] -= augmented_matrix[j, i] * augmented_matrix[i]

        return augmented_matrix[:, -1]
    except Exception as e:
        return f"Error: {str(e)}"

def sustitucion(A, b):
    try:
        n = len(b)
        x = np.zeros(n)

        for i in range(n - 1, -1, -1):
            sum_ax = sum(A[i, j] * x[j] for j in range(i + 1, n))
            x[i] = (b[i] - sum_ax) / A[i, i]

        return x
    except Exception as e:
        return f"Error: {str(e)}"

def resolver():
    try:
        A = np.array([[float(entry_matriz[i][j].get()) for j in range(num_ecuaciones)] for i in range(num_ecuaciones)])
        b = np.array([float(entry_vectores[i].get()) for i in range(num_ecuaciones)])

        metodo = metodo_var.get()
        if metodo == "Cramer":
            resultado = regla_de_cramer(A, b)
        elif metodo == "Jordan":
            resultado = gauss_jordan(A, b)
        elif metodo == "Sustitucion":
            resultado = sustitucion(A, b)
        else:
            resultado = "Seleccione un método válido."

        messagebox.showinfo("Resultado", f"Solución: {resultado}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Solución de Sistemas de Ecuaciones")

# Variables
num_ecuaciones = 3
entry_matriz = [[tk.Entry(ventana, width=5) for _ in range(num_ecuaciones)] for _ in range(num_ecuaciones)]
entry_vectores = [tk.Entry(ventana, width=5) for _ in range(num_ecuaciones)]
metodo_var = tk.StringVar(value="Cramer")

# Interfaz
for i in range(num_ecuaciones):
    for j in range(num_ecuaciones):
        entry_matriz[i][j].grid(row=i, column=j, padx=5, pady=5)

    tk.Label(ventana, text="|").grid(row=i, column=num_ecuaciones, padx=5, pady=5)
    entry_vectores[i].grid(row=i, column=num_ecuaciones + 1, padx=5, pady=5)

tk.Label(ventana, text="Método:").grid(row=num_ecuaciones, column=0, columnspan=2)
tk.OptionMenu(ventana, metodo_var, "Cramer", "Jordan", "Sustitucion").grid(row=num_ecuaciones, column=2, columnspan=2)

tk.Button(ventana, text="Resolver", command=resolver).grid(row=num_ecuaciones + 1, column=0, columnspan=num_ecuaciones + 2, pady=10)

ventana.mainloop()
