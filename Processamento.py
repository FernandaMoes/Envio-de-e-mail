import pandas as pd
from collections import Counter
import os

diretorio= os.path.join(os.path.expanduser("~"), "Downloads")
arquivo = diretorio+"/quotes.csv"

# Ler o arquivo 'quotes.csv'
try:
    df = pd.read_csv(arquivo)
except FileNotFoundError:
    print("Erro: O arquivo 'quotes.csv' não foi encontrado. Certificar de executar a Parte 1 primeiro.")
    exit()

# Identificar e exiba a quantidade de citações
num_citacoes = len(df)
print(f"Número total de citações no arquivo: {num_citacoes}\n")

# Identifica e exiba o autor mais recorrente
autor_mais_recorrente = df['Autor'].mode()[0]
print(f"O autor mais recorrente é: {autor_mais_recorrente}\n")


# Identifique e exibir as tag mais utilizada
# As tags estão em uma única coluna separadas por vírgula.
# Dividindo as tags e contar a frequência de cada uma.
todas_as_tags = []

for tags_str in df['Tags']:
    if type(tags_str) == str:
        tags = tags_str.split(', ')
        todas_as_tags.extend(tags)

tag_counts = Counter(todas_as_tags)
tag_mais_utilizada = tag_counts.most_common(1)[0][0]
print(f"A tag mais utilizada é: {tag_mais_utilizada}")