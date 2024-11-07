import numpy as np


def pvar(polygons):
    """
    Calcula a variância simbólica poligonal a partir de uma lista de polígonos.
    
    Parâmetros:
    polygons - Lista de matrizes de dimensão l x 2, onde l representa o número de lados do polígono.
    
    Retorno:
    Um vetor bi-dimensional que representa a variância simbólica.
    """
    if len(polygons) < 1:
        raise ValueError("Insira um número válido de polígonos!")
    
    # Primeiro momento (média dos polígonos)
    first_moment = pmean(polygons)
    
    # Segundo momento (usando a função psmi)
    second_moment = np.array([psmi(polygon) for polygon in polygons]).T
    
    # Média dos segundos momentos
    sm = np.array([np.mean(second_moment[0, :]), np.mean(second_moment[1, :])])
    
    # Variância simbólica
    x = sm[0] - first_moment[0] ** 2
    y = sm[1] - first_moment[1] ** 2
    
    return np.array([x, y])

# Exemplo de uso
if __name__ == "__main__":
    # Supondo que a função psim esteja definida para gerar os polígonos
    def psim(num_polygons, num_sides):
        # Simulação de polígonos com `num_polygons` polígonos e `num_sides` lados.
        return [np.random.rand(num_sides, 2) for _ in range(num_polygons)]

    # Simulando 8 polígonos de 12 lados
    polygons = psim(8, 12)
    
    # Calculando a variância simbólica dos polígonos
    variance = pvar(polygons)
    print("Variância simbólica:", variance)