import numpy as np

# Função para calcular a área de um polígono
#
# Descrição: Calcula a área de um polígono dado.
#
# Parâmetros:
# - polygon: Uma matriz representando o polígono.
#
# Retorno:
# - Retorna um número inteiro representando a área do polígono.

def parea(polygon):
    # Verifica se a entrada é uma matriz numpy (equivalente à verificação de matriz em R)
    if not isinstance(polygon, np.ndarray) or polygon.ndim != 2 or polygon.shape[1] != 2:
        raise ValueError("Insira um polígono válido!")

    # Verifica se o polígono é degenerado (todos os valores são 0)
    if np.all(polygon == 0):
        print("Aviso: Polígono degenerado!")
        return 0
    
    # Separa as colunas da matriz (x, y)
    a = polygon[:, 0]
    b = polygon[:, 1]

    # Inicializa as áreas
    area1 = 0
    area2 = 0

    # Calcula a área utilizando a fórmula do polígono
    for i in range(len(a)):
        if i < len(a) - 1:
            area1 += a[i] * b[i + 1] - a[i + 1] * b[i]
        else:
            area2 += a[i] * b[0] - a[0] * b[i]

    # Calcula a área total
    area = 0.5 * (area1 + area2)

    # Verifica novamente se a área é 0, indicando um polígono degenerado
    if area == 0:
        print("Aviso: Polígono degenerado!")

    return abs(area)  # Retorna o valor absoluto da área para evitar áreas negativas

# Exemplo de uso
if __name__ == "__main__":
    # Simula 10 polígonos de 10 lados (exemplo fictício)
    x = np.random.rand(10, 2)  # Polígono de 10 lados com coordenadas aleatórias
    
    # Calcula a área do primeiro polígono
    area = parea(x)
    print(f"Área do polígono: {area}")
