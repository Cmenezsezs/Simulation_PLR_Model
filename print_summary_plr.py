
from plr_model import plr
from psim import psim

import numpy as np
import pandas as pd

from summary_plr import summary_plr

def print_summary_plr(x, digits=3, concise=False, **kwargs):
    """
    Print Summary Polygonal Linear Regression

    Args:
        x: an object of the class "summary.plr".
        digits: non-null value for digits specifies the minimum number of significant digits to be printed in values.
        concise: a boolean used to determine the type of digits.
        **kwargs: further arguments that special methods could require.
    
    """

    print("\nCall:\n", "\n".join(map(str, x['call'])), "\n")

    resid = x['residuals']

    coefs = pd.DataFrame(x['coefficients'])

    nam = ['Min', '1Q', 'Median', '3Q', 'Max']
    res = np.quantile(resid, [0, 0.25, 0.5, 0.75, 1])  # 0% (Min), 25%, 50% (Median), 75%, 100% (Max)
    res = np.round(res, digits)

    print('Residuals:')
    for name, value in zip(nam, res):
        print(f"{name}: {value:.{digits}f}")

    print()  # Just for formatting

    if len(coefs) > 0:
        print("Coefficients:")
        print(coefs.to_string(formatters={'float': lambda x: f"{x:.{digits}f}"}, index=False))
    else:
        print("No coefficients\n")

    return x  # Return x invisibly



# Exemplo - Simula 50 polígonos de 10 lados (exemplo fictício)
#num_polygons = 50 
#num_sides = 10

# Simula os polígonos
#yp = psim(num_polygons, num_sides)
#xp1 = psim(num_polygons, num_sides)
#xp2 = psim(num_polygons, num_sides)

# Criação de um ambiente similar ao e em R
#e = {
#    'yp': yp,
#    'xp1': xp1,
#    'xp2': xp2
#}

#fit = plr("yp ~ xp1 + xp2", data=e)
#s = summary_plr(fit)
#print_summary_plr(s)