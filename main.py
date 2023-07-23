from propertyUtils.database import DatabaseMongo
import pandas as pd
import requests
import json


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
    response_json = response.json()["pageProps"]["allChartData"][0]["rows"]

    # Pass the response_json to mongoDB
    mongo_db_dev = DatabaseMongo(environment_name="dev")
    pd.set_option('display.expand_frame_repr', False)

    mongo_db_dev.create_multiple_documents(
        name_of_database="COVID-19_Weekly_Stats",
        name_of_collection="Vaccination_status_by_age_group",
        entries=response_json
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # service_dao_mongodb('PyCharm')
    service_ingestion(
        "https://beta.data.gov.sg/_next/data/luMl8Y-cFHGEd333gPNMi/datasets/522/resources/d_5f9b504acdd7ebc298a974117b490435/view.json?datasetId=522&resourceId=d_5f9b504acdd7ebc298a974117b490435"
    )
