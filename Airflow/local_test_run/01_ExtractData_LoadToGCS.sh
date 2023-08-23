#!/bin/bash

URL=$1
YEAR=$2
DATA_LAKE_BUCKET=$3

# exit when any command fails
#set -e

# #make new work_dir
# mkdir work_dir
# cd work_dir

cwd=$(pwd)

wget $URL -O temp.zip
unzip -d temp temp.zip
cd temp

#find zip files from all subdirectories and remove spaces from their file names
echo 'finding all zips & renaming'
find . -name '*.zip' | rename -v "s/ /_/g"

#find zip files from all subdirectories and unzip their contents into current dir
echo 'finding all zips and unzipping'
find . -name '*.zip' -exec sh -c 'unzip -d . {}' ';'

#find CSVs from all subdirectories and move to current folder for ease of processing
echo 'finding all csvs and moving to current folder'
find . -name '*.csv' -exec mv -v {} . \;

#clean up all unnecessary folders from this directory
echo 'purging dirs'
rm -r */

#copy to GCS
echo 'copying to GCS destination:'
echo $DATA_LAKE_BUCKET/raw/csv/$YEAR/
gsutil -m cp *.csv $DATA_LAKE_BUCKET/raw/csv/$YEAR/

#delete .csv files
echo 'purging csv files'
rm *.csv

#exit from dir & delete it
echo 'exiting from temp dir'
cd $cwd
echo 'Current dir is:'
echo $PWD
rm -r temp
