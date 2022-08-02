from dotenv import load_dotenv
import requests
import os

def extract_scorecard(years):
    """Pull data from scorecard API and store in JSONL"""

    # load API key from environment
    load_dotenv()
    API_KEY=os.getenv("API_KEY")

    # init list to hold output
    l_years = []

    # top level url with API key
    url=f'https://api.data.gov/ed/collegescorecard/v1/schools?api_key={API_KEY}'

    # list of query field parameters
    field_params = ['&school.operating=1', '&school.main_campus=1']

    for p_year in years:

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
            p_year + '.student.size,',
            p_year + '.cost.tuition.in_state,',
            p_year + '.cost.tuition.out_of_state,',
            p_year + '.admissions.admission_rate.overall,',
            # student dems and characteristics (year input required)
            p_year + '.student.demographics.race_ethnicity.white,',
            p_year + '.student.demographics.race_ethnicity.black,',
            p_year + '.student.demographics.race_ethnicity.hispanic,',
            p_year + '.student.demographics.race_ethnicity.asian,',
            p_year + '.student.demographics.race_ethnicity.aian,',
            p_year + '.student.demographics.race_ethnicity.nhpi,',
            p_year + '.student.demographics.race_ethnicity.two_or_more,',
            p_year + '.student.demographics.race_ethnicity.non_resident_alien,',
            p_year + '.student.demographics.race_ethnicity.unknown,',
            p_year + '.student.demographics.race_ethnicity.white_non_hispanic,',
            p_year + '.student.demographics.race_ethnicity.black_non_hispanic,',
            p_year + '.student.demographics.race_ethnicity.asian_pacific_islander,',
            p_year + '.student.share_firstgeneration,',
            p_year + '.student.demographics.avg_family_income'
            ]

        # complete query url with params
        query_url = url + ''.join(field_params) + '&fields=' + ''.join(opt_params)

        # query data, iterating through pages until there are no more query results
        while new_results:
            scorecard_api = requests.get(query_url + f'&page={page}').json()
            new_results = scorecard_api.get("results", [])
            for i in range(0, len(new_results)):
                new_results[i]['data_year'] = p_year
            inst_data.extend(new_results)
            page += 1
            print(p_year + ' Loading page: ' + f'{page}')

        # add to the list
        l_years.append(inst_data)

    # flatten top level list and return output
    output = [item for sublist in l_years for item in sublist]
    return(output)
