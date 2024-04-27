from abc import ABC
from typing import Union


class Parser(ABC):
    def start_parse(self, filepath: str = None) -> None:
        data = self._parse_data(filepath)
        self._write_to_db(data)

    def _write_to_db(self, data: any) -> None:
        pass

    def _parse_data(self, filepath: str = None) -> Union[list[tuple], None]:
        pass
