import traceback
import numpy as np
import pandas as pd
from scipy.stats import norm
from plr_model import plr
from rmsea import rmsea
from spolygon import spolygon
from fitted_plr import fitted_plr

# Função para gerar dados contínuos aleatórios para variáveis explicativas e termos de erro
def generate_data(m=100):
    beta_c = np.array([0, 2, -2, 5])
    beta_r = np.array([0, 1, 2, 3])
    g1_c = np.random.uniform(0, 10, m)
    g2_c = np.random.uniform(0, 10, m)
    g3_c = np.random.uniform(0, 10, m)
    g1_r = np.random.uniform(5, 10, m)
    g2_r = np.random.uniform(5, 10, m)
    g3_r = np.random.uniform(5, 10, m)
    eps_c = norm.rvs(0, 1, m)
    eps_r = norm.rvs(0, 1, m)
    
    return {
        'g1_c': g1_c, 'g2_c': g2_c, 'g3_c': g3_c,
        'g1_r': g1_r, 'g2_r': g2_r, 'g3_r': g3_r,
        'eps_c': eps_c, 'eps_r': eps_r,
        'beta_c': beta_c, 'beta_r': beta_r
    }

# Função para calcular variáveis de resposta
def compute_responses(data):
    w_c = data['beta_c'][0] + data['beta_c'][1] * data['g1_c'] + data['beta_c'][2] * data['g2_c'] + data['beta_c'][3] * data['g3_c'] + data['eps_c']
    w_r = data['beta_r'][0] + data['beta_r'][1] * data['g1_r'] + data['beta_r'][2] * data['g2_r'] + data['beta_r'][3] * data['g3_r'] + data['eps_r']
    return {'w_c': w_c, 'w_r': w_r}

# Função para validar e criar o polígono
def validate_polygon(center, radius, vertices):
    polygon = spolygon(center, radius, vertices)
    if polygon is None or not isinstance(polygon, np.ndarray) or polygon.ndim != 2 or polygon.shape[0] < 3:
        print("Polígono inválido detectado.")
        return None
    return polygon

# Função para calcular intervalo e ponto médio de um polígono, garantindo matriz 2D
def get_interval_and_midpoint(polygon):
    if polygon is None or not isinstance(polygon, np.ndarray) or polygon.shape[0] < 3:
        print("Polígono inválido encontrado")
        return {'midpoint': np.array([[np.nan]]), 'range': np.array([[np.nan]])}
    
    a_vals, b_vals = polygon[:, 0], polygon[:, 1]
    a_min, b_max = np.min(a_vals), np.max(b_vals)
    midpoint = (a_min + b_max) / 2
    range_val = (b_max - a_min) / 2
    return {'midpoint': np.array([[midpoint]]), 'range': np.array([[range_val]])}

