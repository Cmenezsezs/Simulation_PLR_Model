import numpy as np

def spolygon(center, radius, vertices):
    """
    Polígono Simbólico
    
    Descrição:
    A função obtém um polígono simbólico simples a partir da representação de centro e raio.
    
    Parâmetros:
    center - Um número inteiro que representa o baricentro do polígono.
    radius - Um número inteiro que representa o raio do polígono.
    vertices - Representa o número de vértices do polígono.
    
    Retorno:
    Retorna uma matriz que representa o polígono.
    
    Exemplo de uso:
    spolygon(2.5, 3, 5) # Pentágono
    """
    
    # Verificações de entrada
    if vertices <= 2:
        raise ValueError("Insira um número de vértices maior que 2!")
    
    if radius < 0:
        raise ValueError("Insira um valor positivo para o raio!")
    
    elif radius == 0:
        raise ValueError("Polígono degenerado. Insira um valor positivo para o raio!")
    
    # Gerando os vértices do polígono
    i = np.arange(1, vertices + 1)
    
    # Coordenadas X e Y dos vértices
    x_coords = center + radius * np.cos(2 * np.pi * i / vertices)
    y_coords = center + radius * np.sin(2 * np.pi * i / vertices)
    
    # Retorna uma matriz (vertices x 2) com as coordenadas do polígono
    return np.column_stack((x_coords, y_coords))

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de pentágono com centro 2.5 e raio 3
    polygon = spolygon(2.5, 3, 5)
    print(polygon)
