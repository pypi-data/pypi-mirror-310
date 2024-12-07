import json
import io
import csv


class DataParser:
    accepted_formats = {'json', 'csv', 'list'}
    data_to_parse = None

    def __validate_format(self, return_format):
        if return_format not in self.accepted_formats:
            raise ValueError(
                f"Invalid return_format: '{return_format}'. Accepted formats are: {self.accepted_formats}")

    def return_in_format(self, data: list, return_format: str = 'json'):
        self.__validate_format(return_format)
        self.data_to_parse = data

        match return_format:
            case 'json':
                return self.__return_json_format()
            case 'csv':
                return self.__return_csv_format()
            case 'list':
                return self.data_to_parse

    def __return_json_format(self):
        return json.dumps(self.data_to_parse)

    def __return_csv_format(self):
        output = io.StringIO()
        headers = self.data_to_parse[0].keys()

        writer = csv.DictWriter(
            output, fieldnames=headers, lineterminator="\n")

        writer.writeheader()
        writer.writerows(self.data_to_parse)

        csv_data = output.getvalue()
        output.close()

        return csv_data
