
import numpy as np
import matplotlib.pyplot as plt


#Matrices de Transformación 3D


def matriz_traslacion(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])


def matriz_escalamiento(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_x(theta):
    rad = np.radians(theta)
    # Calcula el coseno y seno del ángulo una sola vez para optimizar
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_y(theta):
    rad = np.radians(theta)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_z(theta):
    rad = np.radians(theta)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])



# Figuras Precargadas
FIGURAS = {
    "1": {
        "nombre": "Cubo (5x5x5)",
        "vertices": [
            [0, 0, 0, 1], [5, 0, 0, 1], [5, 5, 0, 1], [0, 5, 0, 1],  # Base inferior (índices 0 al 3)
            [0, 0, 5, 1], [5, 0, 5, 1], [5, 5, 5, 1], [0, 5, 5, 1]  # Base superior (índices 4 al 7)
        ],
        "aristas": [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
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


# Graficación Avanzada

def graficar_figuras(vertices_orig, vertices_trans, aristas, nombre_figura):

    # Crea una ventana  con un tamaño de 10 por 7 pulgadas
    fig = plt.figure(figsize=(10, 7))
    # Añade  la figura
    ax = fig.add_subplot(111, projection='3d')

    x_orig, y_orig, z_orig = [v[0] for v in vertices_orig], [v[1] for v in vertices_orig], [v[2] for v in vertices_orig]

    x_trans, y_trans, z_trans = [v[0] for v in vertices_trans], [v[1] for v in vertices_trans], [v[2] for v in
                                                                                                 vertices_trans]

    ax.scatter(x_orig, y_orig, z_orig, c='blue', s=40, label='Original')
    ax.scatter(x_trans, y_trans, z_trans, c='red', s=40, label='Transformada')

    for arista in aristas:
        p1, p2 = arista
        ax.plot3D([x_orig[p1], x_orig[p2]], [y_orig[p1], y_orig[p2]], [z_orig[p1], z_orig[p2]],
                  color='blue', linestyle='--', alpha=0.4)

        ax.plot3D([x_trans[p1], x_trans[p2]], [y_trans[p1], y_trans[p2]], [z_trans[p1], z_trans[p2]],
                  color='red', linewidth=2)

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.set_title(f'Transformación 3D: {nombre_figura}')
    ax.legend()


    todos_x = x_orig + x_trans
    todos_y = y_orig + y_trans
    todos_z = z_orig + z_trans

    # Calcula cla distancia máxima de apertura en los 3 ejes
    rango = max(max(todos_x) - min(todos_x), max(todos_y) - min(todos_y), max(todos_z) - min(todos_z)) / 2.0

    # Calcula el punto central de todos los puntos en el espacio
    mid_x = (max(todos_x) + min(todos_x)) * 0.5
    mid_y = (max(todos_y) + min(todos_y)) * 0.5
    mid_z = (max(todos_z) + min(todos_z)) * 0.5

    ax.set_xlim(mid_x - rango - 1, mid_x + rango + 1)
    ax.set_ylim(mid_y - rango - 1, mid_y + rango + 1)
    ax.set_zlim(mid_z - rango - 1, mid_z + rango + 1)

    # Despliega la ventana gráfica en pantalla
    plt.show()



# Logica Principal del Programa


def main():
    print("      SISTEMA DE TRANSFORMACIÓN DE FIGURAS 3D")

    #  Menu de Selección de Figura
    print("\nFiguras Disponibles:")
    for clave, datos in FIGURAS.items():
        print(f" [{clave}] - {datos['nombre']}")

    # Solicita al usuario teclear el numero de la figura
    opcion = input("\nSelecciona el número de la figura (1-4): ")

    # Validar la respuesta
    if opcion not in FIGURAS:
        print("Opción inválida. El programa terminará.")
        return

    # Extrae todos los datos de la figura seleccionada
    fig_seleccionada = FIGURAS[opcion]
    nombre_figura = fig_seleccionada["nombre"]
    aristas = fig_seleccionada["aristas"]

    # Convierte las listas de coordenadas en arreglos de numpy
    vertices = [np.array(v) for v in fig_seleccionada["vertices"]]

    print(f"\n>> Has seleccionado: {nombre_figura} ({len(vertices)} vértices)")

    # Parametros
    # Solicita los datos al usuario
    print("\n--- Parámetros de Traslación ---")
    tx = float(input(" Traslación en X: ") or 0)
    ty = float(input(" Traslación en Y: ") or 0)
    tz = float(input(" Traslación en Z: ") or 0)

    # Para el escalamiento
    print("\n--- Parámetros de Escalamiento ---")
    sx = float(input(" Escalamiento en X (Default 1): ") or 1)
    sy = float(input(" Escalamiento en Y (Default 1): ") or 1)
    sz = float(input(" Escalamiento en Z (Default 1): ") or 1)

    print("\n--- Parámetros de Rotación (en grados) ---")
    ang_x = float(input(" Ángulo en X: ") or 0)
    ang_y = float(input(" Ángulo en Y: ") or 0)
    ang_z = float(input(" Ángulo en Z: ") or 0)

    # Transformación
    # Manda llamar a las funciones para generar cada una de las 5 matrices 4x4
    M_esc = matriz_escalamiento(sx, sy, sz)
    M_rotX = matriz_rotacion_x(ang_x)
    M_rotY = matriz_rotacion_y(ang_y)
    M_rotZ = matriz_rotacion_z(ang_z)
    M_tras = matriz_traslacion(tx, ty, tz)

    # Crea la Matriz Final de Transformación.
    # Primero se escala, luego se rota y al final se traslada.
    M_final = M_tras @ M_rotZ @ M_rotY @ M_rotX @ M_esc

    #  Resultados
    print("\n" + "=" * 50)
    print("           RESULTADOS DE LA TRANSFORMACIÓN")
    print("=" * 50)

    # Crea una lista vacia para almacenar los vertices modificados
    vertices_transformados = []

    # Recorre cada vértice original y agarra su índice (i) y su valor (v)
    for i, v in enumerate(vertices):
        # Multiplica la Matriz Final por el vértice actual para obtener sus nuevas coordenadas
        v_trans = M_final @ v
        # Guarda el vertice transformado en la lista para usarlo en la gráfica más adelante
        vertices_transformados.append(v_trans)

        # Redondea a 2 decimales
        o_x, o_y, o_z = np.round(v[:3], 2)
        r_x, r_y, r_z = np.round(v_trans[:3], 2)

        # Imprime los datos del vértice
        print(
            f" Vértice {i + 1:02d} | Original: ({o_x:5.1f}, {o_y:5.1f}, {o_z:5.1f})  -->  Transformado: ({r_x:6.2f}, {r_y:6.2f}, {r_z:6.2f})")

    # mostrar entorno
    print("\nGenerando entorno 3D... (Cierra la ventana para terminar)")
    # Llama a la función de graficacion
    graficar_figuras(vertices, vertices_transformados, aristas, nombre_figura)


if __name__ == "__main__":
    main()