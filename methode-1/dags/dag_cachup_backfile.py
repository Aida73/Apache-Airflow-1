from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args={
    'owner': 'aida',
    'reties': 5,
    'retry_delay': timedelta(minutes=3)
}

with DAG(
    dag_id='dag_with_catchup_backfile_v01',
    start_date=datetime(2021, 12, 8),
    schedule_interval='@daily',
    catchup=True

)as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo this is a simple bash command'
    )
    task1