import pathlib
from typing import Union

from app.parser.description_parser import DescriptionParser
from app.parser.rank_parser import RankParser
from app.parser.sample_parser import SampleParser
from app.parser.taxonomy_parser import TaxonomyParser
from settings import taxonomy_path, description_path


class ParserManager:
    sample_parser = SampleParser()
    taxonomy_parser = TaxonomyParser()
    rank_parser = RankParser()
    description_parser = DescriptionParser()

    @staticmethod
    def start() -> None:
        ParserManager.sample_parser.start_parse()
        ParserManager.taxonomy_parser.start_parse()
        ParserManager.__parse_from_files(ParserManager.rank_parser, f'{taxonomy_path}/silva')
        ParserManager.__parse_from_files(ParserManager.description_parser, description_path)

    @staticmethod
    def __parse_from_files(parser: Union[SampleParser, TaxonomyParser, RankParser, DescriptionParser], filepath: str):
        for filename in pathlib.Path(filepath).glob('*.csv'):
            parser.start_parse(filename)
