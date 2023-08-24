# **Analysis of transborder freight data between the USA, Canada and Mexico**

The last few years have witnessed significant developments in North American trade, including the renegotiation of NAFTA into the USMCA, trade tensions and tariff disputes due to changing governments, and the impact of the COVID-19 pandemic. I was interested in analyzing the effect of these events on historical trends in transborder trade between the three biggest countries in North America - USA, Canada and Mexico. The raw data has been made available by the Bureau of Transportation Statistics (BTS), Department of Transportation (DOT), Government of the United States and can be found here: [Bureau of Transportation Statistics Transborder Freight Raw Data](https://www.bts.gov/topics/transborder-raw-data).

## Objective

My objective was to build a robust data ingestion and processing pipeline that would deliver reliable, reproducible and clean data for analysis, insight generation and possible decision-making regarding North American Transborder trade.

## Technologies

I used the following tools to set up the pipeline:

- Terraform for cloud infrastructure provisioning
- Google Cloud Project (GCP) for:
    - data lake storage (Google Cloud Storage, GCS)
    - data warehouse storage (BigQuery)
    - Spark job processing (Dataproc)
    - data visualization + analysis (Looker Studio)
- Docker/Docker Compose for containerization
- Airflow for workflow orchestration
- Apache Spark for distributed batch data processing

## Data description

The raw data is made available by the Bureau of Transportation Statistics. It is collected and processed by multiple agencies and organizations (public and private), via multiple approaches including administrative data required by regulation and surveys, from both carriers and shippers. A more thorough description of the data can be found here: [North American Transborder Freight Data FAQs](https://www.bts.gov/statistical-products/transborder-freight-data/north-american-transborder-freight-data-faqs)

The data is in .csv format and is updated on the BTS website on a monthly basis. There is also a metadata file that accompanies the raw data, which details the codes used in the raw data files. The metadata is available in excel and pdf format, with the pdf file containing additional information than what is available in the excel file. Therefore, before using the metadata for this project, I manually curated and reconciled the excel and the pdf files. I’ve used this cleaned up metadata excel file as my input file, available here: [TransBorderCodes.xls](TransBorderCodes.xls)

## Project overview

![Data pipeline overview](TBF_analysis_pipeline_overview.png)

Overview of the Transborder Freight data processing pipeline