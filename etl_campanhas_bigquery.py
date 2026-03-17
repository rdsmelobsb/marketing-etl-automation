import pandas
import requests
from datetime import datetime, timedelta
from google.oauth2 import service_account
import math
import smtplib
from email.message import EmailMessage
import random
from google.cloud import bigquery
import google.generativeai as genai
import os 

class MandaEmail:
    def __init__(self, email_disparo, senha, host="smtp.gmail.com", porta=587):
        self.email_disparo = email_disparo
        self.senha = senha
        self.host = host
        self.porta = porta
        self.assinatura_html = """
<br><br>
<div style="border-top: 1px solid #ddd; padding-top: 20px;">
  <img src="https://ci3.googleusercontent.com/meips/ADKq_NZdcHdNy_Hp_y-J5kCshOEzDyqR3_178N-hwJhwoFNL2TWFLG1xZsRvI4w6cRuDFJUAG9vB_LOu5WIeCKFpGW-8kov3dOdJCavhSBpIJWP4=s0-d-e1-ft#https://novasb.com.br/wp-content/uploads/assinatura/bi.png" alt="Logo da Empresa" style="width: 420px; height: 100px">
</div>
"""

    def enviar_email_alerta(self, campanha, planilha):
        ASSUNTO = f'ALERTA ALERTA ALERTA! A campanha {campanha} está com a base vazia.'
        msg = EmailMessage()
        msg['Subject'] = f"{ASSUNTO}"
        msg['From'] = 'bi@novagencia.com'
        msg['To'] = 'rafael.melo@novagencia.com'

        mensagem = f'Olá, <a href="mailto:{msg["To"]}" rel="noopener noreferrer" target="_blank">@{"EQUIPE_BI"}</a> <br><br>A campanha {campanha} está com a base de dados quebrada.<br>Verifique na planilha: {planilha}<br><br>Abs,'

        msg.set_content(mensagem + self.assinatura_html, subtype='html')

        with smtplib.SMTP(self.host, self.porta) as server:
            server.starttls()
            server.login(self.email_disparo, self.senha)
            server.send_message(msg)

        print(f"Email enviado com sucesso para {msg['To']}!")

    def enviar_email_erro_carregar_dados_bq(self, campanha, erro):
        ASSUNTO = f'ALERTA ALERTA ALERTA! o banco {campanha} não foi atualizado.'
        msg = EmailMessage()
        msg['Subject'] = f"{ASSUNTO}"
        msg['From'] = 'bi@novagencia.com'
        msg['To'] = 'rafael.melo@novagencia.com'

        mensagem = f'Olá, <a href="mailto:{msg["To"]}" rel="noopener noreferrer" target="_blank">@{"EQUIPE_BI"}</a> <br><br>O banco de dados {campanha} não foi carregado no dia {datetime.today().date().strftime("%d/%m/%Y")}.<br>O erro é {erro}.<br><br>Abs,'

        msg.set_content(mensagem + self.assinatura_html, subtype='html')

        with smtplib.SMTP(self.host, self.porta) as server:
            server.starttls()
            server.login(self.email_disparo, self.senha)
            server.send_message(msg)

        print(f"Email enviado com sucesso para {msg['To']}!")

    def enviar_sucesso(self, campanha, data_limite):
        ASSUNTO = f'Os últimos 30 dias do banco de dados {campanha} foram ATUALIZADOS com sucesso no dia {(datetime.today().date()).strftime("%d/%m/%Y")}.'
        msg = EmailMessage()
        msg['Subject'] = f"{ASSUNTO}"
        msg['From'] = 'bi@novagencia.com'
        msg['To'] = 'rafael.melo@novagencia.com'

        mensagem = f'Olá, <a href="mailto:{msg["To"]}" rel="noopener noreferrer" target="_blank">@{"EQUIPE_BI"}</a> <br><br>O banco de dados {campanha}, foi montado com sucesso.<br>Foram atualizados no banco todos os registros a partir de {(datetime.today().date() - timedelta(30)).strftime("%d/%m/%Y")}.<br><br>CITAÇÃO DO DIA (pílulas de descompressão ou stress..)<br>"{data_limite[0]}"<br>{data_limite[-1]}<br><br>Abs,'

        msg.set_content(mensagem + self.assinatura_html, subtype='html')

        with smtplib.SMTP(self.host, self.porta) as server:
            server.starttls()
            server.login(self.email_disparo, self.senha)
            server.send_message(msg)

        print(f"Email enviado com sucesso para {msg['To']}!")

