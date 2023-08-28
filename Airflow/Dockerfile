# First-time build can take upto 10 mins.

FROM apache/airflow:latest

ENV AIRFLOW_HOME=/opt/airflow

# Switch back to the airflow user
USER ${AIRFLOW_UID}
# Initialize the Airflow database
RUN airflow db init

USER root
RUN apt-get update -qq && apt-get install vim -qqq
RUN apt-get upgrade wget unzip rename -y


USER ${AIRFLOW_UID}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir sqlalchemy psycopg2-binary

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


USER root
WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID