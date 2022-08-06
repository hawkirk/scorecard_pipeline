import pandas as pd
import json
import os

def transform_scorecard(file_path):
    """Take JSONL, clean and transform, and spit out a csv."""

    proj_dir=os.getcwd()

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

    religious_affil_dict = {
        "0": "Secular",
        "22": "American Evangelical Lutheran Church",
        "24": "African Methodist Episcopal Zion Church",
        "27": "Assemblies of God Church",
        "28": "Brethren Church",
        "30": "Roman Catholic",
        "33": "Wisconsin Evangelical Lutheran Synod",
        "34": "Christ and Missionary Alliance Church",
        "35": "Christian Reformed Church",
        "36": "Evangelical Congregational Church",
        "37": "Evangelical Covenant Church of America",
        "38": "Evangelical Free Church of America",
        "39": "Evangelical Lutheran Church",
        "40": "International United Pentecostal Church",
        "41": "Free Will Baptist Church",
        "42": "Interdenominational",
        "43": "Mennonite Brethren Church",
        "44": "Moravian Church",
        "45": "North American Baptist",
        "47": "Pentecostal Holiness Church",
        "48": "Christian Churches and Churches of Christ",
        "49": "Reformed Church in America",
        "50": "Episcopal Church, Reformed",
        "51": "African Methodist Episcopal",
        "52": "American Baptist",
        "53": "American Lutheran",
        "54": "Baptist",
        "55": "Christian Methodist Episcopal",
        "57": "Church of God",
        "58": "Church of Brethren",
        "59": "Church of the Nazarene",
        "60": "Cumberland Presbyterian",
        "61": "Christian Church (Disciples of Christ)",
        "64": "Free Methodist",
        "65": "Friends",
        "66": "Presbyterian Church (USA)",
        "67": "Lutheran Church in America",
        "68": "Lutheran Church - Missouri Synod",
        "69": "Mennonite Church",
        "71": "United Methodist",
        "73": "Protestant Episcopal",
        "74": "Churches of Christ",
        "75": "Southern Baptist",
        "76": "United Church of Christ",
        "77": "Protestant, not specified",
        "78": "Multiple Protestant Denomination",
        "79": "Other Protestant",
        "80": "Jewish",
        "81": "Reformed Presbyterian Church",
        "84": "United Brethren Church",
        "87": "Missionary Church Inc",
        "88": "Undenominational",
        "89": "Wesleyan",
        "91": "Greek Orthodox",
        "92": "Russian Orthodox",
        "93": "Unitarian Universalist",
        "94": "Latter Day Saints (Mormon Church)",
        "95": "Seventh Day Adventists",
        "97": "The Presbyterian Church in America",
        "99": "Other (none of the above)",
        "100": "Original Free Will Baptist",
        "101": "Ecumenical Christian",
        "102": "Evangelical Christian",
        "103": "Presbyterian",
        "105": "General Baptist",
        "106": "Muslim",
        "107": "Plymouth Brethren",
    }

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
