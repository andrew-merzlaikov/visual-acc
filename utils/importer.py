# coding: utf-8
import csv
from datetime import datetime
import settings


class ImporterCSV(object):

    def __del__(self):
        self.close()

    def __init__(self, file_name, field_names):
        self.path_file = self.__get_file_path(file_name)
        self.file_csv = open(self.path_file, 'wb')

        self.writer = csv.DictWriter(
            self.file_csv, fieldnames=field_names, delimiter=';'
        )
        self.writer.writeheader()

    @staticmethod
    def __get_file_path(file_name):
        key_file_name = datetime.now().strftime("%m-%d_%H-%M-%S")
        path_file = (
            settings.RESULT_DIR + "{type_file}{key}.csv".format(
                type_file=file_name, key=key_file_name
            )
        )
        return path_file

    def save_data_to_csv(self, dict_data):
        self.writer.writerow(dict_data)

    def close(self):
        self.file_csv.close()
