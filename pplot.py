import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from pmean_id import pmean_id

# Função para plotar as variáveis poligonais simbólicas
def pplot(polygon_list, center=False, color='black'):
    fig, ax = plt.subplots()

    # Remover colunas nomeadas (não aplicável em Python como em R, mas preservado aqui)
    polygons = [np.array(p) for p in polygon_list]
    
    # Plota todos os polígonos sobrepostos
    for poly in polygons:
        poly_patch = Polygon(poly, edgecolor='black', fill=None)
        ax.add_patch(poly_patch)

    # Configurações dos eixos
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    
    # Caso center seja True, plota os centros dos polígonos
    if center:
        centers = np.array([pmean_id(p) for p in polygons])
        ax.scatter(centers[:, 0], centers[:, 1], c=color)

    ax.autoscale()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    # Simulação de polígonos (exemplo fictício)
    polygons = [np.random.rand(10, 2) for _ in range(10)]  # 10 polígonos com 10 lados cada
    
    # Plotar os polígonos, exibindo o centro de cada um
    pplot(polygons, center=True, color='red')
