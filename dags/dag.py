from airflow import DAG
from airflow.operators.python import PythonOperator
from dag_functions.extract import extract_scorecard
from dag_functions.transform import transform_scorecard
from dotenv import load_dotenv
from datetime import datetime
import time
import glob
import boto3
import json
import os

# top-level project directory
proj_dir=os.getcwd()

# get current date + time in a string
timestamp = time.strftime("%Y%m%d-%H%M%S")

# specify file names for local files using the timestamp
raw_file_name = 'raw_scorecard_' + timestamp + '.JSONL'
clean_file_name = 'clean_scorecard_' + timestamp + '.csv'

# specify output paths with timestamp in filename
raw_output_path = proj_dir + '/data/raw/' + raw_file_name
clean_output_path = proj_dir + '/data/clean/' + clean_file_name

# wrapper to serialize extract_scorecard function output
def download_api(ti):

    # use XCOMS to pull return output from task 1
    in_data_raw = ti.xcom_pull(task_ids='t1_extract_api')

    # serialize JSONL file to raw data folder
    with open(raw_output_path, 'w') as f:
        for row in in_data_raw:
            f.write(json.dumps(row) + '\n')

    return(raw_output_path)

# function for AWS S3 raw data upload
def upload_raw_s3():

    # identify the latest raw file
    raw_files = glob.glob(proj_dir + '/data/raw/*') # * means all if need specific format then *csv.
    latest_raw = max(raw_files, key=os.path.getctime)

    # upload to s3
    s3_client = boto3.client('s3', aws_access_key_id = "", aws_secret_access_key = "")
    s3_client.upload_file(latest_raw, 'college-scorecard-raw', raw_file_name)

    return latest_raw

# wrapper to serialize transform_scorecard function output to csv
def write_clean_csv(ti):

    # use XCOMS to pull return output from task 1
    latest_raw = ti.xcom_pull(task_ids='t3_upload_raw_s3')

    # run transform function to pull data from API
    in_data_clean = transform_scorecard(file_path=latest_raw)

    # convert df to csv
    in_data_clean.to_csv(clean_output_path, encoding='utf-8', index=False)

# function for AWS S3 clean data upload
def upload_clean_s3():

    # identify the latest raw file
    clean_files = glob.glob(proj_dir + '/data/clean/*') # * means all if need specific format then *csv.
    latest_clean = max(clean_files, key=os.path.getctime)

    # upload to s3
    s3_client = boto3.client('s3', aws_access_key_id = "", aws_secret_access_key = "")
    s3_client.upload_file(latest_clean, 'college-scorecard-clean', clean_file_name)

# test call the functions
# download_api()

# upload_s3(
#     file_name=raw_output_path,
#     bucket='college-scorecard-raw',
#     object_name=raw_file_name)

# write_clean_csv()

# upload_s3(
#     file_name=clean_output_path,
#     bucket='college-scorecard-clean',
#     object_name=clean_file_name)

#### dag ----------------------------------------------------------------------

default_args = {
    'owner': 'airflow',
    'retries': 0
}

with DAG(
    'scorecard_dag_39',
    default_args=default_args,
    start_date=datetime(2022, 1, 1),
    schedule_interval="@once",
    catchup=False
) as dag:

    # task 1: pull data from College Scorecard API
    t1 = PythonOperator(
        task_id="t1_extract_api",
        python_callable=extract_scorecard,
        op_kwargs={'year': '2020', 'API_KEY': ''}
    )

    # task 2: persist output to disk
    t2 = PythonOperator(
        task_id='t2_serialize_output',
        python_callable=download_api
    )

    # task 3: upload JSONL to 'college-scorecard-raw' S3 bucket
    t3 = PythonOperator(
        task_id='t3_upload_raw_s3',
        python_callable=upload_raw_s3
    )

    # task 4: transform and export processed csv in '/data/clean/'
    t4 = PythonOperator(
        task_id="t4_transform_raw_to_clean",
        python_callable=write_clean_csv
    )

    # task 5: upload transformed .CSV to 'college-scorecard-clean' S3 Bucket
    t5 = PythonOperator(
        task_id="t5_upload_clean_s3",
        python_callable=upload_clean_s3
    )

    # task 6: load data to Redshift

    # dag flow
    t1 >> t2 >> t3 >> t4 >> t5