# College Scorecard Data Pipeline [WIP]

**scorecard_pipeline** is an end-to-end data pipeline following an ETL process. This project is a work in progress.

![github_cover](https://user-images.githubusercontent.com/44434691/182048007-cda399cc-57c9-4779-b6d4-da21bf3d3086.jpeg)

## Table of Contents
- [Architecture](#architecture)
  * [ETL Overview](#etl-overview)
  * [Project folder structure](#project-folder-structure)
- [How to Run](#how-to-run)
- [Analysis](#analysis)
- [Reflection](#reflection)
  * [Limitations](#limitations)
  * [Next Steps](#next-steps)
- [Contributions and References](#contributions-and-references)

## Architecture
![scorecard_pipeline_architecture](https://user-images.githubusercontent.com/44434691/182258424-4c132bee-faeb-490f-bddb-93809dacd2eb.jpg)

### ETL Overview

DAG tasks, in order of execution:
1. Data is extracted from the U.S. Department of Education [College Scorecard API](https://collegescorecard.ed.gov/data/documentation/).
2. Raw `JSON` file is uploaded to Amazon S3 bucket.
3. Data is processed with `pandas` and serialized to `csv`.
4. Cleaned `csv` is uploaded to Amazon S3 bucket.
5. Clean data is loaded into Amazon Redshift data warehouse.

### Project folder structure

```
├── LICENSE
├── README.md                <- top-level README file
├── docker-compose.yaml      <- compose file
├── Dockerfile               <- Docker requirements extension
├── dags
│   ├── dag.py               <- Airflow DAG
│   └── dag_functions        
│       ├── extract.py       <- API extraction function
│       └── transform.py     <- data processing/cleaning function
├── db_build
│   ├── create_tables.SQL    <- create table shells
│   └── create_views.SQL     <- create table views
├── data
│   ├── raw                  <- raw data pull from College Scorecard API
│   └── clean                <- processed data in CSV format
└── dashboard.py             <- plotly dashboard app
```

## How to Run

## Analysis

## Reflection

### Limitations
### Next Steps

## References
