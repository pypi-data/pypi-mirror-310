from mantas_j_mod1_atsiskaitymas.data_parser import DataParser
from mantas_j_mod1_atsiskaitymas.crawler import Crawl


def crawl(source: str = 'eurovaistine', timeout: int = 60, return_format: str = 'json'):
    data = Crawl(source, timeout).get_web_data()
    parsed_data = DataParser().return_in_format(data, return_format)
    return parsed_data
