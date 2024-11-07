import numpy as np

from parea import parea

def rmsea(observed, fitted):
    """
    Erro quadrático médio da área (RMSEA).
    
    Descrição:
    O erro quadrático médio da área (RMSEA) é uma métrica proposta por Silva et al. (2019).
    Ele é utilizado para avaliar o desempenho do modelo de regressão poligonal simbólica.
    
    Parâmetros:
    observed - Variável resposta do modelo de regressão poligonal.
    fitted - Polígonos ajustados obtidos como valores ajustados da variável resposta.
    
    Retorno:
    rmsea - O valor do erro quadrático médio da área.
    
    Referências:
    Silva, W.J.F, Souza, R.M.C.R, Cysneiros, F.J.A. (2019). 
    URL: https://www.sciencedirect.com/science/article/pii/S0950705118304052.
    """
    observed_areas = np.array([parea(polygon) for polygon in observed])
    fitted_areas = np.array([parea(polygon) for polygon in fitted])
    
    return np.sqrt(np.mean((observed_areas - fitted_areas) ** 2))

# Exemplo de uso
if __name__ == "__main__":
    """
    Exemplo:
    Simule 10 polígonos de 10 lados e ajuste o modelo de regressão poligonal.
    """
    # Função para simular polígonos com `num_polygons` e `num_sides` lados
    def psim(num_polygons, num_sides):
        return [np.random.rand(num_sides, 2) for _ in range(num_polygons)]
    
    # Simulando 10 polígonos de 10 lados
    yp = psim(10, 10)  # Variável resposta
    xp1 = psim(10, 10)  # Primeiro preditor
    xp2 = psim(10, 10)  # Segundo preditor

    # Supondo que `plr` seja o modelo de regressão poligonal linear
    # e `fitted` retorne os valores ajustados (fitted) como polígonos
    def plr(formula, data_env):
        # Função hipotética para ajustar um modelo de regressão poligonal linear
        # Implementar a lógica de regressão aqui
        pass
    
    def fitted(fit_model, polygon=True, vertices=10):
        # Função hipotética que retorna os valores ajustados pelo modelo `fit_model`
        # Implementar a lógica para retornar os polígonos ajustados aqui
        return psim(10, vertices)  # Simulando polígonos ajustados como exemplo

    # Ambiente de dados simulados
    e = {'yp': yp, 'xp1': xp1, 'xp2': xp2}

    # Ajuste do modelo de regressão poligonal linear (hipotético)
    fit = plr('yp ~ xp1 + xp2 - 1', e)
    
    # Obtendo os polígonos ajustados pelo modelo
    yp_fitted = fitted(fit, polygon=True, vertices=10)

    # Calculando o RMSEA
    rmsea_value = rmsea(yp, yp_fitted)
    print("RMSEA:", rmsea_value)
