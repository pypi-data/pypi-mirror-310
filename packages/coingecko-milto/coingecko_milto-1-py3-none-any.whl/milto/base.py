import logging
import pandas as pd
from abc import abstractmethod
from typing import Dict


logging.basicConfig(
    format="'%(asctime)s - %(levelname)s - %(message)s'",
    level=logging.INFO
)


class LoggerMixin:
    def __init__(self):
        self.logger = logging.getLogger()


class BaseETL(LoggerMixin):
    def execute(self):
        extracted_tables = self.extract()
        transformed_tables = self.transform(**extracted_tables)
        self.load(**transformed_tables)

    @abstractmethod
    def extract(self) -> Dict[str, pd.DataFrame]:
        pass

    @abstractmethod
    def transform(self, **kwargs: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        pass

    @abstractmethod
    def load(self, **kwargs: pd.DataFrame) -> None:
        pass
