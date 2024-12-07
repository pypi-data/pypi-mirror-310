from lxml.etree import HTML
from selenium import webdriver


class Crawl:
    accepted_sources = {'eurovaistine', 'apotheka'}

    def __init__(self, source, timeout=60):
        self.source = source
        self.timeout = timeout
        self.__validate_source()

    def get_web_data(self):
        match self.source:
            case 'eurovaistine':
                response_data = self.__get_web_data_as_text(
                    'https://www.eurovaistine.lt/vaistai-nereceptiniai',
                    self.timeout
                )
                return self.__parse_eurovaistine_data(response_data)
            case 'apotheka':
                response_data = self.__get_web_data_as_text(
                    'https://www.apotheka.lt/prekes/nereceptiniai-vaistai',
                    self.timeout
                )
                return self.__parse_apotheka_data(response_data)

    def __validate_source(self):
        if self.source not in self.accepted_sources:
            raise ValueError(
                f"Invalid source: '{self.source}'. Accepted sources are: {self.accepted_sources}")

    def __get_web_data_as_text(self, url: str, response_timeout: int) -> HTML:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(response_timeout)
        html_content = driver.page_source
        return HTML(html_content)

    def __parse_eurovaistine_data(self, data: HTML) -> list[dict[str, bool]]:
        drugs_cards = data.xpath("//a[contains(@class, 'productCard')]")
        return [self.__process_eurovaistine_xpath(drug) for drug in drugs_cards]

    def __parse_apotheka_data(self, data: HTML) -> list[dict[str, bool]]:
        drugs_cards = data.xpath("//div[@class='box-product']")
        return [self.__process_apotheka_xpath(drug) for drug in drugs_cards]

    def __process_eurovaistine_xpath(self, data):
        image_url = None
        if len(data.xpath(".//div[contains(@class, 'image')]//img/@src")):
            image_url = data.xpath(".//div[contains(@class, 'image')]//img/@src")[0]

        price = ''.join(data.xpath(".//div[contains(@class, 'productPrice')]/span/text()")).strip()[:-2]
        formatted_price = float(price.replace(',', '.'))

        return {
            'title': ''.join(data.xpath(".//div[@class='title']/span/text()")).strip(),
            'img_url': image_url,
            'discounted': bool(
                data.xpath(".//div[contains(@class, 'discountContainer')]//div[contains(@class, 'discount')]/text()")
            ),
            'price': formatted_price
        }

    def __process_apotheka_xpath(self, data):
        image_url = None
        if len(data.xpath(".//div[contains(@class, 'box-product__image')]//img/@src")):
            image_url = data.xpath(".//div[contains(@class, 'box-product__image')]//img/@src")[0]

        price = ''.join(data.xpath(".//span[@class='product-pricing__price-number']/text()")).strip()[:-2]
        formatted_price = float(price.replace(',', '.'))

        return {
            'title': ''.join(data.xpath(".//div[@class='box-product__title']/text()")).strip(),
            'img_url': image_url,
            'discounted': bool(
                data.xpath(".//div[contains(@class, 'special')]//div[contains(@class, 'product-pricing__price-number')]/text()")
            ),
            'price': formatted_price
        }