email_disparo = os.environ.get("EMAIL_DISPARO")
senha = os.environ.get("EMAIL_SENHA")

enviarEmail = MandaEmail(email_disparo=email_disparo, senha=senha)

# Tratamento especial para a chave privada do GCP (para lidar com quebras de linha)
private_key_raw = os.environ.get("GCP_PRIVATE_KEY", "")
private_key_formatada = private_key_raw.replace('\\n', '\n')

file = {
  "type": "service_account",
  "project_id": os.environ.get("GCP_PROJECT_ID"),
  "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
  "private_key": private_key_formatada,
  "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
  "client_id": os.environ.get("GCP_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get("GCP_CLIENT_CERT_URL"),
  "universe_domain": "googleapis.com"
}

table_id = os.environ.get("BQ_TABLE_ID")
google_credentials = (file)
credentials = service_account.Credentials.from_service_account_info(google_credentials, scopes=["https://www.googleapis.com/auth/bigquery"])

# IDs e Keys do Google Sheets
sheets_campanha_id = os.environ.get("SHEETS_CAMPANHAS_ID")
api_jey = os.environ.get("GOOGLE_API_KEY")
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheets_campanha_id}/values/CAMPANHAS!A1%3AC?key='

# Chaves de APIs externas
API_KEY_GEMINI = os.environ.get("GEMINI_API_KEY")
API_KEY_NINJAS = os.environ.get("NINJAS_API_KEY")

genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel('gemini-1.0-pro')

def clean_column_name(column_name):
  cleaned = column_name.strip().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_").replace(".", "").replace("%","").replace('í','i').replace('Ú','U').replace("_actions","").replace("+","").replace("CTA clicks","CTA_clicks").replace(":","_").replace(",","_").replace("（Act）","_act_").replace("/","_").replace('ú','u').replace('ã','a').replace('õ','o').replace('ç','c').replace("ê","e")
  return cleaned

def clean_values(icon):
  value = str(icon).replace('R$','').replace('%','').replace('.','').replace(',','.')
  value = pandas.to_numeric(value, errors='coerce')
  if math.isnan(float(value)):
    value = 0
    return value
  return value

def create_final_seed_column(df):
    filtered_df = df[['SEED', 'ID_SEED', 'Seed']]
    filtered_df['final_seed'] = filtered_df.apply(lambda row: row['SEED'] if pandas.notna(row['SEED'])
                                                  else (row['ID_SEED'] if pandas.notna(row['ID_SEED'])
                                                  else row['Seed']), axis=1)
    df['final_seed'] = filtered_df['final_seed']

    df = df[['Plataforma', 'Placement', 'Date', 'Account', 'Campaign_name',
       'Campaign_start_date', 'Campaign_end_date', 'Ad_set_name',
       'Promoted_post_name', 'Campaign_objective', 'Promoted_post_image_URL',
       'Url_Destino', 'Cost', 'Impressions', 'Link_clicks', 'Post_reactions',
       'Post_comments', 'Post_shares', 'Video_play', 'Video_watches_at_25',
       'Video_watches_at_50', 'Video_watches_at_75', 'Video_watches_at_100',
       'Alcance', 'campanha', 'Reach', 'Veiculo',
       'Ad_group_name', 'Ad_type', 'Clicks', 'CTR', 'Destination_URL', 'Conta',
       'ID', 'final_seed']]
    return df

def limpa_data(i):
  if '/' in i.strip():
    i = (datetime.strptime(i.strip(), "%d/%m/%Y").date())
  else:
    i = (datetime.strptime(i.strip(), "%Y-%m-%d").date())
  return i

