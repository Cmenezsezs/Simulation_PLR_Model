import pandas as pd
import numpy as np

# Agregação de dados poligonais
#
# Descrição: A função obtém dados simbólicos a partir de dados clássicos através da representação de centro e raio.
#
# Parâmetros:
# - data: Um DataFrame com a primeira coluna do tipo fator (categoria).
#
# Retorno:
# - paggreg: Retorna um objeto da classe "paggregated".

def paggreg(data):
    # Verifica se o input é um DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Insira um DataFrame!")
    
    # Verifica se a primeira coluna é de tipo categoria
    if not pd.api.types.is_categorical_dtype(data.iloc[:, 0]):
        raise ValueError("Insira uma coluna do tipo 'categoria' na primeira coluna!")
    
    # Conta a quantidade de elementos em cada categoria
    data_factor = data.iloc[:, 0].value_counts()
    
    # Verifica se todas as categorias possuem mais de um elemento
    if any(data_factor <= 1):
        raise ValueError("Insira dados com todas as categorias tendo mais de 1 observação!")
    
    # Calcula o centro (média) por categoria
    center = data.groupby(data.columns[0]).mean()
    
    # Calcula o raio (2 vezes o desvio padrão) por categoria
    radius = data.groupby(data.columns[0]).agg(lambda x: 2 * np.std(x))

    # Cria uma lista para armazenar os resultados
    pdata = [None, None]
    pdata[0] = center
    pdata[1] = radius

    # Define os nomes dos dados
    pdata_dict = {'center': pdata[0], 'radius': pdata[1]}
    
    # Define a classe do objeto como 'paggregated'
    pdata_dict['class'] = 'paggregated'
    
    return pdata_dict

# Exemplo de uso
if __name__ == "__main__":
    # Gera dados de exemplo
    categories = pd.Categorical(np.random.choice(range(1, 21), 1000, replace=True))
    classical_var = np.random.uniform(0, 1, 1000)
    df = pd.DataFrame({'category': categories, 'cv': classical_var})
    
    # Agrega os dados
    p = paggreg(df)
    print(p)
