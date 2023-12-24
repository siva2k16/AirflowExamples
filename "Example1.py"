from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# These args will get passed on to the Python operator
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define a basic function to use as a Python task
def my_first_function(**kwargs):
    print("Hello from my first function!")

def my_second_function(**kwargs):
    print("Hello from my second function!")

# Define the DAG (workflow)
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(0),
    tags=['example'],
)

# Define tasks
task1 = PythonOperator(
    task_id='my_first_task',
    python_callable=my_first_function,
    dag=dag,
)

task2 = PythonOperator(
    task_id='my_second_task',
    python_callable=my_second_function,
    dag=dag,
)

# Set task order
task1 >> task2
