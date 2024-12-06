import unittest
import json
from mantas_j_mod1_atsiskaitymas.data_parser import DataParser


class TestDataParser(unittest.TestCase):
    def test_validate_format_invalid_value(self):
        parser = DataParser()
        with self.assertRaises(ValueError):
            parser._DataParser__validate_format('invalid_format')

    def test_validate_format_valid_value(self):
        try:
            parser = DataParser()
            parser._DataParser__validate_format('json')
            parser._DataParser__validate_format('csv')
            parser._DataParser__validate_format('list')
        except ValueError:
            self.fail('An exception was raised.')

    def test_return_in_format_list(self):
        data = [{"id": 1, "title": 'Test'}]
        result = DataParser().return_in_format(data, 'list')

        self.assertEqual(data, result)

    def test_return_in_format_json(self):
        data = [{"id": 1, "title": 'Test'}]
        result = DataParser().return_in_format(data, 'json')

        self.assertEqual(json.dumps(data), result)

    def test_return_in_format_csv(self):
        data = [{"id": 1, "title": 'Test'}]
        result = DataParser().return_in_format(data, 'csv')

        self.assertEqual('id,title\n1,Test\n', result)
