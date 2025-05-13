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

EMAIL_DESTINATARIO = "lipelff20@gmail.com"
ASSUNTO = "Resumo de Citações Extraídas e Processadas"
CORPO_EMAIL = f"""
Olá, boa tarde!
Venho por meio deste enviar o projeto,desde já gostaria de agradecer pela oportunidade, como diz a série Suits "Não tenhos sonhos, tenho objetivo". Meu objetivo é está no mundo do desafio, que é claramente da programação.
Espero poder contribuir com meus esforços e conhecimentos que também quero adquiri para meu desenvolvimento e amadurecimento, daqui a 10 anos me vejo casado com um companheiro inabalevel, com Estela nos meus braços trabalhando em home ou hibrido dando todo o apoio para minha família,
ao mesmo tempo sendo uma grande inspiração como algumas mulheres são para mim. 

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
