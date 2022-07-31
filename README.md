# College Scorecard Data Pipeline

Introduction sentence goes here.

![github_cover](https://user-images.githubusercontent.com/44434691/182048007-cda399cc-57c9-4779-b6d4-da21bf3d3086.jpeg)

## Architecture
![piipeline_architecture](https://user-images.githubusercontent.com/44434691/182048113-0e660af9-ccc9-45ee-b2cf-e74bccd232f5.jpg)

### ELT Overview

DAG tasks, in order of execution:
1. Data is extracted from the U.S. Department of Education [College Scorecard API](https://collegescorecard.ed.gov/data/documentation/).
2. Raw `JSON` file is uploaded to Amazon S3 bucket.
3. Data is processed with `pandas` and serialized to `csv`.
4. Cleaned `csv` is uploaded to Amazon S3 bucket.
5. Clean data is loaded into Amazon Redshift data warehouse.

### Project folder structure

```
├── LICENSE
├── README.md                <- Top-level README file
├── docker-compose.yaml      <- Compose file 
├── dags
│   ├── dag.py               <- Main Airflow DAG
│   └── dag_functions        <- Functions used in DAG
│       ├── extract.py
│       └── transform.py
├── data
│   ├── raw                  <- Raw data pull from College Scorecard API
│   ├── clean                <- Processed data in CSV format
│   └── xwalks               <- Variable crosswalks
└── dashboard.py             <- Plotly dashboard app
```

## How to run

## Analysis

## Reflection

## References
