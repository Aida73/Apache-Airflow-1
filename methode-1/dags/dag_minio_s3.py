from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args={
    'owner': 'aida',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


with DAG(
    dag_id='dag_with_minio_aws_s3_v01',
    start_date=datetime(2022, 10, 3),
    default_args=default_args,
    schedule='@daily'
)as dag:
    task1 = S3KeySensor(
        task_id='task1',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn'
    )
    task1