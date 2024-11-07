from spolygon import spolygon


class PolygonalVariables(dict):
    pass

def psymbolic(pdata, vertices):
    if not isinstance(pdata, dict) or 'center' not in pdata or 'radius' not in pdata:
        raise ValueError('Insert an object of the class paggregated')
    
    if vertices <= 2:
        raise ValueError("Insert the number of vertices greater than 2!")
    
    psdata = PolygonalVariables()

    # Verificar se 'center' é um vetor ou matriz
    if isinstance(pdata['center'], np.ndarray):
        if pdata['center'].ndim == 1:  # Caso seja um vetor
            m = len(pdata['center'])
            initial = [None] * m
            for i in range(m):
                initial[i] = spolygon(pdata['center'][i], pdata['radius'][i], vertices)
            psdata['X1'] = initial
        
        elif pdata['center'].ndim == 2:  # Caso seja uma matriz
            m, p = pdata['center'].shape
            initial = [None] * m
            variables = [f'X{i+1}' for i in range(p)]
            
            for j in range(p):
                for i in range(m):
                    initial[i] = spolygon(pdata['center'][i, j], pdata['radius'][i, j], vertices)
                psdata[variables[j]] = initial.copy()
            
            # Se for um DataFrame, pegar os nomes das colunas
            variables_names = pdata.get('center').columns if isinstance(pdata['center'], pd.DataFrame) else None
            if variables_names is not None:
                psdata = {variables_names[i]: psdata[variables[i]] for i in range(p)}
        else:
            raise ValueError('Insert a matrix or vector for center and radius!')
    else:
        raise ValueError('Insert a matrix, data.frame or vector for center and radius!')

    return psdata

# Exemplo de uso corrigido
if __name__ == "__main__":
    import numpy as np
    import pandas as pd

    # Exemplo 1: Obtendo uma variável poligonal simbólica simples
    cat1 = pd.Categorical(np.random.choice(range(1, 21), 1000, replace=True))
    cv1 = np.random.uniform(size=1000)
    pol1 = {'center': cv1, 'radius': np.random.uniform(size=1000)}  # Objeto 'paggregated' exemplo
    out = psymbolic(pol1, 6)  # Hexágono
    print(out['X1'])

    # Exemplo 2: Obtendo três (ou mais) variáveis poligonais simbólicas
    cat2 = pd.Categorical(np.random.choice(range(1, 21), 1000, replace=True))
    cv2 = np.random.uniform(size=(1000, 3))
    pol2 = {'center': cv2, 'radius': np.random.uniform(size=(1000, 3))}  # Objeto 'paggregated' exemplo
    out2 = psymbolic(pol2, 8)  # Octógono
    print(out2['X1'])
    print(out2['X2'])
    print(out2['X3'])