# Função principal da simulação de Monte Carlo
def monte_carlo_simulation(config, n_rep=5, polygon_config=[3, 5, 6, 100]):
    rmsea_results = {config_name: {f"L={L}": [] for L in polygon_config} for config_name in config.keys()}

    for config_name, params in config.items():
        print(f"Iniciando simulação para configuração {config_name}")
        
        for L in polygon_config:
            print(f"Configurando polígono com L = {L}")
    
            for i in range(n_rep):
                print(f"Início da repetição {i + 1} para polígono com L = {L}")

                # Geração de dados e cálculo das respostas
                data = generate_data()
                responses = compute_responses(data)

                # Validação de polígonos
                polygon_g1 = [validate_polygon(data['g1_c'][j], data['g1_r'][j], L) for j in range(len(data['g1_c']))]
                polygon_g2 = [validate_polygon(data['g2_c'][j], data['g2_r'][j], L) for j in range(len(data['g2_c']))]
                polygon_g3 = [validate_polygon(data['g3_c'][j], data['g3_r'][j], L) for j in range(len(data['g3_c']))]
                polygon_w = [validate_polygon(responses['w_c'][j], responses['w_r'][j], L) for j in range(len(responses['w_c']))]

                if any(p is None for p in polygon_g1 + polygon_g2 + polygon_g3 + polygon_w):
                    print(f"Pulo iteração {i + 1}: polígono inválido com L = {L}")
                    continue

                # Calcular intervalos e pontos médios, garantindo matriz 2D
                midpoint_g1 = np.array([get_interval_and_midpoint(p)['midpoint'][0][0] for p in polygon_g1])
                range_g1 = np.array([get_interval_and_midpoint(p)['range'][0][0] for p in polygon_g1])
                midpoint_g2 = np.array([get_interval_and_midpoint(p)['midpoint'][0][0] for p in polygon_g2])
                range_g2 = np.array([get_interval_and_midpoint(p)['range'][0][0] for p in polygon_g2])
                midpoint_g3 = np.array([get_interval_and_midpoint(p)['midpoint'][0][0] for p in polygon_g3])
                range_g3 = np.array([get_interval_and_midpoint(p)['range'][0][0] for p in polygon_g3])
                midpoint_w = np.array([get_interval_and_midpoint(p)['midpoint'][0][0] for p in polygon_w])
                range_w = np.array([get_interval_and_midpoint(p)['range'][0][0] for p in polygon_w])

                # Certificar que todos os dados são matrizes 2D consistentes para o ajuste do modelo
                model_data = pd.DataFrame({
                    'midpoint_g1': midpoint_g1, 'range_g1': range_g1,
                    'midpoint_g2': midpoint_g2, 'range_g2': range_g2,
                    'midpoint_g3': midpoint_g3, 'range_g3': range_g3,
                    'midpoint_w': midpoint_w, 'range_w': range_w
                })

                if model_data.isna().any().any() or model_data.empty:
                    print("model_data contém valores nulos ou está vazio. Pulando iteração.")
                    continue
                
                # Ajuste do modelo PLR
                formula = "midpoint_w ~ midpoint_g1 + midpoint_g2 + midpoint_g3"
                try:
                    model = plr(formula, data=model_data)
                except Exception as e:
                    print(f"Erro ao ajustar modelo PLR: {e}")
                    traceback.print_exc()
                    continue

                # Calcular RMSEA
                fitted_values = fitted_plr(model, polygon=True, vertices=L)
                rmsea_value = rmsea(polygon_w, fitted_values)
                rmsea_results[config_name][f"L={L}"].append(rmsea_value)

    # Resultados formatados
    formatted_results = {}
    for config_name, results in rmsea_results.items():
        formatted_results[config_name] = {}
        for L, values in results.items():
            if values:
                mean_rmsea = np.mean(values)
                std_rmsea = np.std(values, ddof=1)
                formatted_results[config_name][L] = f"{mean_rmsea:.2f} ± {std_rmsea:.2f}"
            else:
                formatted_results[config_name][L] = "N/A"

    print("Simulação completa")
    print("Resultados RMSEA (média ± desvio padrão) para cada configuração e valor de L:")
    for config_name, results in formatted_results.items():
        print(f"Configuração {config_name}:")
        for L, result in results.items():
            print(f"  {L}: {result}")
    
    return formatted_results

# Definir configurações para simulações de Monte Carlo
config = {
    'C1': {'Gc': np.random.uniform(0, 10, 1000), 'Gr': np.random.uniform(5, 10, 1000), 'eps_c': np.random.uniform(-1, 1, 1000), 'eps_r': np.random.uniform(1, 5, 1000)},
    'C2': {'Gc': np.random.uniform(0, 10, 1000), 'Gr': np.random.uniform(5, 10, 1000), 'eps_c': np.random.uniform(-5, 5, 1000), 'eps_r': np.random.uniform(1, 10, 1000)},
    'C3': {'Gc': np.random.uniform(0, 10, 1000), 'Gr': np.random.uniform(5, 10, 1000), 'eps_c': np.random.uniform(-10, 10, 1000), 'eps_r': np.random.uniform(1, 20, 1000)},
    'C4': {'Gc': np.random.uniform(0, 10, 1000), 'Gr': np.random.uniform(5, 10, 1000), 'eps_c': np.random.uniform(-20, 20, 1000), 'eps_r': np.random.uniform(1, 30, 1000)}
}

# Executar a simulação com 100 repetições
formatted_results = monte_carlo_simulation(config, n_rep=5)
print(formatted_results)
