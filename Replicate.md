## To replicate the project follow the steps below:

Here are initial guidelines to  install the required tools.
  
**Terraform:** [Installation guide](https://developer.hashicorp.com/terraform/downloads)
  
**Python:** My installation is done [anaconda](https://www.anaconda.com/download/);Use the relevant commands when it comes to creating the environment)
  
**Google cloud CLI:** [Installation Guide](https://cloud.google.com/sdk/docs/install)
  
**Prefect CLI:** Installed in the instructions
  
**Docker:** Find docker [here](https://docs.docker.com/get-docker)
  
**DBT Core:** Installed in the instructions
  
**Git and a Github Repository:** Download git [here](https://git-scm.com/downloads) and create a repository [here](https://github.com/) 
  if you dont have one
  
 ## Steps
  
1. Clone this repository
2. Create a new environment
  - Install dependencies using the command `pip install -r requirements.txt`
3. GCP set up
  - Log in to GCP and create a project
  - Set up Google cloud CLI as in the [guide](https://cloud.google.com/sdk/docs/install)
  - Create a service account assigning the rights to interact with the  various resources (Bigquery, GCS Bucket).
  - Create the raw, staging and production datasets in bigquery. In the script we only use raw and production, but for development its best practise to use staging. 

4. Set up the infrastructure needed using terraform
- Run `terraform init` , then `terraform plan` ( see an overview), then `terraform apply` to set up the infrastructure.

5. Follow [these steps](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_4_analytics_engineering/docker_setup) to run dbt and bigquery using docker.


6. Prefect is already installed, when we ran requirements.txt so tart prefect orion server locally
  - Open another terminal window and activate the environment (`conda activate <your environment name>`)
  - Register GCP Blocks using the command: `prefect block register -m prefect_gcp`
  - Create prefect GCP blocks on the prefect UI or using [this](https://github.com/discdiver/prefect-zoomcamp/blob/main/blocks/make_gcp_blocks.py) code: 
In our case, we do not require dbt blocks as dbt is running on docker and so we trigger it inside our script instead of using a prefect block. 

At this point you can actuall run the flow but using the command line. By running `python etl.py`, the script will run, calling all the processes in the flow.

To go further and create a prefect deployment:

7. Create  and apply deployments by running the following command. 
`prefect deployment build ./your-main-flow -n  “parent_etl”` (this is the name of the main flow function)
It creates a 'parent_etl-deployment.yaml` file with metadata required by the agent to trigger the flow.

8. Next run the command: `prefect deployment apply parent_etl-deployment.yaml`. 
9. Run the command `prefect agent start --work-queue "default"`
10. On the Prefec UI if we trigger a quick run, the data will be loaded to GCS and big query and we see logs of the process. 


  
  
