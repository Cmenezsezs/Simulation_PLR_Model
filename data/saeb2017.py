# Criação de um DataFrame para o conjunto de dados SAEB 2017
saeb2017_data = {
    'county': [],                      # Identificação do condado
    'proficiency_lp_center': [],       # Centro da proficiência em Português
    'proficiency_mt_center': [],       # Centro da proficiência em Matemática
    'classroom_center': [],            # Centro do número de salas de aula
    'classroom_used_center': [],       # Centro do número de salas de aula usadas
    'employees_center': [],            # Centro do número de funcionários
    'proficiency_lp_radius': [],       # Raio da proficiência em Português
    'proficiency_mt_radius': [],       # Raio da proficiência em Matemática
    'classroom_radius': [],            # Raio do número de salas de aula
    'classroom_used_radius': [],       # Raio do número de salas de aula usadas
    'computers_radius': [],            # Raio do número de computadores
    'employees_radius': []             # Raio do número de funcionários
}

saeb2017 = pd.DataFrame(saeb2017_data)

# Exemplo de como carregar dados a partir de um arquivo CSV
# saeb2017 = pd.read_csv('saeb2017.csv')

print(saeb2017.head())
