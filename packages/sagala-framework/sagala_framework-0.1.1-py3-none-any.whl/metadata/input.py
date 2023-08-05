import sys
sys.path.append("..")
from connection import postgresql


def data_source (source_data, source_data_link, pic_data, pic_data_engineer, db_location, project_in_charge,
                 description_data, db_schema_table_name, is_airflow_exist, airflow_location, airflow_dag_name) :
    engine = postgresql.connect_metadata_airflow_k8s()
    # create list for insert
    data = (source_data, source_data_link, pic_data, pic_data_engineer, db_location, project_in_charge,
                 description_data, db_schema_table_name, is_airflow_exist, airflow_location, airflow_dag_name)

    query = '''INSERT INTO public.adm_source_loc_project
            (source_data, source_data_link, pic_data, pic_data_engineer, db_location, project_in_charge, description_data, db_schema_table_name, is_airflow_exist, airflow_location, airflow_dag_name)
            VALUES {}; '''.format(data)
    engine.execute(query)
    engine.dispose()


# sample
data_source('google_sheet',	'https://docs.google.com/spreadsheets/d/1T-M81ROqHWk29ifVzYTh0qN8CNeXR_B2H1elZsnmxM0/',
            'kim',	'riska',	'bi_server3',	'dashboard_public_pikobar',	'data harian penambahan antigen',
            'bigdata.diskes.covid19_penambahan_harian_antigen',	'true',	'airflow_rancher',
            'dag_data_antigen')