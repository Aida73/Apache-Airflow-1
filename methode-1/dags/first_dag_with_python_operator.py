from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'aidasow',
    'etries': 5,
    'retry_delay': timedelta(minutes=5)
}


def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'My name is {first_name} {last_name} and my age is {age}')

def get_name(ti):
    ti.xcom_push(key='first_name', value='Muhammad'),
    ti.xcom_push(key='last_name', value="Ibn'Abdalah")

def get_age(ti):
    ti.xcom_push(key='age', value=63)

with DAG(
    dag_id='first_dag_with_python_operator_v06',
    description='Our first dag with python operator',
    default_args=default_args,
    start_date=datetime(2021,7,29,2),
    schedule_interval='@daily'

)as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
        #op_kwargs={'age':24}
    )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )
    [task3, task2 ]>> task1