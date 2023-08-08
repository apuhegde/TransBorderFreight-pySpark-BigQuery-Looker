#!/bin/bash


gcloud dataproc jobs submit pyspark \
    --cluster=tbf-analysis-cluster \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://tbf-analysis-forbigquery/code/02b_transform_joinwithmetadata.py \
    -- \
        --gcs_input_path=gs://tbf-analysis-forbigquery/raw_cleanedup_pq/ \
        --bq_output=tbf_with_metadata.data-for-reporting \
        --metadata_file=gs://tbf-analysis/metadata/TransBorderCodes.xls \
        --temp_gcs_bucket=dataproc-temp-us-central1-409813947723-fz9jirko