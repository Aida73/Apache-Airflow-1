from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args={
    'owner': 'aida',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_postgres_operator_v04',
    start_date=datetime(2022, 10, 3),
    default_args=default_args,
    schedule_interval='0 0 * * *'
)as dage:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql='''
            create table if not exists dag_runs(
            dt date,
            dag_id character varying,
            primary key (dt, dag_id)
            )
        '''
    )
    task2 = PostgresOperator(
        task_id='insert_into_table',
        postgres_conn_id='postgres_localhost',
        sql='''
            insert into dag_runs(dt, dag_id) values('{{ ds }}','{{ dag.dag_id }}')
        '''
    )
    task3 = PostgresOperator(
        task_id='delete_into_table',
        postgres_conn_id='postgres_localhost',
        sql='''
            delete from dag_runs where dt='{{ ds }}' and dag_id='{{ dag.dag_id }}'
        '''
    )
    task1 >> task3 >> task2