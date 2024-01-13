from airflow.decorators import dag, task
from datetime import timedelta, datetime

default_agrs = {
    'owner': 'aida',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='dag_with_taskflow_api_v02',
     default_args=default_agrs,
     start_date=datetime(2021, 10, 26),
     schedule_interval='@daily')
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name':'Muhammad',
            'last_name':"Ibn'Abdallah"
        }

    @task
    def get_age():
        return 63
    
    @task
    def greet(fname,lname, age):
        print(f'My name is {fname} {lname} and my age is {age}')
    
    name_dict = get_name()
    age = get_age()
    greet(name_dict['first_name'],name_dict['last_name'], age)

greet_dag = hello_world_etl()
