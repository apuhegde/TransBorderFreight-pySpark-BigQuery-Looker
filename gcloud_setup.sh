#!/bin/bash

gcloud auth activate-service-account terraform@trans-border-freights-394419.iam.gserviceaccount.com --key-file /home/ahegde/.google/credentials/google_credentials.json

gsutil cp ~/TransBorderFreight-pySpark-BigQuery-Looker/02a_transform_consolidate.py gs://tbf-analysis-terraform_trans-border-freights-394419/code/02a_transform_consolidate.py
gsutil cp ~/TransBorderFreight-pySpark-BigQuery-Looker/02b_transform_joinwithmetadata.py gs://tbf-analysis-terraform_trans-border-freights-394419/code/02b_transform_joinwithmetadata.py
gsutil cp ~/TransBorderFreight-pySpark-BigQuery-Looker/TransBorderCodes.xls gs://tbf-analysis-terraform_trans-border-freights-394419/metadata/TransBorderCodes.xls
