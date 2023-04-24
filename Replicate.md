## To replicate the project follow the steps below:

Here are initial guidelines to  install the required tools.
  
**Terraform:**
  
**Python:** My installation is done [anaconda](https://www.anaconda.com/download/);Use the relevant commands when it comes to creating the environment)
  
**Google cloud CLI:** [Installation Guide](https://cloud.google.com/sdk/docs/install)
  
**Prefect CLI:** Installed in the instructions
  
**Docker:** Find docker [here](https://docs.docker.com/get-docker)
  
**DBT Core:** Installed in the instructions
  
**Git and a Github Repository:** Download git [here](https://git-scm.com/downloads) and create a repository [here](https://github.com/) 
  if you dont have one
  
 ## Steps
  
1. Clone the repository
2. Create a new environment
  - Pip install -r requirements.txt
3. GCP set up
  - Log in to GCP and create a project
  - Set up Google cloud CLI as in the guide
  - Create a service account that can interact with rights to interact with the  various resources (Bigquery, GCS Bucket).
  - Create the raw, staging and production datasets in bigquery which we will call from our script later. 

4. Set up the infrastructure needed using terraform
- Run terraform init , then terraform plan ( see an overview), then terraform apply to set up the infrastructure.

5. Follow [these steps](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_4_analytics_engineering/docker_setup) to run dbt and bigquery using docker.


6. Prefect is already installed, when we ran requirements.txt

7. Start prefect orion server locally
  - Open another terminal window and activate the environment (`conda activate <your environment name>`)
  - Register GCP Blocks using the command: `prefect block register -m prefect_gcp`
  - Create prefect GCP blocks on the prefect UI or using [this](https://github.com/discdiver/prefect-zoomcamp/blob/main/blocks/make_gcp_blocks.py) code: 
In our dcase, we do not require dbt blocks as dbt is running on docker and so we trigger it inside our script instead of using a prefect block. 
8. Create  and apply deployments. For deployment you require the following command. 
`prefect deployment build ./your-main-flow -n  “parent_etl”` (this is the name of the main flow function)
It creates a parent_etl-deployment.yaml with metadata required by the agent to trigger the flow.

9. Next run the command: `prefect deployment apply parent_etl-deployment.yaml'. 
10. Run the command `prefect agent start --work-queue "default"`
11. On the Prefec UI if we trigger a quick run, the data will be loaded to GCS and big query and we see logs of the process. 


  
  
