import os
from abc import ABC, abstractmethod


class etl_Main(ABC):
    @abstractmethod
    def extract(self):
        pass

    def transform(self):
        pass

    def load(self):
        pass
