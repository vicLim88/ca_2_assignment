import numpy as np

from typing import List
from requests import session
from requests_html import HTMLSession
from abc import ABC

from propertyUtils.database import DatabaseMongo
from services.etl.etl_Main import etl_Main
from propertyUtils.config_parser import read_ini_configuration_from_resource


class etl_data_gov_sg(etl_Main, ABC):

    def __init__(self, environment_name: str = "DEV"):
        self.list_of_resource_ids = None
        self.dataset_collections_url = None
        self.mongo_db_dev = DatabaseMongo(environment_name=environment_name)
        self.environment_name = environment_name
        self._setup_from_ini_configuration()

    # PUBLIC METHOD
    def extract(self):
        # Extract list of resource_ids from data.gov.sg
        self.list_of_resource_ids: List[str] = self._scrap_links_for_resource_ids()

        # Save the list of resource_ids for record keeping
        self._ini_configuration_update()

    def load(self):
        # extract a list of records
        for resource_id in self.list_of_resource_ids:
            name, record = self._extract_record(resource_id)
            self._write_to_mongodb(name, record)

    # PRIVATE METHOD
    def _setup_from_ini_configuration(self):
        self.config_parse_ini = read_ini_configuration_from_resource()
        self.config_parse_ini.get_config_ini_file("database")  # Todo : set this to 'url.ini'
        self.base_url = self.config_parse_ini.get_value_from_section_key(
            section_name=f"MONGO_{self.environment_name.upper()}",
            key="dataset_url_covid19_stats"
        )

    def _ini_configuration_update(self):
        self.config_parse_ini.set_config_ini_file_with_details(
            section_name="MONGO_DEV",
            key="dataset_url_covid19_stats_resource_ids",
            value=", ".join(self.list_of_resource_ids)
        )

    def _write_to_mongodb(self, collection_name: str, response_json):
        self.mongo_db_dev.create_multiple_documents(
            name_of_database="COVID-19_Weekly_Stats",
            name_of_collection=collection_name.replace(" ", "_").replace(" / ", "_"),
            entries=response_json
        )

    def _extract_record(self, resource_id: str):
        response = HTMLSession().get(self.base_url)
        key: str = response.html.xpath(f".//a[contains(@href, '{resource_id}')]")[0].text
        value = session().get(
            url=f"https://data.gov.sg/api/action/datastore_search?resource_id={resource_id}"
        ).json()['result']['records']
        return key, value

    def _scrap_links_for_resource_ids(self) -> List[str]:
        response = HTMLSession().get(self.base_url)
        list_of_ids = [link.split("?")[1].split("&")[0].split("=")[1] for link in response.html.absolute_links if
                       "?resource_id=" in link]
        list_of_ids_uniq = np.unique(list_of_ids, axis=0).tolist()
        return list_of_ids_uniq
