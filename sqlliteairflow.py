# Import necessary libraries
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sqlite3
import os

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(days=1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define a function to perform full data pull
def full_pull(**kwargs):
    # Connect to the source database
    source_conn = sqlite3.connect(kwargs['source_db'])
    source_cursor = source_conn.cursor()

    # Fetch data from the source
    source_cursor.execute("SELECT * FROM source_table")
    data = source_cursor.fetchall()
    source_conn.close()

    # Connect to the target database and remove existing data
    destination_conn = sqlite3.connect(kwargs['destination_db'])
    destination_cursor = destination_conn.cursor()
    
    # (Optional) Remove existing data if you want to perform a full refresh
    destination_cursor.execute("DELETE FROM destination_table")

    # Insert data into the destination database
    destination_cursor.executemany("INSERT INTO destination_table (id, data) VALUES (?, ?)", data)
    destination_conn.commit()
    destination_conn.close()

# Define the DAG
dag = DAG(
    'data_transfer_dag',
    default_args=default_args,
    description='DAG for transferring data from source to destination',
    schedule_interval=timedelta(days=1),
)

# Define the PythonOperator task
transfer_data_task = PythonOperator(
    task_id='transfer_data',
    python_callable=full_pull,
    op_kwargs={
        'source_db': '/path/to/source.db',
        'destination_db': '/path/to/destination.db',
    },
    dag=dag,
)

# Specify the order of task execution (in this case, just one task)
transfer_data_task
