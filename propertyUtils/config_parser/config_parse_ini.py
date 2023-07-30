import configparser
import os.path

from os import getcwd
from typing import List


class read_ini_configuration_from_resource:
    def __init__(self):
        self.config: configparser = configparser.ConfigParser()

    def get_config_ini_file(self, ini_file_name: str):
        self.full_file_path: str = f"{getcwd()}/resources/config/{ini_file_name}.ini"
        assert os.path.isfile(self.full_file_path), f"{self.full_file_path} does not exist."
        self.config.read(self.full_file_path)

    def get_list_of_sections(self) -> List[str]:
        list_of_keys = [k for (k, v) in self.config.items()]
        return list_of_keys

    def get_value_from_section_key(self, section_name: str, key: str) -> str:
        return self.config.get(section_name, key)

    def set_config_ini_file_with_details(self, section_name: str, key: str, value: str) -> None:
        self.config.set(section_name, key,value)
        with open(file=self.full_file_path, mode="w") as f:
            self.config.write(f)
