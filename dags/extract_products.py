from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import json
import os
from datetime import datetime, timedelta

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# URL da API corrigida para comunicação dentro do Docker
API_BASE_URL = "http://host.docker.internal:8000"

# Diretório onde os arquivos serão salvos
RAW_STORAGE_PATH = "/opt/airflow/local_storage/raw/"

# Certifique-se de que o diretório existe
os.makedirs(RAW_STORAGE_PATH, exist_ok=True)

# Função para autenticação na API
def get_access_token():
    try:
        url = f"{API_BASE_URL}/token"
        data = {"username": "admin", "password": "admin"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        
        token = response.json()["access_token"]
        print(f"✅ Token de acesso obtido com sucesso.")
        return token
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter token: {e}")
        raise

# Função para extrair os produtos da API
def extract_products():
    try:
        token = get_access_token()
        url = f"{API_BASE_URL}/api/v1/products?limit=50&skip=0"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        products = response.json()

        # Criar nome do arquivo baseado na data e hora
        raw_file = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        raw_path = os.path.join(RAW_STORAGE_PATH, raw_file)

        # Salvar os dados na camada Raw
        with open(raw_path, "w") as f:
            json.dump(products, f)

        print(f"✅ Dados extraídos e salvos em: {raw_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao extrair produtos: {e}")
        raise

# Criar a DAG no Airflow
with DAG(
    'extract_products',
    default_args=default_args,
    description='Extrai os produtos da API e salva na camada Raw',
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_products',
        python_callable=extract_products,
    )

    extract_task

