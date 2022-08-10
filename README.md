# College Scorecard Data Pipeline [WIP]

Data pipeline for analysis of postsecondary education data. Data sourced from the College Scorecard API, Python-based ETL process orchestrated with Airflow.

![github_cover](https://user-images.githubusercontent.com/44434691/182048007-cda399cc-57c9-4779-b6d4-da21bf3d3086.jpeg)

## Table of Contents
- [Goals](#goals)
- [Architecture](#architecture)
  * [ETL Overview](#etl-overview)
  * [Project folder structure](#project-folder-structure)
- [Project Setup](#project-setup)
  * [Running Airflow in Docker](#running-airflow-in-docker)
- [References](#references)

## Goals

This project seeks to use publicly available postsecondary education data from the [College Scorecard API](https://collegescorecard.ed.gov/data/documentation/) to investigate the relationships between demographics and tuition costs. Some other potential research questions that could be explored using these data:
- Are secular instiutuions more racially diverse than religious institutions?
- What are the historic trends of enrollment at male-only/female-only institutions?
- In what regions or communities in the United States are for-profit institutions most common?

## Architecture
![college_scorecard_pipeline_architecture](https://user-images.githubusercontent.com/44434691/183802560-12861d97-bd17-4c0c-879b-b400a3cf47b3.jpg)

### ETL Overview

DAG tasks, in order of execution:
1. [x] Extract data from the U.S. Department of Education College Scorecard API
2. [x] Serialize data as `JSON` to `/data/raw/` in project directory
3. [x] Upload raw file to AWS S3 raw bucket
4. [x] Transform data with `pandas`, serialize cleaned `CSV` file to `/data/clean/`
5. [x] Upload clean file to AWS S3 clean bucket
5. [ ] Clean data is loaded into AWS RDS instance (*still under development as of 07/31/22*)

Airflow DAG graph:
![airflow_dag](https://user-images.githubusercontent.com/44434691/183805367-e733869c-a36b-4e75-81a5-4d2f52468dc2.png)


### Project folder structure

```
├── dags
│   ├── dag.py               <- Airflow DAG
│   └── dag_functions        
│       ├── extract.py       <- API extraction function
│       └── transform.py     <- data processing/cleaning function
├── data
│   ├── raw                  <- raw data pull from College Scorecard API
│   └── clean                <- processed data in CSV format
├── db_build
│   ├── create_tables.SQL    <- create table shells
│   └── create_views.SQL     <- create table views
├── dashboard.py             <- Plotly dashboard app
├── LICENSE                  <- MIT license
├── README.md                <- Top-level project README
└── docker-compose.yaml      <- Docker-Compose file w/ Airflow config
```

## Project Setup

**08/09/22**: Project is still a work in progress and potentially unstable, so running is not advised. Some preliminary instructions about Docker and Airflow configuration are provided below. Eventually I'd like to make this whole thing `pip` installable, but for now some manual setup is required.

In order to execute the DAG, you’ll need to store some information in a `.ENV` file in the top-level project directory. **You must add `.ENV` to project `.gitignore` file before publishing anything to GitHub!**

It should look something like this:
```
API_KEY=[insert College Scorecard API key here]
AWS_ACCESS_KEY_ID=[insert AWS Access Key ID here]
AWS_SECRET_ACCESS_KEY=[insert AWS Secret Access Key here]
AIRFLOW_UID=501
``` 

No need to change `AIRFLOW_UID` - this is a constant used to set up the Airflow admin.

### Running Airflow in Docker

Refer to the official [Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) for more information.

1. Install Docker and Docker-Compose first if you don’t already have it.
2. Direct a terminal to your project directory and execute the code below. This will generate `docker-compose.yaml`
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'
```
3. Make sure you've set up your `.ENV` file properly. Initialize 3 folders in your top-level directory: `/dags/`, `/logs/`, and `/plugins/`.
4. With the Docker application running on your computer, `execute docker-compose up airflow-init` in the terminal. This will initialize the Airflow instance. It will create an Admin login with username and password both set to “airflow” by default.
5. Finally, execute `docker-compose up`. This runs everything specified in `docker-compose.yaml`. You can check the health of your containers by opening a new terminal in the same directory and executing `docker ps`. You should now be able to open your web browser and go to `localhost:8080` to log in to the Airflow web client.

Execute `docker-compose down --volumes --rmi all` to stop and delete all running containers, delete volumes with database data and downloaded images.

## References

Major shout-out to [Amanda Jayapurna](https://www.amandajayapurna.com/) for designing the [cover image](https://user-images.githubusercontent.com/44434691/182048007-cda399cc-57c9-4779-b6d4-da21bf3d3086.jpeg) for this project!

Docs:
- [College Scorecard Data Documentation](https://collegescorecard.ed.gov/data/documentation/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/get-started/)
- [Requests Documentation](https://requests.readthedocs.io/en/latest/) (Python Library)

Helpful articles/videos:
- [Docker for Data Science - A Step by Step Guide](https://dagshub.com/blog/setting-up-data-science-workspace-with-docker/)
- [Airflow DAG: Coding your first DAG for Beginners](https://www.youtube.com/watch?v=IH1-0hwFZRQ)
- [Airflow Tutorial for Beginners - Full Course](https://youtu.be/K9AnJ9_ZAXE)

Architecture inspo:
- [Rust Cheaters Data Pipeline](https://github.com/jacob1421/RustCheatersDataPipeline)
- [Surfline Dashboard](https://github.com/andrem8/surf_dash)
- [GoodReads Data Pipeline](https://github.com/san089/goodreads_etl_pipeline)