def gemini_fx(prompt):
  result = model.generate_content(prompt, safety_settings={'HARASSMENT':'block_none','HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none'})
  try:
    return result.text
  except:
    return result.prompt_feedback

def quotes():
  list_category =  ["age", "alone", "amazing", "anger", "architecture", "art", "attitude", "beauty", "best", "birthday", "business", "car", "change", "communication", "computers", "cool", "courage", "dad", "dating", "death", "design", "dreams", "education", "environmental", "equality", "experience", "failure", "faith", "family", "famous", "fear", "fitness", "food", "forgiveness", "freedom", "friendship", "funny", "future", "god", "good", "government", "graduation", "great", "happiness", "health", "history", "home", "hope", "humor", "imagination", "inspirational", "intelligence", "jealousy", "knowledge", "leadership", "learning", "legal", "life", "love", "marriage", "medical", "men", "mom", "money", "morning", "movies", "success"]
  category = random.choice(list_category)
  api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
  
  # Usando a variável de ambiente para a API Key do Ninjas
  response = requests.get(api_url, headers={'X-Api-Key': API_KEY_NINJAS})
  
  if response.status_code == requests.codes.ok:
      response = response.json()
      citacao = response[0]["quote"]
      categoria = response[0]["category"]
      autor = response[0]["author"]
      return [citacao, categoria, autor]
  else:
      print("Error:", response.status_code, response.text)
      pass

URL = f'{url}{api_jey}'
response = requests.get(URL).json()

table = pandas.DataFrame(response['values'])
table.columns = table.iloc[0]
table.columns = [clean_column_name(col_name) for col_name in table.columns]
table = table.drop(index=0)

filtered_data = table
lista_df = []

for index, row in filtered_data.iterrows():
  i = row['CHAVE_PLANILHA']
  campanha = row['CAMPANHA']
  link = f'https://sheets.googleapis.com/v4/spreadsheets/{i}/values/CONSOLIDADO!A1%3AY?key={api_jey}'
  response = requests.get(link).json()
  table = pandas.DataFrame(response['values'])
  table.columns = table.iloc[0]
  table.columns = [clean_column_name(col_name) for col_name in table.columns]
  table = table.drop(index=0)
  table = table.dropna()
  table['campanha'] = campanha

  if len(table) > 0:
    lista_df.append(table)

  if len(table) <= 0:
    enviarEmail.enviar_email_alerta(campanha=campanha, planilha=f'https://docs.google.com/spreadsheets/d/{i}')

  print(f'{campanha} processada!\n')

try:
  obt = pandas.concat(lista_df)
  obt = create_final_seed_column(obt)
  print(f'A obt foi MONTADA com sucesso!')
except:
  print(f'ALERTA ALERTA ALERTA!!\nA obt não foi MONTADA!')
  enviarEmail.enviar_email_alerta(campanha="OBT", planilha='A obt não foi MONTADA')

obt['Date'] = [limpa_data(i) for i in obt['Date']]

data_limite = datetime.today().date() - timedelta(days=30)
obt['Date'] = pandas.to_datetime(obt['Date']).dt.date

for key in obt.columns[12:24]:
    obt[key] = [clean_values(row) for row in obt[key]]
for key in obt.columns[0:12]:
    obt[key] = [str(row) for row in obt[key]]

new_table_id = f"{table_id}"
client = bigquery.Client(credentials=credentials, project=os.environ.get("GCP_PROJECT_ID"))

try:
  citacoes = quotes()
  traducao = gemini_fx(prompt=f'traduza para o pt-br sem alterar o sentido original a citação: {citacoes[0]}')
  citacoes[0] = traducao
  obt.to_gbq(new_table_id, credentials=credentials, if_exists='replace')
  enviarEmail.enviar_sucesso(campanha="OBT", data_limite=citacoes)
  print(f'Os últimos 30 dias da obt foram ARMAZENADOS com sucesso!')
except Exception as err:
  enviarEmail.enviar_email_erro_carregar_dados_bq(campanha="OBT", erro=err)
  print(f'ALERTA ALERTA ALERTA!!\nA obt não foi concatenada!')
