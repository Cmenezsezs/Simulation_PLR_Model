import numpy as np

# Função para calcular o segundo momento interno de um polígono
def psmi(polygon):
    # Verificar se o polígono tem pelo menos 3 vértices
    if polygon.shape[0] < 3:
        raise ValueError("Insert a valid polygon!")
    
    # Extrair as coordenadas x (a) e y (b) dos vértices do polígono
    a = polygon[:, 0]
    b = polygon[:, 1]
    
    # Inicializar as variáveis de soma e área
    sumX = sum1X = sumY = sum1Y = area1 = area2 = 0
    
    # Iterar sobre os vértices do polígono
    for i in range(len(a)):
        if i < len(a) - 1:
            # Cálculo para vértices consecutivos
            sumX += (a[i]**2 + a[i] * a[i + 1] + a[i + 1]**2) * (a[i] * b[i + 1] - a[i + 1] * b[i])
            sumY += (b[i]**2 + b[i] * b[i + 1] + b[i + 1]**2) * (a[i] * b[i + 1] - a[i + 1] * b[i])
            area1 += 0.5 * (a[i] * b[i + 1] - a[i + 1] * b[i])
        else:
            # Cálculo para o último vértice em relação ao primeiro
            sum1X += (a[i]**2 + a[i] * a[0] + a[0]**2) * (a[i] * b[0] - a[0] * b[i])
            sum1Y += (b[i]**2 + b[i] * b[0] + b[0]**2) * (a[i] * b[0] - a[0] * b[i])
            area2 += 0.5 * (a[i] * b[0] - a[0] * b[i])
    
    # Calcular a área total
    area = area1 + area2
    
    # Retornar o segundo momento interno
    return np.abs(np.array([sumX + sum1X, sumY + sum1Y]) / (12 * area))

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de polígono com 3 lados (triângulo)
    x = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])
    moment = psmi(x)
    print("Second moment:", moment)
