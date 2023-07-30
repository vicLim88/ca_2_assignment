import logging

from typing import List
from propertyUtils.config_parser import read_ini_configuration_from_resource
from pymongo import MongoClient


class DatabaseMongo:
    def __init__(self, environment_name: str):
        self.collection = None
        self.db = None
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(funcName)s : %(message)s',
            level=logging.INFO
        )

        self.config_parse_ini = read_ini_configuration_from_resource()
        self.config_parse_ini.get_config_ini_file("database")
        self.client = MongoClient(self.config_parse_ini.get_value_from_section_key(
            section_name=f"MONGO_{environment_name.upper()}",
            key="conn_string"
        ))
        logging.info(msg="DatabaseMongo has been instantiated.")

    # CREATE
    def create_data_base(self, name_of_database: str) -> None:
        self.db = self.client[name_of_database]
        logging.info(msg=f"Database {name_of_database} has been created.")

    def create_single_document(self, name_of_database: str, name_of_collection: str, entry: dict) -> None:
        self.db = self.client[name_of_database]
        self.collection = self.db[name_of_collection]
        self.collection.insert_one(entry)

    def create_multiple_documents(self, name_of_database: str, name_of_collection: str, entries: dict) -> None:
        self.db = self.client[name_of_database]
        self.collection = self.db[name_of_collection]
        self.collection.insert_many(entries)

    # READ
    def read_list_of_available_databases(self) -> List[str]:
        logging.info(msg="Retrieved list of collections : {self.client.list_database_names()}")
        return self.client.list_database_names()

    def read_database_name_is_present(self, name_of_database: str) -> bool:
        return name_of_database in self.client.list_database_names()

    def read_all_documents_from_collection(self, database_name: str, collection_name: str):
        return [document for document in self.client[database_name][collection_name].find()]

    # UPDATE
    # DELETE
