# Envio-de-e-mail
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def acessar_pagina(url):
    # Inicializa o driver do Chrome.
    print(f"Acessando a página: {url}")
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    return driver


def extrair_citacoes(driver):
    """
    Extrai as citações, autores e tags da página atual.
    """
    print("Iniciando a extração das citações...")
    citacoes = []
    try:
        elementos_citacao = driver.find_elements(By.CLASS_NAME, 'quote')
        for elemento in elementos_citacao:
            texto_citacao = elemento.find_element(By.CLASS_NAME, 'text').text.strip('“”')
            autor = elemento.find_element(By.CLASS_NAME, 'author').text
            tags = [tag.text for tag in elemento.find_elements(By.CLASS_NAME, 'tag')]
            citacoes.append({
                'Citação': texto_citacao,
                'Autor': autor,
                'Tags': ", ".join(tags)
            })
        print(f"{len(citacoes)} citações extraídas.")
    except Exception as e:
        print(f"Erro ao extrair citações: {e}")
        return []
    return citacoes


def salvar_csv(nome_arquivo, citacoes):
    """
    Salva as citações em um arquivo CSV, com aspas como delimitador e vírgula como separador.
    """
    if not citacoes:
        print("Não há citações para salvar no arquivo CSV.")
        return

    print(f"Salvando {len(citacoes)} citações no arquivo {nome_arquivo}...")
    try:
        with open(nome_arquivo, 'w', encoding='utf-8', newline='') as arquivo_csv:
            nome_campos = ['Citação', 'Autor', 'Tags']
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=nome_campos, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            escritor_csv.writeheader()
            escritor_csv.writerows(citacoes)
        print(f"Dados salvos com sucesso no arquivo '{nome_arquivo}'")
    except Exception as e:
        print(f"Erro ao salvar arquivo CSV: {e}")


def obter_proxima_pagina(driver):
    """
    Verifica se há uma próxima página e retorna a URL dela.
    """
    try:
        # Espera até que o botão "next" esteja presente e visível
        proxima_pagina = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'next'))
        )
        if proxima_pagina:
            # Extrai o link para a próxima página
            link_proxima_pagina = proxima_pagina.find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(f"Próxima página encontrada: {link_proxima_pagina}")
            return link_proxima_pagina
    except Exception as e:
        print(f"Erro ao verificar a próxima página: {e}")
    print("Não há próxima página.")
    return None  # Retorna se não houver próxima página


def main():
    url_inicial = 'https://quotes.toscrape.com/js-delayed/page/1/'
    nome_arquivo_csv = 'quotes.csv'

    # Acessa a primeira página.
    print("Iniciando o processo de scraping...")
    driver = acessar_pagina(url_inicial)
    citacoes_totais = []

    while driver:
        # Extrai as citações da página atual.
        citacoes = extrair_citacoes(driver)
        citacoes_totais.extend(citacoes)  # Adiciona as citações extraídas à lista total

        # Verifica se existe uma próxima página e, se sim, acessa ela.
        proxima_pagina_url = obter_proxima_pagina(driver)
        if proxima_pagina_url:
            print("Carregando a próxima página...")
            driver.get(proxima_pagina_url)
            time.sleep(15)  # Aguarda um pouco antes de continuar
        else:
            print("Processo concluído: não há mais páginas para carregar.")
            break  # Se não houver próxima página, sai do loop

    # Salva as citações em um arquivo CSV.
    salvar_csv(nome_arquivo_csv, citacoes_totais)

    # Fecha o navegador.
    print("Fechando o navegador...")
    driver.quit()

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
if __name__ == "__main__":
    main()
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Caminho do arquivo .env dentro da pasta Downloads
caminho_env = os.path.join(os.path.expanduser("~"), "Downloads", "acesso_email.env")
load_dotenv(caminho_env)  # Carrega as variáveis do .env

# Configurações do e-mail
EMAIL_REMETENTE = os.getenv('EMAIL_ADDRESS')
SENHA = os.getenv('EMAIL_PASSWORD')  # Use senha de app para Gmail

# É necessário criar um arquivo pelo qual criei o env, com o login do e-mail e o código da senha do e-mail, cria uma pasta e acrescentar no arquivo.

EMAIL_DESTINATARIO = "paulo.andre@parvi.com.br","thiago.jose@parvi.com.br"
ASSUNTO = "Resumo de Citações Extraídas e Processadas"
CORPO_EMAIL = f"""
Olá, bom dia!
Venho por meio deste enviar o projeto,desde já gostaria de agradecer pela oportunidade, como diz a série Suits "Não tenhos sonhos, tenho objetivo". Meu objetivo é está no mundo do desafio, que é claramente da programação.
Espero poder contribuir com meus esforços e conhecimentos que também quero adquiri para meu desenvolvimento e amadurecimento.

Segue em anexo o arquivo 'quotes.csv' contendo os dados de citações extraídos.

Abaixo, um breve resumo dos dados processados:

Atenciosamente,
Fernanda Ferreira
"""

# Caminho do arquivo CSV
caminho_arquivo = os.path.join(os.path.expanduser("~"), "Downloads", "quotes.csv")

# Criação da mensagem
msg = EmailMessage()
msg['Subject'] = ASSUNTO
msg['From'] = EMAIL_REMETENTE
msg['To'] = EMAIL_DESTINATARIO
msg.set_content(CORPO_EMAIL)

# Adiciona o CSV como anexo
with open(caminho_arquivo, 'rb') as f:
    conteudo = f.read()
    msg.add_attachment(conteudo, maintype='text', subtype='csv', filename='quotes.csv')

# Envia o e-mail via servidor SMTP (exemplo com Gmail)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_REMETENTE, SENHA)
    smtp.send_message(msg)

print("E-mail enviado com sucesso!")

