import configparser
import os.path

from os import getcwd
from typing import List


class read_ini_configuration_from_resource:
    def __init__(self):
        self.config: configparser = configparser.ConfigParser()

    def set_config_file_ini(self, ini_file_name: str):
        full_file_path: str = f"{getcwd()}/resources/config/{ini_file_name}.ini"
        assert os.path.isfile(full_file_path), f"{full_file_path} does not exist."
        self.config.read(full_file_path)

    def get_list_of_sections(self) -> List[str]:
        list_of_keys = [k for (k, v) in self.config.items()]
        return list_of_keys

    def get_value_from_section_key(self, section_name: str, key: str) -> str:
        return self.config.get(section_name, key)
