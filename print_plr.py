import numpy as np

from plr_model import plr


def print_plr(fit, digits=4):
    # Exibir a chamada (formula) usada no ajuste do modelo
    print("\nCall:\n", fit.get('call'), "\n")

    # Exibir os coeficientes formatados
    if 'coefficients' in fit and len(fit['coefficients']) > 0:
        print("Coefficients:")
        formatted_coeffs = [f"{coeff:.{digits}g}" for coeff in fit['coefficients']]
        print("  ".join(formatted_coeffs))
    else:
        print("No coefficients")
    
    # Exibir outros detalhes do modelo, se presentes
    if 'model' in fit:
        print("\nModel details:")
        print("yc:", fit['model']['yc'])
        print("yr:", fit['model']['yr'])
        print("mat_xc:", fit['model']['mat_xc'])
        print("x_radius:", fit['model']['x_radius'])
    
    print("\n")

# Exemplo de uso da função print_plr com o modelo ajustado
data = {
    'yp': np.random.rand(10, 10),
    'xp1': np.random.rand(10, 10),
    'xp2': np.random.rand(10, 10)
}
formula = 'yp ~ xp1 + xp2'

fit = plr(formula, data)
print_plr(fit)
