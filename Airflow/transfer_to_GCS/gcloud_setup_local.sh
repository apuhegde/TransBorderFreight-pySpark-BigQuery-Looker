#!/bin/bash

#gcloud auth activate-service-account terraform@trans-border-freights-394419.iam.gserviceaccount.com --key-file /home/ahegde/.google/credentials/google_credentials.json

BUCKET=$1

echo "Bucket is:"
echo ${BUCKET}

gsutil -m cp /opt/airflow/transfer_to_GCS/02a_transform_consolidate.py ${BUCKET}/code/
gsutil -m cp /opt/airflow/transfer_to_GCS/02b_transform_joinwithmetadata.py ${BUCKET}/code/
gsutil -m cp /opt/airflow/transfer_to_GCS/TransBorderCodes.xls ${BUCKET}/metadata/
