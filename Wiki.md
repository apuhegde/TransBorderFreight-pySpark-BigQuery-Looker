# Trans-border freight analysis

## Steps to recreate the project

### A. Set up GCS account, GCS bucket and VM instance

1. Set up google cloud project (I’ve called mine “trans-border-freights-394419”) and VM instance (make sure to give full access to the service account while setting up the VM!), service account permissions, gcloud authentication and ssh access (detailed instructions: [https://medium.com/google-cloud/how-to-use-multiple-accounts-with-gcloud-848fdb53a39a](https://medium.com/google-cloud/how-to-use-multiple-accounts-with-gcloud-848fdb53a39a). Also you will have to run `gcloud compute config-ssh` each time you start the VM before SSHing, see these instructions: [https://github.com/ziritrion/dataeng-zoomcamp/tree/c4447687719f76ca04cedfcc1ac8f8ad23eb0cde/7_project#create-a-vm-instance](https://github.com/ziritrion/dataeng-zoomcamp/tree/c4447687719f76ca04cedfcc1ac8f8ad23eb0cde/7_project#create-a-vm-instance))
2. Set up new GCS bucket in project (I’ve called mine “tbf-analysis”)
3. SSH into your VM, set your python path in your ~/.profile file on your VM so it’s always able to find python ([https://unix.stackexchange.com/questions/552328/pythonpath-is-not-working-at-all](https://unix.stackexchange.com/questions/552328/pythonpath-is-not-working-at-all)) (To find your python path, start python3 and run the following):
    
    ```python
    import sys
    print(sys.path)
    ```
    
4. Run `sudo apt update && sudo apt -y upgrade` 
5. Install prereqs like java and spark (links: [https://stackoverflow.com/a/52950746/3276842,](https://stackoverflow.com/a/52950746/3276842) [https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md), [https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/pyspark.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/pyspark.md)).
    1. Manual spark installation did not work for me - when running in jupyter notebook, I still got “pyspark not found” error. So I resorted to installing pyspark via pip. It installed it in `/home/ahegde/.local/bin/pyspark`
6. Generate SSH key credentials, download to local terminal and transfer to VM. Export path within the VM as environment variable (follow [https://github.com/ziritrion/dataeng-zoomcamp/tree/c4447687719f76ca04cedfcc1ac8f8ad23eb0cde/7_project#create-a-google-cloud-project](https://github.com/ziritrion/dataeng-zoomcamp/tree/c4447687719f76ca04cedfcc1ac8f8ad23eb0cde/7_project#create-a-google-cloud-project))
7. Ubuntu 20.4 usually comes with python3 as well as jupyter installed. If running `jupyter notebook` doesn’t work, it probably means it’s not installed. So if it isn’t, install jupyter using pip3 (`pip3 install jupyter`). Add jupyter to path (`export PATH=$PATH:/home/ahegde/.local/bin/jupyter`), source your bash rc file and try running jupyter. If it still says command not found, run jupyter using the command `python3 -m notebook`
8. You may have to run `gcloud auth login` on VM shell to be able to access GCS bucket

### B. Extract data files + Load into data lake (GCS)

1. From inside your VM, run the scripts `01_Construct_URL.py` to download raw data from [https://www.bts.gov/topics/transborder-raw-data](https://www.bts.gov/topics/transborder-raw-data) into GCS
2. Download metadata excel file from [https://www.bts.gov/transborder](https://www.bts.gov/transborder) . This file is missing some metadata info that is available in the PDF on the same webpage. I manually added this data into the excel, as well as performed some clean up in terms of excel sheet headers, USAstate column in the port_codes sheet, etc. This complete, cleaned-up excel file is available in the github repo. Upload this complete excel file into GCS as well by running the gsutil line of code (commented out) from `01_ExtractMetadata.sh` in the VM shell. 

### C. Set up a pySpark cluster using Dataproc

1. Enable the Cloud Dataproc API. Create a new pySpark cluster (I’ve named mine “tbf-analysis-cluster”). Preferably use the same region as your GCS bucket. Add any additional optional components you may desire (I added Jupyter Notebook and Docker, just in case, for the future.) This automatically creates a VM instance that is associated with the Dataproc cluster. I followed detailed instructions from this video: [https://www.youtube.com/watch?v=osAiAYahvh8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=56](https://www.youtube.com/watch?v=osAiAYahvh8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=56)
2. Add dataproc administrator permissions to the service account you are using

### D. Transform data and Load into data warehouse (BigQuery)

3. Upload scripts `02a_transform_consolidate.py` and `02b_transform_joinwithmetadata.py` to GCS bucket (in my case, I created a new bucket for BigQuery table storage, called “tbf-analysis-forbigquery”.)
4. In the accompanying bash script `02a_transform_consolidate_submitjobs.sh` replace the arguments `-cluster` , `-region` , gsutil path to the `02a_transform_consolidate.py` script on GCS bucket, `-gcs_input_path` and `-gcs_output_path` with your own input/output bucket name(s) and information. 
5. Run this bash script in the VM
6. In the accompanying bash script `02b_transform_joinwithmetadata_submitjobs.sh` replace the arguments `-cluster` , `-region` , gsutil path to the `02b_transform_joinwithmetadata.py` script on GCS bucket, `-gcs_input_path`, `-bq_output`, `-metadata_file` and `-temp_gcs_bucket` with your own input/output bucket name(s) and information. `-temp_gcs_bucket` is the name of the temporary GCS bucket associated with your Dataproc cluster. 
7. Run this bash script in the VM

### E. Orchestration with Airflow

This section is still a work in progress. I plan to use a Python operator for the Extraction-Load steps (`01_Construct_URL.py`), bash operator to transfer the metadata excel file to GCS, and bash operators for the Transformation-Load steps (`02a_transform_consolidate_submitjobs.sh` and `02b_transform_joinwithmetadata_submitjobs.sh`).
