from datetime import datetime, timedelta
import csv
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args={
    'owner': 'aida',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step1: query data from postgresql db and save into text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date <= %s",(ds_nodash,next_ds_nodash))
    with open(f"dags/get_orders_{ds_nodash}.txt","w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    cursor.close()
    conn.close()
    logging.info("Saved data into text file get_orders.txt")
    # step2: upload text file into S3 
    s3_hook = S3Hook(aws_conn_id="minio_conn")
    s3_hook.load_file(
        filename=f'get_orders_{ds_nodash}.txt',
        key=f"orders/{ds_nodash}.txt",
        bucket_name="airflow",
        replace=True
    )

with DAG(
    dag_id='dag_hook_v02',
    start_date=datetime(2022, 10, 3),
    default_args=default_args,
    schedule='@daily'
)as dag:
    task1 = PythonOperator(
        task_id="task1",
        python_callable=postgres_to_s3
    )
    task1