-- create institution dimension table
CREATE TABLE scorecard.dim_inst(
        ipeds_id integer primary key,
        ope6_id integer,
        data_year varchar,
        name varchar,
        state varchar,
        region varchar,
        ownership varchar,
        religious_affiliation varchar,
        flag_historically_black boolean,
        flag_men_only boolean,
        flag_women_only boolean
);

-- create fact table
CREATE TABLE scorecard.fct_inst(
        ipeds_id integer primary key,
        data_year varchar,
        admissions_admission_rate_overall numeric,
        cost_tuition_out_of_state numeric,
        cost_tuition_in_state numeric,
        pct_ethnicity_aian numeric,
        pct_ethnicity_asian numeric,
        pct_ethnicity_black numeric,
        pct_ethnicity_hispanic numeric,
        pct_ethnicity_nhpi numeric,
        pct_ethnicity_non_resident_alien numeric,
        pct_ethnicity_two_or_more numeric,
        pct_ethnicity_unknown numeric,
        pct_ethnicity_white numeric, 
        pct_firstgeneration numeric,
        student_demographics_avg_family_income numeric,
        student_size numeric
);
