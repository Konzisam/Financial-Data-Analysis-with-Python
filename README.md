## E-Charging infrastructure in germany: Monthly Release Pipeline
I have been  working on this project for a while and decided to make it my capstone project for the 2023 Data Engineering Zoomcamp. 
Previously I ran some cohorrt analysis of the data using **SQL** and **python**.
I wanted to build  a pipeline so that the data can be prepared for visualizaion easily. 

With this project we do just that; By a trigger on the prefect UI, we fetch the data, 
transform it and load it to Google cloud storage then to Bigquery warehouse. 
It is further consumed by Looker studio, providing visualizations of key insights.

### Background and dataset
In Germany the charging infrastructure has seen rapid growth over the years.
Take a case where an investor may be interested in an overview of the e-mobility trend?
We would want an all in one place where one can see the data and compare over time, states and other parameters of intrest.
For that we need trustworthy data to work with.

The Federal network agency website (Bundesnetzagentur.de), a place where companies, authorities and interested trade visitors 
can find information on the agencies’ topics,releases updated data on e-charging infrastructure. 

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

