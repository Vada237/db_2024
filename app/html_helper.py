from settings import ROW_COUNT


class HtmlHelper:
    @staticmethod
    def get_button_flags(count_rows: int, page: int) -> dict:
        return {
            'backward': True if page > 0 else False,
            'forward': True if (page + 1) * ROW_COUNT < count_rows else False
        }
