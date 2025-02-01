from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
import os
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

RAW_STORAGE_PATH = "/opt/airflow/local_storage/raw/"

def load_to_stage():
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # Listar arquivos JSON na pasta Raw
    files = [f for f in os.listdir(RAW_STORAGE_PATH) if f.endswith(".json")]
    
    for file in files:
        file_path = os.path.join(RAW_STORAGE_PATH, file)

        with open(file_path, "r") as f:
            products = json.load(f)

        for product in products:
            cursor.execute("""
                INSERT INTO stage.products (name, category, price, created_at)
                VALUES (%s, %s, %s, %s);
            """, (product["name"], product["category"], product["price"], datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Dados carregados na camada Stage!")

with DAG(
    'load_stage',
    default_args=default_args,
    description='Carrega os produtos para a camada Stage',
    schedule_interval='@daily',
    catchup=False
) as dag:

    load_task = PythonOperator(
        task_id='load_to_stage',
        python_callable=load_to_stage,
    )

    load_task

