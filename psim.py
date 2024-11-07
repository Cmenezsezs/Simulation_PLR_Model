import numpy as np

from spolygon import spolygon

# Função para simular um polígono
def psim(n, vertices):
    # Gera centros aleatórios entre -1 e 1
    center = np.random.uniform(-1, 1, n)
    # Gera raios aleatórios positivos
    radius = np.random.uniform(0, 1, n)
    
    # Verificações de validade para centro e raio
    if not isinstance(center, np.ndarray):
        raise ValueError('Insert a vector for center!')
    if not isinstance(radius, np.ndarray):
        raise ValueError('Insert a vector for radius!')
    if len(center) != len(radius):
        raise ValueError('Insert center and radius vectors with the same size!')
    
    objects = len(center)
    
    # Verificações de validade para número de vértices e objetos
    if vertices <= 2:
        raise ValueError("Insert a vertex number greater than 2")
    if objects < 1:
        raise ValueError("Insert a valid number of objects")
    if np.min(radius) <= 0:
        raise ValueError('Insert radius greater than 0!')
    
    # Lista para armazenar os polígonos gerados
    polygons = []
    
    # Gera os polígonos usando a função spolygon
    for i in range(objects):
        polygons.append(spolygon(center[i], radius[i], vertices))
    
    # Retorna a lista de polígonos
    return polygons

# Exemplo de uso
if __name__ == "__main__":
    number_polygons = 10
    vertices = 4
    polygons = psim(number_polygons, vertices)
    
    for i, polygon in enumerate(polygons):
        print(f"Polygon {i + 1}:")
        print(polygon)
        print()
