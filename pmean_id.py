import numpy as np
from psim import psim

# Função para calcular a média empírica simbólica de um polígono
#
# Parâmetros:
# - polygon: Uma matriz representando o polígono, com coordenadas (lados x 2).
#
# Retorno:
# - A média empírica simbólica do polígono, nas duas dimensões (x e y).
# Função para calcular a média poligonal
def pmean_id(polygon):
    
    if not isinstance(polygon, np.ndarray) or polygon.ndim != 2:
        raise ValueError("O polígono deve ser uma matriz 2D.")

    if polygon.shape[0] < 3:
        raise ValueError("Insert a valid polygon!")
    
    a = polygon[:, 0]
    b = polygon[:, 1]
    sumX = 0
    sum1X = 0
    sumY = 0
    sum1Y = 0
    area1 = 0
    area2 = 0
    
    for i in range(len(a)):
        if i < len(a) - 1:
            sumX += (a[i] + a[i + 1]) * (a[i] * b[i + 1] - a[i + 1] * b[i])
            sumY += (b[i] + b[i + 1]) * (a[i] * b[i + 1] - a[i + 1] * b[i])
            area1 += (a[i] * b[i + 1] - a[i + 1] * b[i])
        else:
            sum1X += (a[i] + a[0]) * (a[i] * b[0] - a[0] * b[i])
            sumY += (b[i] + b[0]) * (a[i] * b[0] - a[0] * b[i])
            area2 += (a[i] * b[0] - a[0] * b[i])
    
    area = 0.5 * (area1 + area2)
    
    if area == 0:
        print("Area of one polygon is degenerated")
    else:
        return np.array([sumX + sum1X, sumY + sum1Y]) / (6 * area)

# Exemplo de uso
if __name__ == "__main__":
    # Gerar 10 polígonos com 4 vértices
    number_polygons = 10
    vertices = 4
    polygons = psim(number_polygons, vertices)
    
    # Calcular a média poligonal do primeiro polígono gerado
    first_polygon = polygons[0]
    mean_polygon = pmean_id(first_polygon)
    
    print("Primeiro polígono:")
    print(first_polygon)
    print("\nMédia poligonal do primeiro polígono:")
    print(mean_polygon)

