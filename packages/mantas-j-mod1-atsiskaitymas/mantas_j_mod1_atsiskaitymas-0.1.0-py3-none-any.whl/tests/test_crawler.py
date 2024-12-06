import unittest
from unittest.mock import MagicMock, patch

from mantas_j_mod1_atsiskaitymas.crawler import Crawl


class TestDataParser(unittest.TestCase):
    def test_validate_source_invalid_value(self):
        with self.assertRaises(ValueError):
            Crawl('invalid_source')

    def test_validate_source_valid_value(self):
        try:
            Crawl('eurovaistine')
            Crawl('apotheka')
        except ValueError:
            self.fail('An exception was raised.')

    @patch('mantas_j_mod1_atsiskaitymas.crawler.webdriver.Chrome')
    def test_get_web_data_as_text(self, mock_chrome):
        mock_driver = MagicMock()
        mock_driver.page_source = "<html><head><title>Test</title></head></html>"
        mock_chrome.return_value = mock_driver

        instance = Crawl('eurovaistine')
        result = instance._Crawl__get_web_data_as_text(
            "https://example.com", 10)

        self.assertEqual(result.xpath("//title/text()")[0], "Test")

        mock_driver.get.assert_called_once_with("https://example.com")

    @patch('mantas_j_mod1_atsiskaitymas.crawler.webdriver.Chrome')
    def test_get_web_data_eurovaistine(self, mock_webdriver):
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = """
        <html>
            <a class="productCard">
                <div class="title"><span>Test</span></div>
                <div class="image"><img src="image_url_a.jpg"/></div>
                <div class="discountContainer"><div class="discount">10</div></div>
                <div class="productPrice"><span>10,99 €</span></div>
            </a>
        </html>
        """
        crawler = Crawl('eurovaistine')
        data = crawler.get_web_data()

        # Expected parsed data
        expected_data = [{
            'title': 'Test',
            'img_url': 'image_url_a.jpg',
            'discounted': True,
            'price': 10.99
        }]
        self.assertEqual(data, expected_data)

    @patch('mantas_j_mod1_atsiskaitymas.crawler.webdriver.Chrome')
    def test_get_web_data_apotheka(self, mock_webdriver):
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = """
        <html>
            <div class="box-product">
                <div class="box-product__title">Testing</div>
                <div class="box-product__image"><img src="image_url.jpg"/></div>
                <div class="special"><div class="product-pricing__price-number">10</div></div>
                <span class="product-pricing__price-number">10,99 €</span>
            </div>
        </html>
        """
        crawler = Crawl('apotheka')
        data = crawler.get_web_data()

        expected_data = [{
            'title': 'Testing',
            'img_url': 'image_url.jpg',
            'discounted': True,
            'price': 10.99
        }]
        self.assertEqual(data, expected_data)
