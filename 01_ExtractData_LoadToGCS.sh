#!/bin/bash

URL=$1
YEAR=$2

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
echo 'copying to GCS'
gsutil -m cp *.csv gs://tbf-analysis/$YEAR/

#delete .csv files
echo 'purging csv files'
rm *.csv

#exit from dir & delete it
echo 'exiting from temp dir'
cd ../
rm -r temp