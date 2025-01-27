import streamlit as st
import numpy as np

def gauss_jordan(x, y, verbose=0):
    m, n = x.shape
    augmented_mat = np.zeros(shape=(m, n + 1))
    augmented_mat[:m, :n] = x
    augmented_mat[:, m] = y
    np.set_printoptions(precision=2, suppress=True)
    
    if verbose > 0:
        st.write('# Matriz aumentada inicial:')
        st.write(augmented_mat)
        
    outer_loop = [[0, m - 1, 1], [m - 1, 0, -1]]
    for d in range(2):
        for i in range(outer_loop[d][0], outer_loop[d][1], outer_loop[d][2]):
            inner_loop = [[i + 1, m, 1], [i - 1, -1, -1]]
            for j in range(inner_loop[d][0], inner_loop[d][1], inner_loop[d][2]):
                k = (-1) * augmented_mat[j, i] / augmented_mat[i, i]
                temp_row = augmented_mat[i, :] * k
                if verbose > 1:
                    st.write(f'# Usar fila {i + 1} para fila {j + 1}')
                    st.write(f'k={k:.2f} * {augmented_mat[i, :]} = {temp_row}')
                augmented_mat[j, :] = augmented_mat[j, :] + temp_row
                if verbose > 1:
                    st.write(augmented_mat)
                    
    for i in range(0, m):
        augmented_mat[i, :] = augmented_mat[i, :] / augmented_mat[i, i]
        
    if verbose > 0:
        st.write('# Normalizar las filas:')
        st.write(augmented_mat)
        
    return augmented_mat[:, n]

def main():
    st.title("Resolución de Sistemas de Ecuaciones Lineales usando Gauss-Jordan")
    
    col1, col2 = st.columns(2)
    with col1:
        filas = st.number_input("Número de ecuaciones (filas)", min_value=1, value=2, step=1)
    with col2:
        columnas = st.number_input("Número de incógnitas (columnas)", min_value=1, value=2, step=1)
    
    st.subheader("Matriz de Coeficientes")
    coeficientes = []
    for i in range(int(filas)):
        cols = st.columns(int(columnas))
        fila = []
        for j, col in enumerate(cols):
            val = col.number_input(f"a{i+1}{j+1}", value=0.0, format="%.2f", key=f"coef_{i}_{j}")
            fila.append(val)
        coeficientes.append(fila)
    
    # Términos independientes
    st.subheader("Términos Independientes")
    lado_derecho = []
    cols = st.columns(int(filas))
    for i, col in enumerate(cols):
        val = col.number_input(f"b{i+1}", value=0.0, format="%.2f", key=f"b_{i}")
        lado_derecho.append(val)
    
    # Nivel de detalle
    verbose = st.select_slider(
        "Nivel de detalle",
        options=[0, 1, 2],
        value=1,
        help="0: Sin pasos, 1: Con matriz aumentada inicial y final, 2: Todos los pasos"
    )
    
    if st.button("Resolver Sistema"):
        try:
            coeficientes_array = np.array(coeficientes)
            lado_derecho_array = np.array(lado_derecho)
            
            st.subheader("Sistema de Ecuaciones:")
            for i in range(len(coeficientes)):
                ecuacion = " + ".join([f"{coeficientes[i][j]:.2f}x{j+1}" for j in range(len(coeficientes[i]))])
                st.write(f"{ecuacion} = {lado_derecho[i]:.2f}")
            
            resultado = gauss_jordan(coeficientes_array, lado_derecho_array, verbose)
            
            st.subheader("Solución del Sistema:")
            for i, val in enumerate(resultado):
                st.write(f"x{i+1} = {val:.4f}")
                
        except np.linalg.LinAlgError:
            st.error("Error: El sistema no tiene solución única.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()