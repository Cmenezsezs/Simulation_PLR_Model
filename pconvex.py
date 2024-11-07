import numpy as np

# Função para verificar a convexidade de um polígono
#
# Descrição: Verifica a convexidade de um polígono dado.
#
# Parâmetros:
# - polygon: Uma matriz com dimensão l x 2, onde l representa o número de lados do polígono.
#
# Retorno:
# - Retorna um valor booleano indicando se o polígono é convexo ou não.

def pconvex(polygon):
    # Verifica se o polígono tem pelo menos 3 vértices
    if polygon.shape[0] < 3:
        raise ValueError("Insira um polígono válido!")

    # Função auxiliar para calcular o comprimento do produto vetorial
    def cross_product_length(ax, ay, bx, by, cx, cy):
        BAx = ax - bx
        BAy = ay - by
        BCx = cx - bx
        BCy = cy - by
        return BAx * BCy - BAy * BCx

    # Número de vértices do polígono
    vertex_number = polygon.shape[0]

    # Função para testar cada tripla de vértices
    def test_for(a):
        b = (a + 1) % vertex_number
        c = (b + 1) % vertex_number
        return np.sign(cross_product_length(
            polygon[a, 0], polygon[a, 1],  # coordenadas do vértice a
            polygon[b, 0], polygon[b, 1],  # coordenadas do vértice b
            polygon[c, 0], polygon[c, 1]   # coordenadas do vértice c
        ))

    # Aplica o teste de convexidade para cada vértice
    signs = np.array([test_for(a) for a in range(vertex_number)])

    # Verifica se todos os sinais são iguais, o que indica que o polígono é convexo
    convex = np.all(signs == signs[0])

    return convex

# Exemplo de uso
if __name__ == "__main__":
    # Simula um polígono com 10 lados (exemplo fictício)
    x = np.random.rand(10, 2)  # Polígono de 10 lados com coordenadas aleatórias
    
    # Verifica se o polígono é convexo
    is_convex = pconvex(x)
    print(f"O polígono é convexo? {is_convex}")
