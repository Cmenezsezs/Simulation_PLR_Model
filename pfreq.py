import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

# Função para calcular a frequência relativa simbólica poligonal
# 
# Parâmetros:
# - pol: Uma lista de matrizes, onde cada matriz representa um polígono (lados x 2).
#
# Retorno:
# - Retorna a frequência relativa bivariada.
def pfreq(pol):
    nr = len(pol)
    nv = len(pol[0])

    # Criação das matrizes para armazenar as coordenadas dos polígonos
    pol1 = np.zeros((nv, nr))
    pol2 = np.zeros((nv, nr))

    # Preenchendo as matrizes pol1 e pol2 com coordenadas x e y
    for temp in range(nr):
        pol1[:, temp] = pol[temp][:, 0]
        pol2[:, temp] = pol[temp][:, 1]

    # Determinando os valores mínimos e máximos de X e Y
    minX = np.min(pol1)
    maxX = np.max(pol1)
    minY = np.min(pol2)
    maxY = np.max(pol2)

    # Cálculo das razões de X e Y com base no número de polígonos
    ratioX = (maxX - minX) / nr
    ratioY = (maxY - minY) / nr

    # Criação de uma lista para armazenar os retângulos gerados
    rectangles = []
    for j in range(nr):
        for i in range(nr):
            rectangles.append(np.array([
                [minX + (i-1)*ratioX, minY + (j-1)*ratioY],
                [minX + (i-1)*ratioX, minY + j*ratioY],
                [minX + i*ratioX, minY + j*ratioY],
                [minX + i*ratioX, minY + (j-1)*ratioY]
            ]))

    len_rectangles = len(rectangles)

    # Matriz de frequência
    frequency = np.zeros((nr, len_rectangles))

    # Cálculo da interseção entre os polígonos e os retângulos
    for k in range(nr):
        p1 = Polygon(pol[k])

        # Verifica se o polígono é válido; caso contrário, corrige-o
        if not p1.is_valid:
            p1 = p1.buffer(0)

        for l in range(len_rectangles):
            p2 = Polygon(rectangles[l])

            # Verifica a interseção entre os polígonos e os retângulos
            gI = p1.intersection(p2)
            if not gI.is_empty:
                frequency[k, l] = gI.area / p1.area

    # Transposta da matriz de frequência
    frequency = frequency.T

    # Somatório por linha e cálculo da frequência relativa
    frequency = np.sum(frequency, axis=1).reshape(-1, nr)
    relative_frequency_temp = frequency / nr

    return relative_frequency_temp

# Exemplo de uso
if __name__ == "__main__":
    # Simulação de 10 polígonos com 10 lados (exemplo fictício)
    polygons = [np.random.rand(10, 2) for _ in range(10)]  # Lista de 10 polígonos com coordenadas aleatórias

    # Calcula a frequência relativa poligonal
    frequency = pfreq(polygons)
    print(f"Frequência relativa: \n{frequency}")
