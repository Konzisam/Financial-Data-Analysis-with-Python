## E-Charging infrastructure in Germany: Monthly Release Data Pipeline
This is my capstone project for the 2023 Data Engineering Zoomcamp. 
Previously I ran some interesting analysis of the data using [**SQL**](https://github.com/Konzisam/echarging_infrastracture_pipeline/blob/main/analysis/Charging_infrastructure_analysis_SQL.ipynb) and [**Python**](https://github.com/Konzisam/echarging_infrastracture_pipeline/blob/main/analysis/Charging_infrastructure_analysis_Python.ipynb)but wanted to build  a pipeline so that the data can be prepared for visualizaion. 

I finally got to do just that; By a trigger on the prefect UI, we fetch the data, 
transform it and load it to Google cloud storage then to Bigquery warehouse. 
It is further consumed by Looker studio, providing visualizations of key insights.\
The required infrastructure was provisioned using terraform.

### Background and dataset
In Germany the charging infrastructure has seen rapid growth over the years.
Take a case where an investor may be interested in an overview of the e-mobility trend?
They would want an all in one place dashboard, where one can see the data and compare over time, states and other parameters of intrest.
For that we need trustworthy data to work with, perform the necessary clean up, to present the required metrics succintly.

The Federal network agency website [(Bundesnetzagentur.de)](https://www.bundesnetzagentur.de/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/HandelundVertrieb/Ladesaeulenkarte/Ladesaeulenkarte_node.html), a place where companies, authorities and interested trade visitors 
can find information on the agencies’ topics, releases updated data on e-charging infrastructure. 

The data is was being updated on a monthly basis till January this year(it seems to have be paused or stopped) but still we create a pipeline that fetches the data once there a new release.

Unfortunately, its now hard to track the months and so we work with the latest release, and save it in our google cloud storage.

### Tools
- **Terraform:** Define and provision Infrastructure.
- **Docker:** to containerize code; in our case we containerize the transformation process.
- **Prefect:** to orchestrate,  trigger and monitor the entire workflow.
- **Github:** to host our code and track changes.
- **Google cloud storage:** Once data has been fetched its loaded in cloud storage, which is our data lakehouse.
- **Google Bigquery:** this is the Data warehouse.
- **Looker studio:** easily connects to bigquery and so we use it to visualize the data.
- **DBT:** In our case leveraged DBT Core version to transform the data in our warehouse and preparing it for consumption by BI tools.
- **Python:** use python library pandas to fetch the data, save a copy locally and load it to gcs bucket.

### Architechture
![pipeline](https://github.com/Konzisam/echarging_infrastracture_pipeline/blob/main/images/architechture.png)

## Flow
<ol><li>The data is fetched using pandas, initial cleaning performed so that we are able to load it to Bigquery. Bigquery has specifications of the allowed schema components  for example column names.

The task proved to be unexpectedly challenging due to schema detection discrepancies between BigQuery and pandas. Some records contained embedded commas, causing schema parsing errors. After identifying the issue, I implemented additional data cleaning steps to resolve it effectively. Below is an example of one such error.

![error](https://github.com/Konzisam/echarging_infrastracture_pipeline/blob/main/images/bigquery_error.png)

Ideally we would have loaded the data as is to GCS (data lake) and perform transformations from there but decided to keep it simple.</li>
  <li>Load the data to an external table in bigquery from GCS bucket.</li>
<li>We do not perform any partitioning and clustering as the dataset is not large.</li>
<li>Perform dbt transformation on the external table, create views on the staging schrma to see the development status and then load the transformed data to our production schema.</li>
  <li>Build visualizations of the production schema.</li></ol>
  
Below is a snapshot of the final dashboard. 
It can be found [here](https://lookerstudio.google.com/reporting/122a39cc-6be8-4bd6-b9f7-ef9c80cab32b/page/gzgND>).

![dashboard](https://github.com/Konzisam/echarging_infrastracture_pipeline/blob/main/images/echarging_dashboard.png)



## To replicate the project:

Follow [these Instructions](https://github.com/Konzisam/echarging_infrastracture_pipeline/blob/main/Replicate.md)
 
