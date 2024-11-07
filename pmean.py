import numpy as np

from pmean_id import pmean_id

# Função para calcular a média empírica simbólica poligonal
#
# Parâmetros:
# - polygons: Uma lista de matrizes, onde cada matriz representa um polígono (lados x 2).
#
# Retorno:
# - Um vetor contendo a média empírica simbólica poligonal nas duas dimensões.
def pmean(polygons):
    # Calcular o primeiro momento de cada polígono usando a função pmean_id
    first_moment = [pmean_id(polygon) for polygon in polygons]

    # Converter a lista de momentos em uma matriz (número de polígonos x 2)
    first_moment = np.array(first_moment)

    # Calcular a média das duas dimensões (primeira coluna para x, segunda para y)
    mean_x = np.mean(first_moment[:, 0])
    mean_y = np.mean(first_moment[:, 1])

    # Retorna a média nas duas dimensões
    return [mean_x, mean_y]

# Exemplo de uso
if __name__ == "__main__":
    # Simulação de 10 polígonos com 10 lados (exemplo fictício)
    polygons = [np.random.rand(10, 2) for _ in range(10)]  # Lista de 10 polígonos com coordenadas aleatórias

    # Calcula a média empírica poligonal
    mean_values = pmean(polygons)
    print(f"Média empírica poligonal: {mean_values}")
