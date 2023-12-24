import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def full_pull():
    # Code to perform a full pull of data:
    # - Establish a connection to source database
    # - Fetch data from source
    # - Establish a connection to target database
    # - Delete existing data in target (optional, based on requirements)
    # - Insert retrieved data into target
    pass

dag = DAG(
    'full_pull_dag',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1),
    schedule_interval="@daily"  # Or another timedelta or cron expression
)

full_pull_task = PythonOperator(
    task_id='full_pull',
    python_callable=full_pull,
    dag=dag,
)
