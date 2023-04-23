## E-Charging infrastructure in germany: Monthly Release Automation Pipeline
I have been  working on this project for a while and decided to make it my capstone project for the 2023 Data Engineering Zoomcamp. 
I have previously done some cohorrt analysis of the data using **SQL** and **python**.
I wanted to build  a pipeline so that the data can be prepared for visualizaion easily. 

With this project we do just that; By a trigger on the prefect UI, we fetch the data, 
transform it and load it to Google cloud storage then to Bigquery warehouse. 
It is further consumed by Looker studio, providing visualizations of key insights.

## Background and dataset
In Germany the charging infrastructure has seen rapid growth over the years.
Take a case where an investor may be interested in an overview of the e-mobility trend?
We would want an all in one place where on can see the data and compare over time, states and other parameters.
For that we need trustworthy data to work with.

The Federal network agency website (Bundesnetzagentur.de), a place where companies, authorities and interested trade visitors 
can find information on the agencies’ topics,releases updated data on e-charging infrastructure. 

The data is was being updated on a monthly basis till January this year(it seems to have be paused or stopped) but still we create a pipeline that fetches the data once there a new release.
