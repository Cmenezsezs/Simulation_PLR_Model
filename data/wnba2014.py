import pandas as pd

# Criação de um DataFrame para WNBA 2014
wnba2014_data = {
    'player_id': [],      # ID do jogador
    'team_pts': [],       # Pontos do time
    'opp_pts': [],        # Pontos do oponente
    'minutes': [],        # Minutos jogados
    'fgatt': [],          # Tentativas de arremesso de quadra
    'efficiency': []      # Eficiência
}

wnba2014 = pd.DataFrame(wnba2014_data)

# Exemplo de como carregar dados a partir de um arquivo CSV
# wnba2014 = pd.read_csv('wnba2014.csv')

print(wnba2014.head())

