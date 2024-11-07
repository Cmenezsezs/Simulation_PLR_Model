# Criação de um DataFrame para o conjunto de dados longair
longair_data = {
    'city1': [],                       # Cidade de embarque
    'city2': [],                       # Cidade de desembarque
    'average_fare': [],                # Tarifa média
    'distance': [],                    # Distância entre as cidades
    'average_weekly_passengers': [],   # Passageiros semanais médios
    'market_leading_airline': [],      # Companhia aérea líder de mercado
    'market_share': [],                # Participação de mercado
    'average_return_fare': [],         # Tarifa média de ida e volta
    'low_price_airline': [],           # Companhia aérea de menor preço
    'market_share2': [],               # Segunda maior participação de mercado
    'price': []                        # Preço da viagem
}

longair = pd.DataFrame(longair_data)

# Exemplo de como carregar dados a partir de um arquivo CSV
# longair = pd.read_csv('longair.csv')

print(longair.head())
