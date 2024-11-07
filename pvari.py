import numpy as np

def pvari(polygon):
    """
    Calcula a variância interna simbólica de um polígono.
    
    Parâmetros:
    polygon - Matriz que representa uma variável poligonal.
    
    Retorno:
    A variância interna simbólica.
    """
    if polygon.shape[0] < 3:
        raise ValueError("Insira um polígono válido!")
    
    # Primeiro momento (média)
    first_moment = pmean_id(polygon)
    
    # Segundo momento
    second_moment = psmi(polygon)
    
    # Variância interna
    x = second_moment[0] - first_moment[0] ** 2
    y = second_moment[1] - first_moment[1] ** 2
    
    return np.array([x, y])

# Exemplo de uso
if __name__ == "__main__":
    # Simulando 10 polígonos de 10 lados
    def psim(num_polygons, num_sides):
        # Função para simular polígonos com `num_polygons` e `num_sides` lados
        return [np.random.rand(num_sides, 2) for _ in range(num_polygons)]

    # Simulando 10 polígonos de 10 lados
    polygons = psim(10, 10)
    
    # Calculando a variância interna simbólica do primeiro polígono
    internal_variance = pvari(polygons[0])
    print("Variância interna simbólica:", internal_variance)
