from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.ssh_operator import SSHOperator

default_args = {
    'owner': 'price-insight',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG('listing_stats_batch', default_args=default_args, schedule_interval='@once')

data_fetch_task = SSHOperator(
    ssh_conn_id='data_fetch_conn',
    task_id='data_fetch',
    command='cd ~/PriceInsight/data_fetch; ./data_fetch.sh los-angeles',
    dag=dag)

config_generation_task = SSHOperator(
    ssh_conn_id='spark_master_conn',
    task_id='config_generation',
    command='cd ~/PriceInsight/price_stats_calculation; ./s3_urls_generation.sh los-angeles',
    dag=dag)

data_cleaning_task = SSHOperator(
    ssh_conn_id='spark_master_conn',
    task_id='data_cleaning',
    command='source ~/.profile; cd ~/PriceInsight/price_stats_calculation; ~/.local/bin/spark-submit all_write_columns_to_db.py los_angeles',
    dag=dag)

stats_aggregation_task = SSHOperator(
    ssh_conn_id='spark_master_conn',
    task_id='stats_aggregation',
    command='source ~/.profile; cd ~/PriceInsight/price_stats_calculation; ~/.local/bin/spark-submit zipcode_stats.py los_angeles',
    dag=dag)

config_generation_task.set_upstream(data_fetch_task)
data_cleaning_task.set_upstream(config_generation_task)
stats_aggregation_task.set_upstream(data_cleaning_task)
