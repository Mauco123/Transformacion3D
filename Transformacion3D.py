# Importa la librería numpy, indispensable para el manejo de arreglos y la multiplicación de matrices (álgebra lineal).
import numpy as np
# Importa la librería matplotlib, utilizada para generar gráficos y visualizaciones, específicamente en 3D.
import matplotlib.pyplot as plt


# ==========================================
# --- Matrices de Transformación 3D ---
# En computación gráfica, usamos matrices de 4x4 y coordenadas homogéneas [x, y, z, 1]
# para poder aplicar traslación, rotación y escalamiento mediante una sola multiplicación.
# ==========================================

def matriz_traslacion(tx, ty, tz):
    """Genera matriz de traslación 4x4."""
    # Retorna un arreglo 4x4. La última columna contiene los desplazamientos tx, ty, tz.
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])


def matriz_escalamiento(sx, sy, sz):
    """Genera matriz de escalamiento 4x4."""
    # Retorna un arreglo 4x4. La diagonal principal contiene los factores de escala sx, sy, sz.
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_x(theta):
    """Genera matriz de rotación sobre el eje X."""
    # Convierte el ángulo ingresado de grados a radianes (numpy usa radianes por defecto)
    rad = np.radians(theta)
    # Calcula el coseno y seno del ángulo una sola vez para optimizar
    c, s = np.cos(rad), np.sin(rad)
    # Devuelve la matriz estándar de rotación en el eje X
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_y(theta):
    """Genera matriz de rotación sobre el eje Y."""
    rad = np.radians(theta)
    c, s = np.cos(rad), np.sin(rad)
    # Devuelve la matriz estándar de rotación en el eje Y
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_z(theta):
    """Genera matriz de rotación sobre el eje Z."""
    rad = np.radians(theta)
    c, s = np.cos(rad), np.sin(rad)
    # Devuelve la matriz estándar de rotación en el eje Z
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


