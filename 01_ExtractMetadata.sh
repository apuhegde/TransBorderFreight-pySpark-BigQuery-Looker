#!/bin/bash

URL="http://cms.bts.dot.gov/sites/bts.dot.gov/files/2022-04/TransBorder%20Codes.xlsx"

#download file
wget $URL -O DataDotGov_TransBorderCodes.xlsx

#copy to GCS
#gsutil -m cp DataDotGov_TransBorderCodes.xlsx gs://tbf-analysis/metadata/

