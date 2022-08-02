import pandas as pd
import json
import csv

def transform_scorecard(file_path):
    """Take JSONL, clean and transform, and spit out a csv."""

    # init list to store data
    in_data = []

    # load each line (row) of JSONL object and append to list
    with open(file_path) as f:
        for row in f:
            in_data.append(json.loads(row))

    # convert list to DataFrame object
    df = pd.DataFrame(in_data)

    # melt long
    df_long = pd.melt(df,
        id_vars=[
            'school.name',
            'school.state',
            'school.ownership',
            'school.region_id',
            'school.religious_affiliation',
            'school.minority_serving.historically_black',
            'school.men_only',
            'school.women_only',
            'id',
            'ope6_id',
            'data_year',
            ]
        )

    # format variable names, removing year prefix
    def clean_variable_names(x):
        x = x.split('.')
        del x[0]
        x = '_'.join(x)
        return(x)

    df_long["variable"] = df_long["variable"].map(clean_variable_names)

    # more variable name standardization
    df_long["variable"] = df_long["variable"].str.replace('student_demographics_race|student_share', 'pct', regex=True)

    # standardize ID colnames
    df_long.columns = df_long.columns.str.replace("school.", "", regex=True)
    df_long = df_long.rename(columns={
        'region_id': 'region',
        'minority_serving.historically_black': 'flag_historically_black',
        'men_only': 'flag_men_only',
        'women_only': 'flag_women_only',
        'id': 'ipeds_id'
        })

    # remove rows with NaN values (many were created during the melt)
    df_long = df_long[df_long['value'].notna()]

    # recode ownership levels
    ownership_old = list(range(1, 3+1))
    ownership_new = ["Public", "Private nonprofit", "Private for-profit"]
    df_long['ownership'] = df_long['ownership'].replace(ownership_old, ownership_new)

    # recode region levels
    region_old = list(range(0, 9+1))
    region_new = [
        'U.S. Service Schools',
        'New England',
        'Mid East',
        'Great Lakes',
        'Plains',
        'Southeast',
        'Southwest',
        'Rocky Mountains',
        'Far West',
        'Outlying Areas'
    ]
    df_long['region'] = df_long['region'].replace(region_old, region_new)

    # recode NaNs in some cols to 0
    nan_to_zero = [
        'religious_affiliation',
        'flag_historically_black',
        'flag_men_only',
        'flag_women_only'
    ]
    df_long[nan_to_zero] = df_long[nan_to_zero].fillna(0)

    # load religious affiliation xwalk
    religious_affil_dict = {}
    relig_affil_xwalk_path = '/Users/h/Documents/code/college_scorecard_wh/data/xwalks/religious_affil_xwalk.csv'
    with open(relig_affil_xwalk_path, mode='r') as xwalk:
        reader = csv.reader(xwalk)
        religious_affil_dict = {rows[0]:rows[1] for rows in reader}

    # map the religious affil xwalk to the column
    df_long["religious_affiliation"] = df_long["religious_affiliation"].astype(str).str[:-2]
    df_long["religious_affiliation"] = df_long["religious_affiliation"].map(religious_affil_dict)

    # convert flags to bool and ope6_id to int
    df_long = df_long.astype(
        {'flag_historically_black': 'bool',
        'flag_men_only': 'bool',
        'flag_women_only': 'bool',
        'ope6_id': 'int'}
    )

    # cast wide by variable
    index_cols = [
        'ipeds_id',
        'ope6_id',
        'data_year',
        'name',
        'state',
        'region',
        'ownership',
        'religious_affiliation',
        'flag_historically_black',
        'flag_men_only',
        'flag_women_only'
    ]
    df_wide = df_long.pivot(index=index_cols, columns='variable', values='value').reset_index().rename_axis(None, axis=1)
    return(df_wide)
