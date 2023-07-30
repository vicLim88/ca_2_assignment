import numpy as np

from typing import List
from requests import session
from requests_html import HTMLSession
from abc import ABC
from services.etl.etl_Main import etl_Main
from propertyUtils.config_parser import read_ini_configuration_from_resource


class etl_data_gov_sg(etl_Main, ABC):

    def __init__(self, environment_name: str = "DEV"):
        self.list_of_dataset_links = None
        self.dataset_collections_url = None
        self.environment_name = environment_name
        self._setup_from_ini_configuration()

    # PUBLIC METHOD
    def extract(self):
        # self.dataset_collections_url = self._extract_record_from_url()
        self.list_of_dataset_links: List[str] = self._scrap_links_for_resource_ids()

    # PRIVATE METHOD
    def _setup_from_ini_configuration(self):
        self.config_parse_ini = read_ini_configuration_from_resource()
        self.config_parse_ini.set_config_file_ini("database")  # Todo : set this to 'url.ini'
        self.base_url = self.config_parse_ini.get_value_from_section_key(
            section_name=f"MONGO_{self.environment_name.upper()}",
            key="dataset_url_covid19_stats"
        )

    def _extract_record_from_url(self):
        return session().get(
            url="https://data.gov.sg/api/action/datastore_search?resource_id=68289dd4-e9d1-41cf-afe6-b093d04b60af"
        ).json()

    def _scrap_links_for_resource_ids(self) -> List[str]:
        response = HTMLSession().get(self.base_url)
        list_of_ids = [link.split("?")[1].split("&")[0].split("=")[1] for link in response.html.absolute_links if "?resource_id=" in link]
        list_of_ids_uniq = np.unique(list_of_ids, axis = 0).tolist()
        return list_of_ids_uniq
