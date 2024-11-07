from math import dist
import numpy as np
from pmean_id import pmean_id
from scipy.spatial.distance import euclidean

from psim import psim

# Função PLR
# Função PLR com verificação adicional do formato dos dados
def plr(formula, data, model=True, **kwargs):
    # Verifica se a fórmula é uma string válida
    if not isinstance(formula, str):
        raise ValueError("Insira uma fórmula válida como string!")
    
    # Divide a fórmula em variáveis dependentes e independentes
    formula_parts = formula.replace(' ', '').split('~')
    dependent_var = formula_parts[0]
    independent_vars = formula_parts[1].split('+')
    
    # Extrai as variáveis de resposta e preditoras
    response_variable = data[dependent_var]
    predictors = {var: data[var] for var in independent_vars}
    
   
    # Adicione verificação para o tipo de cada polígono em predictors
    for var in independent_vars:
        for i, poly in enumerate(predictors[var]):
            if not isinstance(poly, np.ndarray) or poly.ndim != 2:
                print(f"Erro: `predictors[{var}][{i}]` não é uma matriz 2D. Tipo: {type(poly)}, Shape: {getattr(poly, 'shape', None)}")
    
    # Calcula centros e raios para as variáveis preditoras e resposta
    x_centers = np.array([pmean_id(poly) for poly in predictors[independent_vars[0]]])
    for var in independent_vars[1:]:
        x_centers = np.column_stack((x_centers, [pmean_id(poly) for poly in predictors[var]]))
    
    y_centers = np.array([pmean_id(y) for y in response_variable])  # matriz (n_observations, 2)
    
    # Cálculo de raio para cada preditora
    x_radius = np.column_stack([[dist(pmean_id(poly), poly[0]) for poly in predictors[var]] for var in independent_vars])
    y_radius = np.array([dist(pmean_id(y), y[0]) for y in response_variable])  # vetor de raio

    # Expande `y_radius` para ter duas colunas, alinhando com `y_centers`
    y_radius_expanded = np.tile(y_radius, (2, 1)).T

    # Número de observações e variáveis
    n_observations = len(response_variable)
    n_variables = len(independent_vars) + 1  # resposta + variáveis preditoras

    # Montagem das matrizes
    intercept = True  # Considera intercepto
    xc = np.column_stack((np.ones((n_observations, 1)), x_centers)) if intercept else x_centers
    xr = np.column_stack((np.ones((n_observations, 1)), x_radius)) if intercept else x_radius

    # Expande `xc` e `xr` com zeros para igualar o número de colunas, se necessário
    max_columns = max(xc.shape[1], xr.shape[1])
    mat_zero_xc = np.zeros((n_observations, max_columns - xc.shape[1]))
    mat_zero_xr = np.zeros((n_observations, max_columns - xr.shape[1]))
    
    xc_zero = np.column_stack((xc, mat_zero_xc))
    xr_zero = np.column_stack((xr, mat_zero_xr))

    # Concatenação de centros e raios em uma única matriz X de 2*n_observations linhas
    X = np.vstack((xc_zero, xr_zero))
    
    # Concatena `y_centers` e `y_radius_expanded` para formar Y com 2*n_observations linhas
    Y = np.vstack((y_centers, y_radius_expanded))

    # Calcula os coeficientes do modelo
    coefficients = np.linalg.lstsq(X, Y, rcond=None)[0]

    # Separa os coeficientes para centro e raio
    beta_pol_center = coefficients[:n_variables]
    beta_pol_radius = coefficients[n_variables:]
    coefficients = np.concatenate((beta_pol_center, beta_pol_radius))

    # Predições
    Y_hat = X @ coefficients
    residuals = Y - Y_hat

    # Nomeando os coeficientes
    coefficient_names = ['(center-intercept)'] + [f'center-{var}' for var in independent_vars]
    if intercept:
        coefficient_names += ['(radius-intercept)'] + [f'radius-{var}' for var in independent_vars]
    else:
        coefficient_names += [f'radius-{var}' for var in independent_vars]
    
    # Resultados
    res = {
        "coefficients": dict(zip(coefficient_names, coefficients)),
        "residuals": residuals,
        "fitted.values": Y_hat,
        "rank": X.shape[1],
        "call": formula,
        "terms": formula_parts
    }
    
    # Matriz do modelo com centros e raios
    if model:
        center_radius_data = {
            'yc': y_centers,
            'yr': y_radius,
            'xc': x_centers,  # Adicionado
            'xr': x_radius,    # Adicionado
            **{f'xc_{i}': x_centers[:, i] for i in range(x_centers.shape[1])},
            **{f'xr_{i}': x_radius[:, i] for i in range(x_radius.shape[1])}
        }
        res["model"] = center_radius_data

    return res


# Exemplo de uso
#num_polygons = 5
#num_sides = 3

# Simula os polígonos
#yp = psim(num_polygons, num_sides)
#xp1 = psim(num_polygons, num_sides)
#xp2 = psim(num_polygons, num_sides)

# Cria um ambiente de dados
#data = pd.DataFrame({
#    'yp': yp,
#    'xp1': xp1,
#    'xp2': xp2
#})

#formula = 'yp ~ xp1 + xp2'

# Ajuste do modelo
#fit = plr(formula, data) 


    
#print("Coeficientes=")
#print(fit['coefficients'])
#print("Valores ajustados=")
#print(fit['fitted.values'])
#print("Resíduos=")
#print(fit['residuals'])

#import matplotlib.pyplot as plt
# Função para visualizar os polígonos
#def plot_polygons(polygons):
    #plt.figure(figsize=(8, 8))
    
    #for i, polygon in enumerate(polygons, start=1):
        # Desempacota as coordenadas x e y do polígono
        #x_coords, y_coords = zip(*polygon)
        
        # Fecha o polígono conectando o último ponto ao primeiro
        #x_coords += (x_coords[0],)
        #y_coords += (y_coords[0],)
        
        # Plotar o polígono
        #plt.plot(x_coords, y_coords, marker='o', label=f'Polígono {i}')
    
  # Configurações do gráfico
    #plt.title('Polígonos Gerados')
    #plt.xlabel('X')
    #plt.ylabel('Y')
    #plt.axhline(0, color='gray', linewidth=0.5)
    #plt.axvline(0, color='gray', linewidth=0.5)
    #plt.grid(True, linestyle='--', alpha=0.7)
    #plt.legend()
    #plt.axis('equal')  # Assegura que o aspecto seja quadrado
    #plt.show()

# Chame a função com a lista de polígonos gerados
#plot_polygons(polygons)