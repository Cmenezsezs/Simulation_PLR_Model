# Extrair valores ajustados do modelo de regressão linear poligonal
# 
# Descrição: A função é usada para calcular o centro ajustado e o raio ou os polígonos ajustados
# a partir do modelo de regressão linear poligonal.
# 
# Parâmetros:
# - object: um objeto da classe "plr".
# - ...: outros argumentos que métodos especiais possam requerer.
# - polygon: booleano. Se FALSE, a função retorna o centro e o raio previstos para o polígono.
#            Se TRUE, a função retorna um objeto da classe "Polygonal" representando os polígonos ajustados.
# - vertices: Se polygon for TRUE, um número de vértices deve ser definido.
#             Além disso, o número de vértices deve ser maior que 2 e igual ao número de vértices
#             escolhido nas variáveis simbólicas poligonais.
# 
# Retorno:
# - ans: os valores ajustados para a regressão linear poligonal.

from spolygon import spolygon


def fitted_plr(object, polygon=False, vertices=None, **kwargs):
    n = len(object['fitted.values'])
    
    if n % 2 != 0:
        raise ValueError('O número de centros ajustados é diferente do número de valores de raio!')
    
    nc = n // 2
    nr = n // 2
    center_idx = list(range(nc))
    
    # Se polygon for False, retorna os valores ajustados (centro e raio)
    if not polygon:
        ans = object['fitted.values']
    else:
        if vertices is None or vertices < 3:
            raise ValueError('Insira um número válido de vértices!')
        
        # Extrai centros e raios ajustados
        fitted_center = object['fitted.values'][:nc]
        fitted_radius = object['fitted.values'][nc:]
        ans = [None] * nc
        
        # Gera os polígonos ajustados com base nos centros e raios
        for i in range(nc):
            ans[i] = spolygon(fitted_center[i], fitted_radius[i], vertices)
        
        # Define a classe do objeto como 'polygonal'
        ans = {'class': 'polygonal', 'polygons': ans}
    
    return ans
