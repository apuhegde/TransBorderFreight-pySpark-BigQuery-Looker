import importlib
construct_download_URL = importlib.import_module("01_Construct_URL", package=None)


URL_PREFIX = 'https://www.bts.gov/sites/bts.dot.gov/files/transborder-raw'
years = range(2018,2024, 1)
months = range(1, 13)
extract_script_loc = '/Users/ahegde/Job_misc/Portfolio/TransBorderFreightAnalysis/VM_project_files/TransBorderFreight-pySpark-BigQuery-Looker/Airflow/dags/01_ExtractData_LoadToGCS.sh'
BUCKET = 'tbf-analysis-terraform_trans-border-freights-394419'


construct_download_URL.construct_download_URL(URL_PREFIX = URL_PREFIX, 
                       years = years, 
                       months = months, 
                       extract_script_loc = extract_script_loc,
                       data_lake_bucket = f"gs://{BUCKET}")