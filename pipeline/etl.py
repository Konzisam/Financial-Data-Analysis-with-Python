from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from prefect_gcp import GcpCredentials
from prefect_gcp.bigquery import BigQueryWarehouse


@flow(retries=3)
def scrap_and_load():
    '''webscraping cities data'''
    # Scrap a table containing German cities
    html_data = requests.get('http://www.citymayors.com/gratis/german_topcities.html').text
    # Extract the relevant tables
    soup = BeautifulSoup(html_data, "html.parser")
    data = pd.read_html (str(soup))
    df_cities = data[1]
    df_cities.columns = df_cities.iloc[0]
    df_cities.drop([0], inplace = True)
    #replace sql keywords
    df_cities.rename(columns={'Rank':'City_Rank', 'State':'Federal_state'}, inplace = True)
    print(df_cities.head())
    write_local_cities(df_cities)
    cities_to_bq(df_cities)
    return df_cities

@task()
def write_local_cities(df_cities: pd.DataFrame) -> Path:
    """Write cities out locally as csv"""
    path_df_cities = Path(f"data/cities.csv")
    df_cities.to_csv(path_df_cities)
    return path_df_cities


@task()
def cities_to_bq(df_cities):
    """Load Data to BigQuery Warehouse"""

    gcp_credentials = GcpCredentials.load("echarging-gcp-creds")
    
    df_cities.to_gbq(
        destination_table=f"raw_echarging.cities",
        project_id="zoomcamp-380308",
        credentials=gcp_credentials.get_credentials_from_service_account(),
        if_exists="replace",
    )

@flow(retries=3)
def fetch_and_clean(dataset_url: str) -> pd.DataFrame:
    """Read echarging and data from web into pandas DataFrame """
    df = pd.read_csv(dataset_url, encoding='iso-8859-1', sep=';', skiprows=10)
    df_clean = clean(df)
    return df_clean
    

@task()
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Perform initial transformation"""
    # Translate headers
    df.rename(columns=lambda x: GoogleTranslator(source='auto', target='en').translate(x), 
              inplace=True)

    # Replace spaces with hyphens
    df.rename(columns=lambda x: x.replace(" ","_"), inplace=True)

    # Rename column names to bigquery allowed characters
    df.rename(columns= {'District/district-free_city':'District_district_free_city', 
                        'P1_[kW]':'Power_point_1_KW',
                        'P2_[kW]':'Power_point_2_KW' ,
                        'P3_[kW]':'Power_point_3_KW',
                        'P4_[kW]':'Power_point_4_KW'}, inplace = True)
    
    # Parse commisioning date to datetime
    df['commissioning_date'] = pd.to_datetime(df['commissioning_date'], format='%d.%m.%Y')

    # Select columns with object data type
    string_data = df.select_dtypes(include='object').columns

    # Remove leading and lagging spaces
    for column in string_data:
        df[column] = df[column].str.strip()
    df.drop(columns=['Public_Key1','address_supplement','Public_Key2', 
                     'Public_Key3', 'Public_Key4'], axis =1,inplace=True)    

    # One latitude has a dot at the end, remove it
    df['latitude'] = df.latitude.apply(lambda x: str(x).rstrip('.'))

    # Power_point_2_KW' has a forward slash,split on it and keep the first value
    df['Power_point_2_KW'] = df['Power_point_2_KW'].apply(lambda x: str(x).split('/', 1)[0])

    # Power_point_3_KW' has a forward slash, split on it and keep the first value
    df['Power_point_3_KW'] = df['Power_point_3_KW'].apply(lambda x: str(x).split('/', 1)[0])

    # Replace comma with dot and parse the data type to float
    type_replace = ['latitude','longitude', 'connected_load', 'Power_point_1_KW',
                    'Power_point_2_KW','Power_point_3_KW']

    for col in type_replace:
        df[col] = df[col].str.replace(',','.').astype('float')

    print(df.head())
    print(df.info())
    return df
    

@task()
def write_local(df_clean: pd.DataFrame) -> Path:
    """Write DataFrame out locally as csv"""
    path_df = Path(f"data/Emobility_clean.csv")
    df_clean.to_csv(path_df)
    return path_df

@task()
def write_gcs(path_df: Path) -> None:
    """Upload local file to GCS"""
    gcs_block = GcsBucket.load("echarging-gcs")
    gcs_block.upload_from_path(from_path=path_df, to_path=path_df)
    return

@task()
def load_bq(uris):
    """Load to BQ"""
    uris = ['gs://dtc_data_lake_zoomcamp-380308/data/Emobility_clean.csv']

    with BigQueryWarehouse.load("echarging-bigquery") as warehouse:
        operation = """
            CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-380308.raw_echarging.raw`
            OPTIONS (
                format = 'CSV',
                uris = %(uris)s
            );
        """
        warehouse.execute(operation, parameters={"uris": uris})

@task()
def dbt_transform():
    'Trigger dbt workflow using dbt build'
    os.system('docker-compose run --workdir="//usr/app/dbt/echarging_dbt" dbt-bq run')


@flow()
def parent_etl() -> None:
    """The main ETL function"""
    dataset_url = "https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeulenregister_CSV.csv?__blob=publicationFile&v=42"
 
    df_clean = fetch_and_clean(dataset_url)
    path_df = write_local(df_clean)
    write_gcs(path_df)
    load_bq(uris = ['gs://dtc_data_lake_zoomcamp-380308/data/Emobility_clean.csv'])
    dbt_transform()

    # Run scrap_and_load if the file cities does not exist
    path = Path(f"data/cities.csv")
    if not path.is_file():
        scrap_and_load()
    else:
        pass
        
if __name__ == "__main__":
    parent_etl()