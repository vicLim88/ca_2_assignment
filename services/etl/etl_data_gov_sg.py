import os
import numpy as np
import pandas as pd

from typing import List, Dict
from requests import session
from requests_html import HTMLSession
from abc import ABC

from propertyUtils.database import DatabaseMongo
from services.etl.etl_Main import etl_Main
from propertyUtils.config_parser import read_ini_configuration_from_resource


class etl_data_gov_sg(etl_Main, ABC):

    def __init__(self, environment_name: str = "DEV"):
        self.dict_dbName_colls = None
        self.list_of_dataset_folders = None
        self.curr_dir: str = os.getcwd()
        self.list_of_resource_ids = None
        self.dataset_collections_url = None
        self.mongo_db_dev = DatabaseMongo(environment_name=environment_name)
        self.environment_name = environment_name
        self._setup_from_ini_configuration()

    # PUBLIC METHOD
    def extract(self, source: str = "INTERNET"):
        if source.upper() == "DATASET":
            self.dict_dbName_colls = self._fetch_list_of_dataset_folders()

        else:
            # Extract list of resource_ids from data.gov.sg
            self.list_of_resource_ids: List[str] = self._scrap_links_for_resource_ids()

            # Save the list of resource_ids for record keeping
            self._ini_configuration_update()

    def load(self) -> None:
        # extract a list of records
        if self.dict_dbName_colls is not None:
            for dbName, colls in self.dict_dbName_colls.items():
                for coll in colls:
                    if ".csv" in coll:
                        csv_file_path = f"{self.curr_dir}/resources/datasets/{dbName}/{coll}"
                        entries = pd.read_csv(csv_file_path).dropna().to_dict('records')
                        print(entries)
                        self._write_to_mongodb(
                            database_name=dbName,
                            collection_name=coll,
                            entries=entries
                        )
            return

        if (self.list_of_resource_ids is not None) and (len(self.list_of_resource_ids) > 0):
            for resource_id in self.list_of_resource_ids:
                name, record = self._extract_record(resource_id)
                self._write_to_mongodb(
                    database_name="COVID-19_Weekly_status",
                    collection_name=name,
                    entries=record
                )
            return

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

    def _write_to_mongodb(self, database_name: str, collection_name: str, entries) -> None:
        self.mongo_db_dev.create_multiple_documents(
            name_of_database=database_name,
            name_of_collection=collection_name.replace(" ", "_").replace(" / ", "_"),
            entries=entries
        )
        return

    def _write_to_mongodb_from_datasets(self) -> None:
        for collection_name in self.list_of_dataset_folders:
            document_name = f"{self.curr_dir}/"
            print(collection_name)
        # self.mongo_db_dev.create_multiple_documents(
        #     name_of_database="COVID-19_Weekly_Stats",
        #     name_of_collection=collection_name.replace(" ", "_").replace(" / ", "_"),
        #     entries=response_json
        # )

    def _extract_record(self, resource_id: str):
        response = HTMLSession().get(self.base_url)
        key: str = response.html.xpath(f".//a[contains(@href, '{resource_id}')]")[0].text
        value = session.Sess().set(

        ).get(
            url=f"https://data.gov.sg/api/action/datastore_search?resource_id={resource_id}"
        ).json()['result']['records']
        return key, value

    def _scrap_links_for_resource_ids(self) -> List[str]:
        response = HTMLSession().get(self.base_url)
        list_of_ids = [link.split("?")[1].split("&")[0].split("=")[1] for link in response.html.absolute_links if
                       "?resource_id=" in link]
        assert len(list_of_ids) > 0, "Unable to retrieve list of ids"
        list_of_ids_uniq = np.unique(list_of_ids, axis=0).tolist()
        return list_of_ids_uniq

    def _fetch_list_of_dataset_folders(self):
        base_path = f"{self.curr_dir}/resources/datasets"
        dict_of_db_colls = {}
        for roots in os.walk(base_path):
            if (roots is not None) and (roots[0] != base_path):
                db_name = roots[0].split('\\')[-1]
                collections = roots[2]
                dict_of_db_colls[db_name] = collections
        return dict_of_db_colls
