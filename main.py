from propertyUtils.database import DatabaseMongo
import pandas as pd
import requests
import json

from services.etl.etl_data_gov_sg import etl_data_gov_sg


def service_dao_mongodb(name):
    mongo_db_dev = DatabaseMongo(environment_name="dev")
    pd.set_option('display.expand_frame_repr', False)
    pd_data = pd.DataFrame(
        mongo_db_dev.read_all_documents_from_collection(
            database_name="PORTFOLIO",
            collection_name="posts"
        )
    )


def service_ingestion(web_url: str):
    session = requests.session()
    response = session.get(
        url=web_url
    )
    response_json = response.json()

    # Pass the response_json to mongoDB
    mongo_db_dev = DatabaseMongo(environment_name="dev")
    pd.set_option('display.expand_frame_repr', False)

    mongo_db_dev.create_multiple_documents(
        name_of_database="COVID-19_Weekly_Stats",
        name_of_collection="Vaccination_status_by_age_group",
        entries=response_json
    )


# def extract_from_


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pd.read_csv()
    # service_dao_mongodb('PyCharm')
    # service_ingestion(
    #     "https://data.gov.sg/api/action/datastore_search?resource_id=68289dd4-e9d1-41cf-afe6-b093d04b60af"
    # )

    etl = etl_data_gov_sg().extract()