# ==========================================
# --- Catálogo de Figuras Precargadas ---
# ==========================================
# Diccionario que almacena la información de las 4 figuras requeridas.
FIGURAS = {
    "1": {
        "nombre": "Cubo (5x5x5)",
        # 'vertices': Lista de listas. Cada sublista es un punto [x, y, z, w].
        # El '1' final es la coordenada homogénea obligatoria para multiplicar por matrices 4x4.
        "vertices": [
            [0, 0, 0, 1], [5, 0, 0, 1], [5, 5, 0, 1], [0, 5, 0, 1],  # Base inferior (índices 0 al 3)
            [0, 0, 5, 1], [5, 0, 5, 1], [5, 5, 5, 1], [0, 5, 5, 1]  # Base superior (índices 4 al 7)
        ],
        # 'aristas': Lista de tuplas. Indica qué vértices deben conectarse con una línea al dibujar.
        # Por ejemplo, (0,1) indica que se dibujará una línea entre el vértice 0 y el vértice 1.
        "aristas": [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Conexiones de la base inferior
            (4, 5), (5, 6), (6, 7), (7, 4),  # Conexiones de la base superior
            (0, 4), (1, 5), (2, 6), (3, 7)  # Conexiones verticales (postes)
        ]
    },
    "2": {
        "nombre": "Pirámide Cuadrangular",
        "vertices": [
            [0, 0, 0, 1], [4, 0, 0, 1], [4, 4, 0, 1], [0, 4, 0, 1],
            [2, 2, 6, 1]  # Cúspide
        ],
        "aristas": [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (0, 4), (1, 4), (2, 4), (3, 4)
        ]
    },
    "3": {
        "nombre": "Paralelepípedo (2x6x3)",
        "vertices": [
            [0, 0, 0, 1], [2, 0, 0, 1], [2, 6, 0, 1], [0, 6, 0, 1],
            [0, 0, 3, 1], [2, 0, 3, 1], [2, 6, 3, 1], [0, 6, 3, 1]
        ],
        "aristas": [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
    },
    "4": {
        "nombre": "Prisma Triangular",
        "vertices": [
            [0, 0, 0, 1], [4, 0, 0, 1], [2, 3, 0, 1],
            [0, 0, 5, 1], [4, 0, 5, 1], [2, 3, 5, 1]
        ],
        "aristas": [
            (0, 1), (1, 2), (2, 0),
            (3, 4), (4, 5), (5, 3),
            (0, 3), (1, 4), (2, 5)
        ]
    }
}


# ==========================================
# --- Función de Graficación Avanzada ---
# ==========================================

def graficar_figuras(vertices_orig, vertices_trans, aristas, nombre_figura):
    """Genera un espacio 3D trazando los vértices y las aristas para formar las figuras."""

    # Crea una ventana de figura (lienzo) con un tamaño de 10 por 7 pulgadas
    fig = plt.figure(figsize=(10, 7))
    # Añade un sistema de ejes (axes) proyectado en 3 dimensiones a la figura
    ax = fig.add_subplot(111, projection='3d')

    # Utiliza "list comprehensions" (comprensión de listas) para separar las coordenadas.
    # Recorre cada vértice original (v) y extrae todos los valores X (índice 0), Y (índice 1) y Z (índice 2)
    x_orig, y_orig, z_orig = [v[0] for v in vertices_orig], [v[1] for v in vertices_orig], [v[2] for v in vertices_orig]
    # Hace exactamente lo mismo, pero para los vértices que ya fueron transformados por las matrices
    x_trans, y_trans, z_trans = [v[0] for v in vertices_trans], [v[1] for v in vertices_trans], [v[2] for v in
                                                                                                 vertices_trans]

    # Dibuja los vértices originales como puntos sueltos (scatter) en color azul (s=40 es el tamaño del punto)
    ax.scatter(x_orig, y_orig, z_orig, c='blue', s=40, label='Original')
    # Dibuja los vértices transformados como puntos sueltos en color rojo
    ax.scatter(x_trans, y_trans, z_trans, c='red', s=40, label='Transformada')

    # Bucle que recorre la lista de aristas para dibujar el "esqueleto" (las líneas) de la figura
    for arista in aristas:
        # Extrae los dos índices de la tupla (ej. p1=0, p2=1)
        p1, p2 = arista

        # Dibuja una línea conectando p1 y p2 de la figura ORIGINAL
        # Se dibuja punteada ('--') y semi-transparente (alpha=0.4) para diferenciarla
        ax.plot3D([x_orig[p1], x_orig[p2]], [y_orig[p1], y_orig[p2]], [z_orig[p1], z_orig[p2]],
                  color='blue', linestyle='--', alpha=0.4)

        # Dibuja una línea sólida (linewidth=2) conectando p1 y p2 de la figura TRANSFORMADA
        ax.plot3D([x_trans[p1], x_trans[p2]], [y_trans[p1], y_trans[p2]], [z_trans[p1], z_trans[p2]],
                  color='red', linewidth=2)

    # Añade etiquetas descriptivas a los 3 ejes del plano
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    # Coloca un título dinámico que incluye el nombre de la figura elegida
    ax.set_title(f'Transformación 3D: {nombre_figura}')
    # Muestra el cuadro de texto indicando qué es azul y qué es rojo (la leyenda)
    ax.legend()

    # --- Cálculo de límites dinámicos de la cámara ---
    # Para que la cámara 3D no "aplaste" o deforme la figura, se calculan límites cuadrados.
    # Junta todas las X, Y y Z (originales y transformadas) en listas únicas
    todos_x = x_orig + x_trans
    todos_y = y_orig + y_trans
    todos_z = z_orig + z_trans

    # Calcula cuál es la distancia máxima de apertura en los 3 ejes
    rango = max(max(todos_x) - min(todos_x), max(todos_y) - min(todos_y), max(todos_z) - min(todos_z)) / 2.0

    # Calcula el punto central (mid) de todos los puntos en el espacio
    mid_x = (max(todos_x) + min(todos_x)) * 0.5
    mid_y = (max(todos_y) + min(todos_y)) * 0.5
    mid_z = (max(todos_z) + min(todos_z)) * 0.5

    # Fija los límites de visualización de los ejes basados en el centro +- el rango calculado
    ax.set_xlim(mid_x - rango - 1, mid_x + rango + 1)
    ax.set_ylim(mid_y - rango - 1, mid_y + rango + 1)
    ax.set_zlim(mid_z - rango - 1, mid_z + rango + 1)

    # Despliega la ventana gráfica en pantalla e interactúa con el usuario
    plt.show()


# ==========================================
# --- Lógica Principal del Programa ---
# ==========================================

def main():
    # Impresión del encabezado decorativo en la consola
    print("=" * 50)
    print("      SISTEMA DE TRANSFORMACIÓN DE FIGURAS 3D")
    print("=" * 50)

    # --- 1. Menú de Selección de Figura ---
    print("\nFiguras Disponibles:")
    # Recorre el diccionario FIGURAS imprimiendo la clave (1,2,3,4) y el nombre correspondiente
    for clave, datos in FIGURAS.items():
        print(f" [{clave}] - {datos['nombre']}")

    # Solicita al usuario teclear el número de la figura
    opcion = input("\nSelecciona el número de la figura (1-4): ")

    # Si ingresa algo distinto a "1", "2", "3" o "4", el programa muestra error y se detiene (return)
    if opcion not in FIGURAS:
        print("Opción inválida. El programa terminará.")
        return

    # Extrae todos los datos de la figura seleccionada
    fig_seleccionada = FIGURAS[opcion]
    nombre_figura = fig_seleccionada["nombre"]
    aristas = fig_seleccionada["aristas"]

    # Convierte las listas de coordenadas puras de Python en arreglos de numpy (np.array),
    # paso obligatorio para poder aplicar las multiplicaciones de matrices después.
    vertices = [np.array(v) for v in fig_seleccionada["vertices"]]

    print(f"\n>> Has seleccionado: {nombre_figura} ({len(vertices)} vértices)")

    # --- 2. Captura de Parámetros ---
    # Solicita los datos numéricos al usuario. La estructura `input() or 0` permite que
    # si el usuario solo presiona Enter, el valor tome un "0" por defecto (para traslación y rotación).
    print("\n--- Parámetros de Traslación ---")
    tx = float(input(" Traslación en X: ") or 0)
    ty = float(input(" Traslación en Y: ") or 0)
    tz = float(input(" Traslación en Z: ") or 0)

    # Para el escalamiento, el valor por defecto es "1" (escala original)
    print("\n--- Parámetros de Escalamiento ---")
    sx = float(input(" Escalamiento en X (Default 1): ") or 1)
    sy = float(input(" Escalamiento en Y (Default 1): ") or 1)
    sz = float(input(" Escalamiento en Z (Default 1): ") or 1)

    print("\n--- Parámetros de Rotación (en grados) ---")
    ang_x = float(input(" Ángulo en X: ") or 0)
    ang_y = float(input(" Ángulo en Y: ") or 0)
    ang_z = float(input(" Ángulo en Z: ") or 0)

    # --- 3. Pipeline de Transformación (Construcción Matricial) ---
    # Manda llamar a las funciones definidas arriba para generar cada una de las 5 matrices 4x4
    M_esc = matriz_escalamiento(sx, sy, sz)
    M_rotX = matriz_rotacion_x(ang_x)
    M_rotY = matriz_rotacion_y(ang_y)
    M_rotZ = matriz_rotacion_z(ang_z)
    M_tras = matriz_traslacion(tx, ty, tz)

    # Crea la Matriz Final de Transformación.
    # El símbolo '@' en numpy realiza multiplicación de matrices (producto punto).
    # La matemática de graficación indica que se debe aplicar de derecha a izquierda:
    # Primero se escala, luego se rota, finalmente se traslada.
    M_final = M_tras @ M_rotZ @ M_rotY @ M_rotX @ M_esc

    # --- 4. Cálculo de Resultados (Presentación) ---
    print("\n" + "=" * 50)
    print("           RESULTADOS DE LA TRANSFORMACIÓN")
    print("=" * 50)

    # Crea una lista vacía para almacenar los vértices ya modificados
    vertices_transformados = []

    # Recorre cada vértice original extrayendo su índice (i) y su valor (v)
    for i, v in enumerate(vertices):
        # Multiplica la Matriz Final por el vértice actual para obtener sus nuevas coordenadas
        v_trans = M_final @ v
        # Guarda el vértice transformado en la lista para usarlo en la gráfica más adelante
        vertices_transformados.append(v_trans)

        # Redondea a 2 decimales solo para imprimir los valores limpiamente en pantalla.
        # Usa 'v[:3]' para tomar solo X, Y, Z e ignorar el '1' homogéneo final.
        o_x, o_y, o_z = np.round(v[:3], 2)
        r_x, r_y, r_z = np.round(v_trans[:3], 2)

        # Imprime los datos del vértice usando f-strings.
        # ':5.1f' significa que reserva 5 espacios y muestra 1 decimal (alinea las columnas en la consola)
        print(
            f" Vértice {i + 1:02d} | Original: ({o_x:5.1f}, {o_y:5.1f}, {o_z:5.1f})  -->  Transformado: ({r_x:6.2f}, {r_y:6.2f}, {r_z:6.2f})")

    # --- 5. Visualización ---
    print("\nGenerando entorno 3D... (Cierra la ventana para terminar)")
    # Llama a la función de graficación, pasándole los datos listos para dibujar
    graficar_figuras(vertices, vertices_transformados, aristas, nombre_figura)


# Esta validación de Python se asegura que el código principal solo se ejecute
# si este archivo se corre directamente, no si se importa como módulo en otro programa.
if __name__ == "__main__":
    main()