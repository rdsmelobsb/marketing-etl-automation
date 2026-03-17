# Pipeline de Dados: ETL Campanhas Google Sheets para BigQuery 🚀

Este repositório contém um script em Python (`etl_campanhas_bigquery.py`) responsável por automatizar a extração, transformação e carga (ETL) de dados de campanhas de marketing. O código lê informações do Google Sheets, limpa e consolida os dados, e os envia para o Google BigQuery. 

Além disso, o pipeline conta com um sistema de alertas por e-mail e integração com a IA do Google Gemini para enviar mensagens motivacionais diárias.

## 🛠️ Funcionalidades

* **Extração Automática:** Conecta-se à API do Google Sheets para ler uma planilha "mãe" com os links das campanhas e faz o download automático de todas as planilhas "filhas".
* **Transformação de Dados (Limpeza):** Padroniza os nomes das colunas, remove caracteres especiais de valores financeiros e ajusta formatos de data utilizando a biblioteca `pandas`.
* **Carga (Load):** Envia a tabela final consolidada (OBT - *One Big Table*) diretamente para um banco de dados no Google BigQuery.
* **Sistema de Alertas (E-mail):** Notifica a equipe de BI caso alguma planilha esteja vazia, ocorra algum erro no carregamento ou o processo seja concluído com sucesso.
* **Integração com IA:** Consome frases motivacionais (API Ninjas) e utiliza a API do Google Gemini para traduzi-las automaticamente para o português nos e-mails de sucesso.

## 💻 Tecnologias e Bibliotecas Utilizadas

* **Linguagem:** Python 3
* **Manipulação de Dados:** `pandas`
* **Requisições Web:** `requests`
* **Google Cloud & APIs:** `google-cloud-bigquery`, `google-auth`, `google-generativeai` (Gemini)
* **Segurança:** `python-dotenv`, `os` (para variáveis de ambiente)

## ⚙️ Como Configurar e Rodar o Projeto

Siga os passos abaixo para executar este código na sua máquina:

### 1. Clone o repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
```

### 2. Instale as dependências
Certifique-se de ter o Python instalado. É recomendado criar um ambiente virtual. Depois, instale as bibliotecas necessárias:
```bash
pip install pandas requests google-cloud-bigquery google-auth google-generativeai python-dotenv
```

### 3. Configure as Variáveis de Ambiente (.env)
Para manter suas credenciais seguras, **NUNCA** coloque suas senhas no código. 
Crie um arquivo chamado `.env` na raiz do projeto e preencha com os seus dados reais:

```text
# Configurações de E-mail
EMAIL_DISPARO=seu_email@empresa.com
EMAIL_SENHA=sua_senha_de_app_aqui

# Credenciais do Google Cloud (GCP)
GCP_PROJECT_ID=seu_project_id
GCP_PRIVATE_KEY_ID=seu_private_key_id
GCP_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_AQUI\n-----END PRIVATE KEY-----\n"
GCP_CLIENT_EMAIL=seu_client_email@...
GCP_CLIENT_ID=seu_client_id
GCP_CLIENT_CERT_URL=sua_url_de_certificado

# Configurações do BigQuery e Sheets
BQ_TABLE_ID=projeto.dataset.tabela
SHEETS_CAMPANHAS_ID=id_da_planilha_mae_aqui
GOOGLE_API_KEY=sua_api_key_do_google

# APIs Externas
GEMINI_API_KEY=sua_api_key_do_gemini
NINJAS_API_KEY=sua_api_key_do_api_ninjas
```

### 4. Execute o script
Com tudo configurado, basta rodar o comando:
```bash
python etl_campanhas_bigquery.py
