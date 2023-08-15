## Setup

### Pre-Reqs

Created a new sub-directory called `Airflow` in my `project` dir 

Set the Airflow user using the following commands:

    ```bash
    mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
