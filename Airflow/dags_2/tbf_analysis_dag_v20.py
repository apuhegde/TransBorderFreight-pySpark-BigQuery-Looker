import importlib
import os
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
    ClusterGenerator)
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
construct_download_URL = importlib.import_module("01_Construct_URL", package=None)

#Get the environment variables
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
REGION = os.environ.get("GCP_REGION")
#REGION = "global"
#ZONE = os.environ.get("GCP_ZONE")
ZONE = os.environ.get("GCP_REGION")+"-b"
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_TABLE = os.environ.get("BQ_TABLE")
BQ_OUTPUT = f'{BQ_DATASET}.{BQ_TABLE}'
METADATA_FILE = os.environ.get("METADATA_FILE")

#set other GCP variables
TEMP_GCS_BUCKET = f'{BUCKET}-temp'
CLUSTER_NAME = f'{PROJECT_ID}-dataproc'
GCS_SERVICE_ACCOUNT = os.environ.get("GCS_SERVICE_ACCOUNT")
GCS_CREDENTIALS_JSON = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

#set pyspark job variables
PYSPARK_URI_LOC1 = f'gs://{BUCKET}/code/02a_transform_consolidate.py'
PYSPARK_URI_LOC2 = f'gs://{BUCKET}/code/02b_transform_joinwithmetadata.py'
JARS_URI_LOC = 'gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar'

#set download raw files task variables
URL_PREFIX = os.environ.get("RAW_DATA_URL")
START_YEAR = int(os.environ.get("DOWNLOAD_YEAR_START"))
END_YEAR = int(os.environ.get("DOWNLOAD_YEAR_END"))
years = range(START_YEAR,END_YEAR, 1)
months = range(1, 13)
#extract_script_loc = os.environ.get("DAGS_LOCATION")+"/01_ExtractData_LoadToGCS.sh"
extract_script_loc = os.environ.get("DAGS_LOCATION")+"/dags/01_ExtractData_LoadToGCS.sh"
GCS_TRANSFER_SCRIPT = os.environ.get("GCS_TRANSFER_SCRIPT")

#Define default args for dag
default_args = {
    "owner": "airflow",
    "start_date": days_ago(0),
    "depends_on_past": False,
    "retries": 1,
}

'''
#Set Dataproc cluster configuration
CLUSTER_CONFIG = ClusterGenerator(
    project_id=PROJECT_ID,
    zone=ZONE,
    master_machine_type="e2-standard-4",
    worker_machine_type="e2-standard-4",
    num_workers=2,
    worker_disk_size=50,
    master_disk_size=50,
    storage_bucket=TEMP_GCS_BUCKET,
).make()

#Define cluster config:
CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "e2-standard-4",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 30},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "e2-standard-4",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 30},
    },
    "software_config": {
        "image_version": "2.1.21-ubuntu20",
        "override_properties": {
        "dataproc:dataproc.allow.zero.workers": "true",
        "dataproc:dataproc.conscrypt.provider.enable": "false"
      }
    }
}
'''


#Define pyspark jobs
PYSPARK_JOB1 = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
        "main_python_file_uri": PYSPARK_URI_LOC1, 
        "jar_file_uris": [JARS_URI_LOC],
        "args": [
            f"--gcs_input_path=gs://{BUCKET}/raw/csv",
            f"--gcs_output_path=gs://{BUCKET}/raw"
            ]
    }
}

PYSPARK_JOB2 = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
        "main_python_file_uri": PYSPARK_URI_LOC2, 
        "jar_file_uris": [JARS_URI_LOC],
        "args": [
            f"--gcs_input_path=gs://{BUCKET}/raw/cleanedup_pq",
            f"--bq_output={BQ_OUTPUT}", 
            f"--metadata_file={METADATA_FILE}", 
            f"--temp_gcs_bucket={TEMP_GCS_BUCKET}"
            ]
    }
}


#Airflow DAG
with DAG(dag_id="tbf_analysis_dag_v20", 
    schedule_interval="@once", 
    default_args=default_args, 
    tags=['tbf-analysis'], 
    catchup=False
) as dag:
    
    #0a. Authenticate gcloud service account
    authenticate_service_acct_task = BashOperator(
                task_id=f"authenticate_service_acct_task",
                bash_command=f"echo starting_gcloud_auth; gcloud auth activate-service-account {GCS_SERVICE_ACCOUNT} --key-file {GCS_CREDENTIALS_JSON}; echo ending_gcloud_auth"
            )
    
    # #0b. Transfer code to GCS bucket
    # transfer_to_GCS_task = BashOperator(
    #             task_id="transfer_to_GCS_task",
    #             bash_command=f"bash {GCS_TRANSFER_SCRIPT} gs://{BUCKET}"
    #         )
    
    #0c. Install pip package
    install_pip_package_task = BashOperator(
        task_id="install_pip_package_task",
        bash_command=f"gcloud compute ssh {PROJECT_ID}-dataproc-m --zone={REGION}-b --project={PROJECT_ID} --command='pip install xlrd'"
    )

    # #1. Download RAW data files from data.gov
    # download_raw_data_task = PythonOperator(
    #             task_id=f"download_raw_data_task",
    #             python_callable=construct_download_URL.construct_download_URL,
    #             op_kwargs={
    #                 "URL_PREFIX": URL_PREFIX,
    #                 "years": years,
    #                 "months": months,
    #                 "extract_script_loc": extract_script_loc,
    #                 "data_lake_bucket": f"gs://{BUCKET}"
    #             },
    #         )
    
    # #2. Create Dataproc cluster
    # create_dataproc_cluster_task = DataprocCreateClusterOperator(
    #     task_id="create_dataproc_cluster_task",
    #     cluster_name=CLUSTER_NAME,
    #     project_id=PROJECT_ID,
    #     region=REGION,
    #     cluster_config=CLUSTER_CONFIG,
    # )

    with TaskGroup(group_id='transformations') as transformations:
        # #3. Transformation - step 1
        # submit_pyspark_job1 = DataprocSubmitJobOperator(
        #     task_id="submit_pyspark_job1", 
        #     job=PYSPARK_JOB1, 
        #     region=REGION, 
        #     project_id=PROJECT_ID,
        #     trigger_rule='all_success'
        # )

        #4. Transformation - step 2
        submit_pyspark_job2 = DataprocSubmitJobOperator(
            task_id="submit_pyspark_job2", 
            job=PYSPARK_JOB2,
            region=REGION, 
            project_id=PROJECT_ID,
            trigger_rule='all_success'
        )

        # submit_pyspark_job1 >> submit_pyspark_job2
        submit_pyspark_job2

    # #5. Delete Dataproc cluster
    # delete_dataproc_cluster_task = DataprocDeleteClusterOperator(
    #     task_id="delete_dataproc_cluster_task", 
    #     project_id=PROJECT_ID, 
    #     cluster_name=CLUSTER_NAME, 
    #     region=REGION,
    # )

    # authenticate_service_acct_task >> transfer_to_GCS_task >> download_raw_data_task >> create_dataproc_cluster_task >> transformations >> delete_dataproc_cluster_task
    # authenticate_service_acct_task >> create_dataproc_cluster_task >> transformations >> delete_dataproc_cluster_task
    authenticate_service_acct_task >> install_pip_package_task >> transformations
