from plr_model import plr
from psim import psim
import numpy as np
from scipy import stats

def summary_plr(object, digits=3):
    z = object
    ans = z.copy()  # Copiando o objeto original

    # Verificando a estrutura do modelo
    print("Estrutura do modelo:", z)  # Debugging

    n = len(z['model']['yc'])  # Número de observações
    p = z['rank']  # Posto (rank)

    rdf = n - p - 1  # Graus de liberdade
    r = z['residuals']  # Resíduos

    ans = {}  # Inicializa o dicionário de resposta
    ans['call'] = z['call']
    ans['aliased'] = [coef is None for coef in z['coefficients'].values()]  # Checa se os coeficientes são alias
    ans['residuals'] = r

    rss = np.sum(r ** 2)  # Soma dos resíduos ao quadrado
    resvar = rss / rdf if rdf > 0 else np.nan  # Variância dos resíduos
    ans['sigma'] = np.sqrt(resvar) if resvar > 0 else np.nan  # Desvio padrão

    if p == 0:
        ans['coefficients'] = {var: None for var in z['coefficients'].keys()}
        return ans

    f = z['fitted.values']  # Valores ajustados

    # Cálculo da matriz do modelo
    model_matrix = np.column_stack((np.ones(n), z['model']['xc']))

    # Erros padrão
    try:
        inv_matrix = np.linalg.pinv(model_matrix.T @ model_matrix)  # Usando pseudoinversa
        se = np.sqrt(np.maximum(np.diagonal(inv_matrix) * resvar, 0))  # Evita raízes de valores negativos
    except np.linalg.LinAlgError:
        print("Erro: A matriz do modelo é singular ou mal-condicionada. Não foi possível calcular erros padrão.")
        se = np.full(len(z['coefficients']), np.nan)  # Se não for possível calcular, preencha com NaN

    # Cálculo da estatística z
    coefficients = np.array(list(z['coefficients'].values())).flatten()
    se = np.resize(se, coefficients.shape)  # Ajusta se para ter o mesmo tamanho que coefficients
    zval = np.divide(coefficients, se, out=np.zeros_like(coefficients), where=se != 0)

    # Monta os coeficientes
    ans['coefficients'] = {
        'Estimate': coefficients,
        'Std. Error': np.nan_to_num(se),  # Substitui NaNs por zero para estabilidade
        'z value': np.nan_to_num(zval),
        'Pr(>|z|)': 2 * (1 - stats.norm.cdf(np.abs(zval)))  # P-valor para teste bicaudal
    }

    ans['terms'] = z['terms']
    return ans


# Exemplos de uso
#yp = psim(50, 10)  # Simular 10 polígonos de 3 lados
#xp1 = psim(50, 10)  # Simular 10 polígonos de 3 lados
#xp2 = psim(50, 10)  # Simular 10 polígonos de 3 lados
#e = {
    #'yc': yp,
    #'xc1': xp1,
    #'xc2': xp2
#}
#fit = plr(formula="yp ~ xp1 + xp2", data={"yp": yp, "xp1": xp1, "xp2": xp2})
#summary = summary_plr(fit)
#print(summary)



