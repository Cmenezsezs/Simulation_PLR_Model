import numpy as np
import pandas as pd

def ptransform(data, vertices):
    # Verificação se o data é um DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Insira um dataframe!")

    # Verificação se a primeira coluna é do tipo categoria (factor)
    if not pd.api.types.is_categorical_dtype(data.iloc[:, 0]):
        raise ValueError("Insira uma categoria na primeira coluna!")

    data_factor = data.iloc[:, 0].value_counts()

    # Verificação se todos os fatores têm mais de 1 ocorrência
    if (data_factor <= 1).sum() != 0:
        raise ValueError("Insira dados com todos os fatores maiores que 1!")

    # Verificação se o número de vértices é maior que 2
    if vertices <= 2:
        raise ValueError("Insira o número de vértices maior que 2!")

    # Caso o número de colunas seja 3
    if data.shape[1] == 3:
        grouped_data = data.groupby(data.columns[0])
        number_polygons = len(grouped_data)

        # Calcula o centro e raio dos polígonos
        center = np.array(grouped_data.mean().to_numpy())
        radius = grouped_data.std().apply(lambda x: 2 * np.max(np.abs(x)), axis=1).to_numpy()

        polygons1 = []
        for i in range(number_polygons):
            polygons = np.zeros((vertices, 2))
            for j in range(vertices):
                polygons[j, 0] = center[i, 0] + radius[i] * np.cos(2 * np.pi * j / vertices)
                polygons[j, 1] = center[i, 1] + radius[i] * np.sin(2 * np.pi * j / vertices)
            polygons1.append(polygons)

    # Caso o número de colunas seja 2
    elif data.shape[1] == 2:
        grouped_data = data.groupby(data.columns[0])
        center = grouped_data.mean().to_numpy().flatten()
        radius = (2 * grouped_data.std().to_numpy().flatten())

        polygons1 = []
        for i in range(len(center)):
            polygons = np.zeros((vertices, 2))
            for j in range(vertices):
                polygons[j, 0] = center[i] + radius[i] * np.cos(2 * np.pi * j / vertices)
                polygons[j, 1] = center[i] + radius[i] * np.sin(2 * np.pi * j / vertices)
            polygons1.append(polygons)

    else:
        raise ValueError("Insira um conjunto de dados válido!")

    return polygons1

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo com 3 colunas
    cat = pd.Categorical(np.random.choice(range(1, 21), 1000, replace=True))
    cv = np.random.rand(1000)  # variável clássica
    data = pd.DataFrame({"category": cat, "cv1": cv, "cv2": np.random.rand(1000)})
    polygons = ptransform(data, 4)
    print(polygons)

    # Exemplo com 2 colunas
    data2 = pd.DataFrame({"category": cat, "cv": cv})
    polygons2 = ptransform(data2, 4)
    print(polygons2)
