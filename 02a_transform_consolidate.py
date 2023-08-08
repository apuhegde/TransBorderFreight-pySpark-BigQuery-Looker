
import argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import types
from pyspark.sql import functions as F
from pyspark.sql import DataFrame
from pyspark.sql import Window
from functools import reduce
import pandas as pd
import re
from pathlib import Path
import subprocess as s



#set up input argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--gcs_input_path', required=True)
parser.add_argument('--gcs_output_path', required=True)

args = parser.parse_args()

gcs_input_path = args.gcs_input_path
gcs_output_path = args.gcs_output_path



#set up spark configuration
spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()



#set correct schema
schema = types.StructType([
    types.StructField("MONTH", types.IntegerType(),True),
    types.StructField("YEAR", types.IntegerType(),True),
    types.StructField("TRDTYPE", types.StringType(),True),
    types.StructField("DEPE", types.StringType(),True),
    types.StructField("COUNTRY", types.IntegerType(),True),
    types.StructField("CANPROV", types.StringType(),True),
    types.StructField("MEXSTATE", types.StringType(),True),
    types.StructField("COMMODITY2", types.IntegerType(),True),
    types.StructField("CONTCODE", types.StringType(),True),
    types.StructField("DF", types.IntegerType(),True),
    types.StructField("DISAGMOT", types.IntegerType(),True),
    types.StructField("VALUE", types.IntegerType(),True),
    types.StructField("SHIPWT", types.IntegerType(),True),
    types.StructField("FREIGHT_CHARGES", types.IntegerType(),True)])




#make a list of csv file paths
gcs_input_path_recur = gcs_input_path + '/**'
popen = s.Popen(['gsutil','ls','-r',gcs_input_path_recur], stdout=s.PIPE, universal_newlines=True)
all_paths, all_paths_err = popen.communicate()
all_paths = all_paths.split("\n")
filtered = [str(x) for x in all_paths if "ytd" not in x and "dot" in x and ".csv" in x]
#filtered.sort()
#print(filtered)


#too many inconsistencies in the datasets so need to import each one individually, 
# set schema and then append to common df
years = range(2014,2024, 1)

for y in years:

    for month_num in range(1,13): #loop through each month & concatenate all dfs for each month

        month_num = f'{month_num:02}'
        print(f'Starting with date {month_num}/{y}')

        current_month_paths = []

        for path in filtered:
            if "/"+str(y)+"/" in path and "_"+month_num in path:
                current_month_paths.append(path)
        #print(current_month_paths)
        
        if(len(current_month_paths)>0):
            
            #initiate empty list to hold dataframes for current month
            df_append=[]

            for current_month_path in current_month_paths:

                #read in the CSV files
                df = spark.read.option("header", "true").csv(current_month_path)

                #add any missing columns
                missing_cols = [sn for sn in schema.names if sn not in df.columns]
                missing_cols

                if(len(missing_cols)>0):
                    for mc in missing_cols:
                        print(f"Adding missing column: {mc}")
                        df = df.withColumn(mc, F.lit(None).cast(types.StringType()))

                #drop extra columns not present in the schema
                drop_cols = [column for column in df.columns if column not in schema.names]
                len(drop_cols)

                if(len(drop_cols)>0):
                    for column in drop_cols:
                        df = df.drop(column)

                #sort columns
                df = df.select( 
                               "MONTH", 
                               "YEAR", 
                               "TRDTYPE", 
                               "DEPE", 
                               "COUNTRY", 
                               "CANPROV", 
                               "MEXSTATE", 
                               "COMMODITY2", 
                               "CONTCODE", 
                               "DF", 
                               "DISAGMOT", 
                               "VALUE", 
                               "SHIPWT", 
                               "FREIGHT_CHARGES")

                #cast columns to appropriate data types
                df = df.withColumn("MONTH", F.col("MONTH").cast(types.IntegerType()))
                df = df.withColumn("YEAR", F.col("YEAR").cast(types.IntegerType()))
                df = df.withColumn("COUNTRY", F.col("COUNTRY").cast(types.IntegerType()))
                df = df.withColumn("COMMODITY2", F.col("COMMODITY2").cast(types.IntegerType()))
                df = df.withColumn("DF", F.col("DF").cast(types.IntegerType()))
                df = df.withColumn("DISAGMOT", F.col("DISAGMOT").cast(types.IntegerType()))
                df = df.withColumn("VALUE", F.col("VALUE").cast(types.IntegerType()))
                df = df.withColumn("SHIPWT", F.col("SHIPWT").cast(types.IntegerType()))
                df = df.withColumn("FREIGHT_CHARGES", F.col("FREIGHT_CHARGES").cast(types.IntegerType()))

                #append cleaned up data to df list
                df_append.append(df)

            #union all dfs
            df_final = reduce(DataFrame.union, df_append)

            #add unique ID column
            df_final = df_final.withColumn("ID",F.row_number().over(Window.orderBy(F.monotonically_increasing_id())))

            df_final = df_final.select(F.concat_ws('_',df_final.ID,df_final.MONTH,df_final.YEAR).alias("INDEX"), "*")

            df_final = df_final.drop("ID")


            #write to file
            # new_path = re.sub(r"dot[0-9]_", r"dot_all_", current_month_path)
            # new_path = re.sub(".csv", ".pq", new_path)
            new_gcs_path = gcs_output_path + "/" + "raw_cleanedup_pq" + "/" + str(y)
            new_file = current_month_path.split("/")[-1]
            new_file = re.sub(".csv", ".pq", new_file)
            new_path = new_gcs_path + "/" + new_file

            df_final.repartition(4).write.parquet(new_path, mode="overwrite")

            print(f"Finished consolidating {month_num} datasets!")           
        
        else:
            print(f'{month_num}/{y} has no data! Moving to next dataset')
    print(f'Done with {y}!')
print('Done with all years!')

print("Final schema is:")
df_final.printSchema()