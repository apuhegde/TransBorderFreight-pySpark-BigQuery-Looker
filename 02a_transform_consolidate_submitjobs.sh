#!/bin/bash

gcloud dataproc jobs submit pyspark \
    --cluster=tbf-analysis-cluster \
    --region=us-central1 \
    gs://tbf-analysis-forbigquery/code/02a_transform_consolidate.py \
    -- \
        --gcs_input_path=gs://tbf-analysis \
        --gcs_output_path=gs://tbf-analysis-forbigquery