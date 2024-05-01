from typing import Union

from settings import ROW_COUNT


class HtmlHelper:
    @staticmethod
    def get_button_flags(count_rows: int, page: int) -> dict:
        return {
            'backward': True if page > 0 else False,
            'forward': True if (page + 1) * ROW_COUNT < count_rows else False
        }

    @staticmethod
    def numbers_to_float(number: str) -> Union[int, float, None]:
        return None if number == '' or number == 'None' else float(number)

    @staticmethod
    def str_null_to_none(string: str) -> Union[str, None]:
        if string == 'None':
            return None
