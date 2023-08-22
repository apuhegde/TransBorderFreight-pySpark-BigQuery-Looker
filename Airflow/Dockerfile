# First-time build can take upto 10 mins.

FROM apache/airflow:2.4.1

#ENV AIRFLOW_UID=50000
ENV AIRFLOW_HOME=/opt/airflow
#dir location of raw data extraction bash script
#ENV DAGS_LOC=/Users/ahegde/Job_misc/Portfolio/TransBorderFreightAnalysis/VM_project_files/TransBorderFreight-pySpark-BigQuery-Looker/Airflow/dags
#ENV AIRFLOW_HOME=/usr/local/airflow

USER root
RUN apt-get update -qq && apt-get install vim -qqq
#git gcc g++ -qqq
RUN apt-get upgrade wget unzip rename -y
# RUN apt-get -y install wget
# RUN apt-get -y install unzip
# RUN apt-get -y install rename

USER ${AIRFLOW_UID}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir sqlalchemy psycopg2-binary
#RUN pip install --no-cache-dir xlrd pyspark functools pandas

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

USER root
SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

ARG CLOUD_SDK_VERSION=322.0.0
ENV GCLOUD_HOME=/home/google-cloud-sdk

ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"

RUN DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/google-cloud-sdk.tar.gz" \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "${TMP_DIR}/google-cloud-sdk.tar.gz" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
       --bash-completion=false \
       --path-update=false \
       --usage-reporting=false \
       --quiet \
    && rm -rf "${TMP_DIR}" \
    && gcloud --version


#clone git repo and transfer scripts to GCS bucket for dataproc
#RUN cd TransBorderFreight-pySpark-BigQuery-Looker

# RUN gsutil cp gs://tbf-analysis-terraform_trans-border-freights-394419/code/01_Construct_URL.py /opt/airflow
# RUN gsutil cp gs://tbf-analysis-terraform_trans-border-freights-394419/code/01_ExtractData_LoadToGCS.sh /opt/airflow
#RUN gcloud auth activate-service-account terraform@trans-border-freights-394419.iam.gserviceaccount.com --key-file /home/ahegde/.google/credentials/google_credentials.json
#RUN gsutil cp ~/TransBorderFreight-pySpark-BigQuery-Looker/02a_transform_consolidate.py gs://tbf-analysis-terraform_trans-border-freights-394419/code/02a_transform_consolidate.py
#RUN gsutil cp ~/TransBorderFreight-pySpark-BigQuery-Looker/02b_transform_joinwithmetadata.py gs://tbf-analysis-terraform_trans-border-freights-394419/code/02b_transform_joinwithmetadata.py
#RUN gsutil cp ~/TransBorderFreight-pySpark-BigQuery-Looker/TransBorderCodes.xls gs://tbf-analysis-terraform_trans-border-freights-394419/metadata/TransBorderCodes.xls
#RUN export PYTHONPATH=/opt/airflow/:$PYTHONPATH

# USER ${AIRFLOW_UID}
# RUN gcloud auth activate-service-account terraform@trans-border-freights-394419.iam.gserviceaccount.com --key-file /.google/credentials/google_credentials.json

# WORKDIR /Users/ahegde/

# RUN mkdir -p ~/.google/credentials
# COPY /Users/ahegde/.google/credentials/google_credentials.json ~/.google/credentials

USER root
WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID