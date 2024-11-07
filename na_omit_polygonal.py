# Lidar com valores ausentes em objetos poligonais
# 
# Descrição: A função omite polígonos ausentes.
# 
# Parâmetros:
# - object: objetos da classe "polygonal".
# - ...: outros argumentos que métodos especiais possam requerer.
# 
# Retorno:
# - polygons: um objeto da classe "polygonal" sem valores ausentes.

def na_omit(object, **kwargs):
    # Verifica se há valores ausentes nos polígonos
    missing_polygons = [poly is None for poly in object]
    
    if sum(missing_polygons) != 0:
        # Filtra os polígonos que não são ausentes
        polygons = [poly for poly, missing in zip(object, missing_polygons) if not missing]
    else:
        polygons = object
    
    # Define a classe do objeto como 'polygonal'
    polygons = {'class': 'polygonal', 'polygons': polygons}
    
    return polygons
