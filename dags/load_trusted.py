from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def load_to_trusted():
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # Agregação dos dados para a camada Trusted
    cursor.execute("""
        INSERT INTO trusted.product_sales_daily (date, category, total_sales, avg_ticket, num_transactions)
        SELECT
            CURRENT_DATE AS date,
            category,
            SUM(price) AS total_sales,
            AVG(price) AS avg_ticket,
            COUNT(*) AS num_transactions
        FROM stage.products
        GROUP BY category;
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Dados agregados e carregados na camada Trusted!")

with DAG(
    'load_trusted',
    default_args=default_args,
    description='Transforma e carrega os dados na camada Trusted',
    schedule_interval='@daily',
    catchup=False
) as dag:

    load_task = PythonOperator(
        task_id='load_to_trusted',
        python_callable=load_to_trusted,
    )

    load_task

