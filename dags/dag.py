from airflow import DAG
from airflow.operators.python import PythonOperator
from dag_functions.extract import extract_scorecard
from dag_functions.transform import transform_scorecard
from dotenv import load_dotenv
from datetime import datetime
import time
import boto3
import json
import os 

# top-level project directory
proj_dir = os.getcwd()

# specify data years to pull
years = ['2014']

# get current date + time in a string
timestamp = time.strftime("%Y%m%d-%H%M%S")

# specify file names for local files using the timestamp
raw_file_name = 'raw_scorecard_' + timestamp + '.JSONL'
clean_file_name = 'clean_scorecard_' + timestamp + '.csv'

# specify output paths with timestamp in filename
raw_output_path = proj_dir + '/data/raw/' + raw_file_name
clean_output_path = proj_dir + '/data/clean/' + clean_file_name

# wrapper to serialize extract_scorecard function output
def download_api():

    # run extraction function to pull data from API
    in_data_raw = extract_scorecard(years)

    # serialize JSONL file to raw data folder
    with open(raw_output_path, 'w') as f:
        for row in in_data_raw:
            f.write(json.dumps(row) + '\n')

# function for AWS S3 data upload
def upload_s3(file_name, bucket, object_name):

    # load AWS key
    load_dotenv()
    AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    s3.upload_file(file_name, bucket, object_name)

# wrapper to serialize transform_scorecard function output to csv
def write_clean_csv():

    # run transform function to pull data from API
    in_data_clean = transform_scorecard(file_path=raw_output_path)

    # convert df to csv
    in_data_clean.to_csv(clean_output_path, encoding='utf-8', index=False)

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
    'retries': 1
}

with DAG(
    'scorecard_dag',
    default_args=default_args,
    start_date=datetime(2022, 1, 1),
    schedule_interval="@once",
    catchup=True
) as dag:

    # task 1: pull data from College Scorecard API
    t1 = PythonOperator(
        task_id='t1_extract_api',
        python_callable=download_api
    )

    # task 2: upload JSONL to 'college-scorecard-raw' S3 bucket
    t2 = PythonOperator(
        task_id='t2_upload_raw_s3',
        python_callable=upload_s3,
        op_args='college-scorecard-raw'
    )

    # task 3: transform and export processed csv in '/data/clean/'
    t3 = PythonOperator(
        task_id="t3_transform_raw_to_clean",
        python_callable=write_clean_csv
    )

    # task 4: upload transformed .CSV to 'college-scorecard-clean' S3 Bucket
    t4 = PythonOperator(
        task_id="t4_upload_clean_s3",
        python_callable=upload_s3,
        op_args='college-scorecard-clean'
    )

    # task 5: load data to Redshift

    # dag flow
    t1 >> t2 >> t3 >> t4