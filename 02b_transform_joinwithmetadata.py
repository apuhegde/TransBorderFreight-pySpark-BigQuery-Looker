import argparse
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql import Window

#Install xlrd for pandas when running for the first time
# import conda.cli.python_api as Conda
# import sys

# (stdout_str, stderr_str, return_code_int) = Conda.run_command(
#     Conda.Commands.INSTALL,
#     [ 'xlrd'],
#     use_exception_handler=True,
#     stdout=sys.stdout,
#     stderr=sys.stderr,
#     search_path=Conda.SEARCH_PATH
# )

import pandas as pd

#set up input argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--gcs_input_path', required=True)
parser.add_argument('--bq_output', required=True)
parser.add_argument('--metadata_file', required=True)
parser.add_argument('--temp_gcs_bucket', required=True)
#parser.add_argument('--credentials_path', required=True)

args = parser.parse_args()

gcs_input_path = args.gcs_input_path
gcs_input_path=gcs_input_path+"/**/*"
print(f'gcs_input_path is {gcs_input_path}')
temp_gcs_bucket = args.temp_gcs_bucket
metadata_file = args.metadata_file
print(f'Metadata file path is {metadata_file}')
bq_output = args.bq_output



#set up spark configuration
spark = SparkSession.builder \
        .appName('test') \
        .getOrCreate()



#1. trade type
print("starting with metadata file ingestion")
print("1. trade type")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='Trade_type_code_TRDTYPE', 
                    skiprows = 2)
meta_df.rename(columns=lambda x: x.replace(" ",""), inplace=True)
meta_df['TradeType'] = meta_df['TradeType'].astype('str')
trade_type = spark.createDataFrame(meta_df)
# trade_type.show()

#2. transport mode type
print("2. transport mode")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='MODES', 
                    skiprows = 2)
meta_df['Description'] = meta_df['Description'].astype('str')
transport_mode = spark.createDataFrame(meta_df)
# transport_mode.show()

#3. country
print("3. country")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='Country_Codes', 
                    skiprows = 2)
meta_df['Country'] = meta_df['Country'].astype('str')
country = spark.createDataFrame(meta_df)
# country.show()

#4. domestically produced or foreign produced
print("4. domestic or foreign")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='Domestic_Foreign_Code_DF', 
                    skiprows = 2)
meta_df.rename(columns=lambda x: x.replace(" ",""), inplace=True)
meta_df['DomesticorForeign'] = meta_df['DomesticorForeign'].astype('str')
domesticforeign = spark.createDataFrame(meta_df)
# domesticforeign.show()

#5. containerized or not
print("5. container")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='Container_Code_CONTCODE', 
                    skiprows = 2)
meta_df['Code'] = meta_df['Code'].astype('str')
meta_df['Containerized'] = meta_df['Containerized'].astype('str')
container = spark.createDataFrame(meta_df)
# container.show()

#6. Ports and US state names
print("6. ports")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='PORT_Codes', 
                    skiprows = 2)
meta_df.rename(columns=lambda x: x.replace(" ",""), inplace=True)
meta_df['Districtcode'] = meta_df['Districtcode'].astype('str')
meta_df['Portcode'] = meta_df['Portcode'].astype('str')
meta_df['Portname'] = meta_df['Portname'].astype('str')
meta_df['USAstate'] = meta_df['USAstate'].astype('str')
ports = spark.createDataFrame(meta_df)
# ports.show()

#7. Commodity types
print("7. commodity")
meta_df = pd.read_excel((metadata_file), 
                    sheet_name='COMM_Codes', 
                    skiprows = 2)
meta_df.rename(columns=lambda x: x.replace(" ",""), inplace=True)
meta_df['Code'] = meta_df['Code'].astype('int')
meta_df['Commoditydescription'] = meta_df['Commoditydescription'].astype('str')
commodity = spark.createDataFrame(meta_df)
# commodity.show()



#import pq file
print("Reading parquet files from GCS")
df_pq = spark.read.parquet(gcs_input_path)
print(df_pq.count())



#join with metadata
print("Joining with metadata")
#trade type data
df_pq = df_pq.join(trade_type, df_pq.TRDTYPE ==  trade_type.Code,"left")
df_pq = df_pq.drop("Code", "TRDTYPE")
df_pq = df_pq.withColumnRenamed("TradeType","TRADETYPE")
#df_pq.show()

#transport mode data
df_pq = df_pq.join(transport_mode, df_pq.DISAGMOT ==  transport_mode.Code, "left")
df_pq = df_pq.drop("Code", "DISAGMOT")
df_pq = df_pq.withColumnRenamed("Description","TRANSPORT_MODE")
#df_pq.show()

#country data
df_pq = df_pq.join(country, df_pq.COUNTRY ==  country.Code, "left").drop(df_pq.COUNTRY)
df_pq = df_pq.drop('Code')
df_pq = df_pq.withColumnRenamed("Country","COUNTRY")
#df_pq.show()

#DF data
df_pq = df_pq.join(domesticforeign, df_pq.DF ==  domesticforeign.Code, "left")
df_pq = df_pq.drop('Code', 'DF')
df_pq = df_pq.withColumnRenamed("DomesticorForeign","DOMESTIC_FOREIGN")
#df_pq.show()

#container data
df_pq = df_pq.join(container, df_pq.CONTCODE ==  container.Code, "left")
df_pq = df_pq.drop('Code', 'CONTCODE')
df_pq = df_pq.withColumnRenamed("Containerized","CONTAINERIZED")
#df_pq.show()

#port data
df_pq = df_pq.join(ports, df_pq.DEPE ==  ports.Portcode, "left").drop(ports.Districtcode)
df_pq = df_pq.drop('Portcode', 'DEPE')
df_pq = df_pq.withColumnRenamed("Portname","PORT")
df_pq = df_pq.withColumnRenamed("USAstate","USASTATE")
#df_pq.show()

#commodity data
df_pq = df_pq.join(commodity, df_pq.COMMODITY2 ==  commodity.Code, "left")
df_pq = df_pq.drop('Code', 'COMMODITY2')
df_pq = df_pq.withColumnRenamed("Commoditydescription","COMMODITY")

df_pq.show()



#Add a partition-index column to flatten the write directories:
print("Partitioning data")
df_pq = df_pq.select(F.concat_ws('_',df_pq.YEAR,df_pq.MONTH).alias("PARTITION_ID"), "*")
df_pq.show()



#partition data by month and year
Windowspec = Window.partitionBy("PARTITION_ID").orderBy("INDEX")

#add row numbers
print("adding row numbers")
df_pq = df_pq.select(F.row_number().over(Windowspec).alias("PARTITION_ROW_NUM"), "*")
df_pq.show()



#write data to BigQuery
print("writing to BigQuery")

df_pq.write.format("bigquery") \
    .option("header", True) \
        .option("temporaryGcsBucket",temp_gcs_bucket) \
            .mode("overwrite") \
                .option('table', bq_output) \
                    .save()