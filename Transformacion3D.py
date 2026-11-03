import numpy as np


# --- Matrices de Transformación ---

def matriz_traslacion(tx, ty, tz):
    """Genera matriz de traslación 4x4."""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])


def matriz_escalamiento(sx, sy, sz):
    """Genera matriz de escalamiento 4x4."""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_x(theta_grados):
    """Genera matriz de rotación sobre el eje X[cite: 5]."""
    rad = np.radians(theta_grados)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_y(theta_grados):
    """Genera matriz de rotación sobre el eje Y[cite: 5]."""
    rad = np.radians(theta_grados)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])


def matriz_rotacion_z(theta_grados):
    """Genera matriz de rotación sobre el eje Z[cite: 2, 5]."""
    rad = np.radians(theta_grados)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


# --- Lógica Principal del Programa ---

def main():
    print("=== Transformación de Figuras 3D ===")

    # 1. Captura de vértices
    n_vertices = int(input("¿Cuántos vértices tiene tu figura? "))
    vertices = []

    print("\nIngresa las coordenadas (x, y, z) de cada vértice:")
    # Puedes usar coordenadas de prueba como (0,0,0) o (5,5,5)
    for i in range(n_vertices):
        coords = input(f"Vértice {i + 1} (separado por espacios, ej. 5 0 5): ").split()
        x, y, z = float(coords[0]), float(coords[1]), float(coords[2])
        # Almacenar como coordenada homogénea [x, y, z, 1]
        vertices.append(np.array([x, y, z, 1.0]))

    # 2. Captura de parámetros de transformación
    print("\n--- Parámetros de Traslación ---")
    tx = float(input("Traslación en X: "))
    ty = float(input("Traslación en Y: "))
    tz = float(input("Traslación en Z: "))

    print("\n--- Parámetros de Escalamiento ---")
    sx = float(input("Escalamiento en X (1 = sin cambio): "))
    sy = float(input("Escalamiento en Y (1 = sin cambio): "))
    sz = float(input("Escalamiento en Z (1 = sin cambio): "))

    print("\n--- Parámetros de Rotación (en grados) ---")
    ang_x = float(input("Ángulo de rotación en X: "))
    ang_y = float(input("Ángulo de rotación en Y: "))
    ang_z = float(input("Ángulo de rotación en Z: "))

    # 3. Construcción del Pipeline de Matrices
    # El orden estándar para graficación suele ser Escalar -> Rotar -> Trasladar
    M_esc = matriz_escalamiento(sx, sy, sz)
    M_rotX = matriz_rotacion_x(ang_x)
    M_rotY = matriz_rotacion_y(ang_y)
    M_rotZ = matriz_rotacion_z(ang_z)
    M_tras = matriz_traslacion(tx, ty, tz)

    # Multiplicación matricial (se aplica de derecha a izquierda)
    M_final = M_tras @ M_rotZ @ M_rotY @ M_rotX @ M_esc

    # 4. Aplicación de las transformaciones
    print("\n=== Resultados de la Transformación ===")
    for i, v in enumerate(vertices):
        v_transformado = M_final @ v
        # Extraer solo x, y, z
        res_x, res_y, res_z = np.round(v_transformado[:3], 4)
        print(f"Vértice {i + 1} original: ({v[0]}, {v[1]}, {v[2]}) -> Transformado: ({res_x}, {res_y}, {res_z})")


if __name__ == "__main__":
    main()