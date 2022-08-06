from dotenv import load_dotenv
import requests
import os

def extract_scorecard(year, API_KEY):
    """Pull data from scorecard API and store in JSONL"""

    # top level url with API key
    url=f'https://api.data.gov/ed/collegescorecard/v1/schools?api_key=' + API_KEY

    # list of query field parameters
    field_params = ['&school.operating=1', '&school.main_campus=1']

    # init objects for query run
    inst_data = []
    new_results = True
    page = 0

    # list of option parameters
    # note delimiter comma absence in last list element
    opt_params = [
        # school identifiers (no year associated)
        'id,',
        'ope6_id,',
        'school.name,',
        'school.state,',
        # school attributes (no year associated)
        'school.ownership,',
        'school.region_id,',
        'school.religious_affiliation,',
        'school.minority_serving.historically_black,',
        'school.men_only,',
        'school.women_only,',
        # instution stats (year input required)
        year + '.student.size,',
        year + '.cost.tuition.in_state,',
        year + '.cost.tuition.out_of_state,',
        year + '.admissions.admission_rate.overall,',
        # student dems and characteristics (year input required)
        year + '.student.demographics.race_ethnicity.white,',
        year + '.student.demographics.race_ethnicity.black,',
        year + '.student.demographics.race_ethnicity.hispanic,',
        year + '.student.demographics.race_ethnicity.asian,',
        year + '.student.demographics.race_ethnicity.aian,',
        year + '.student.demographics.race_ethnicity.nhpi,',
        year + '.student.demographics.race_ethnicity.two_or_more,',
        year + '.student.demographics.race_ethnicity.non_resident_alien,',
        year + '.student.demographics.race_ethnicity.unknown,',
        year + '.student.demographics.race_ethnicity.white_non_hispanic,',
        year + '.student.demographics.race_ethnicity.black_non_hispanic,',
        year + '.student.demographics.race_ethnicity.asian_pacific_islander,',
        year + '.student.share_firstgeneration,',
        year + '.student.demographics.avg_family_income'
        ]

    # complete query url with params
    query_url = url + ''.join(field_params) + '&fields=' + ''.join(opt_params)

    print(query_url)

    # query data, iterating through pages until there are no more query results
    while new_results:
        scorecard_api = requests.get(query_url + f'&page={page}').json()
        new_results = scorecard_api.get("results", [])
        for i in range(0, len(new_results)):
            new_results[i]['data_year'] = year
        inst_data.extend(new_results)
        page += 1
        print(year + ' Loading page: ' + f'{page}')
        if page > 1:
            break

    return(inst_data)
