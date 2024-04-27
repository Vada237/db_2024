from app.parser.sample_parser import SampleParser


class ParserManager:
    sample_parser = SampleParser()

    @staticmethod
    def start(filepathes: list[str] = None) -> None:
        ParserManager.sample_parser.start_parse()
