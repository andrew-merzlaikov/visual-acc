# coding: utf-8
from datas.mutation import MutationScaleData, MutationGravityData


class DataException(Exception):
    u""" Ошибка при работе с данными """
    pass


class BaseData(object):
    u""" Базовый клас для работы с данными """

    # список атрибутов в которых будет храниться данные
    name_attributes = []
    # список математических преобразований
    math_mutation = []

    def __init__(self):
        u""" Конструктор создающий арибуты данных"""
        for attr in self.name_attributes:
            setattr(self, attr, 0)

    def set_received_data(self, package):
        u""" Заполняем данные из полеченного пакета """
        number_package = 0
        for attr in self.name_attributes:
            try:
                setattr(self, attr, package[number_package])
            except Exception as error:
                raise DataException(
                    "Не могу заполнить данные из"
                    " полученного пакета {error}".format(error=error)
                )

    def mutation_data(self):
        u""" Выполняем матемтические преобразования """
        for math in self.math_mutation:
            math.mutation(self)

    def get_dict_data(self):
        u""" Генерируем словарик с данными """
        result = {}
        for key in self.name_attributes:
            if hasattr(self, key):
                result[key] = getattr(self, key)
        return result


class VisualisationData(BaseData):
    u""" Набор данных для визуализации """
    name_attributes = [
        "xl_x_value",
        "xl_y_value",
        "xl_z_value",
        "gyro_x_value",
        "gyro_y_value",
        "gyro_z_value",
        "altitude_value",
        "time_stamp",
    ]
    math_mutation = [MutationScaleData, MutationGravityData]


class CalibrationData(BaseData):
    u""" Набор данных для калибровки """
    name_attributes = [
        "xl_x_value",
        "xl_y_value",
        "xl_z_value",
    ]

    math_mutation = [MutationScaleData, MutationGravityData]

    u"""
    матрица калибровки размерности 6х3
    matrix_calibration = [
        [xl_x_value, xl_y_value, xl_z_value]
        ....
    ]
    """
    matrix_calibration = list()

    def __init__(self):
        u""" Конструктор для работы калибровки """

        # mean - временный вектор который необходим для усреднения
        self.mean = dict()
        for key in self.name_attributes:
            self.mean[key] = 0

        # iteration - количество итераций для поиска среднего значения
        self.iteration = 0

        super(CalibrationData, self).__init__()

    def math_mean_and_append_matrix(self):
        u""" Вычесляем среднее и добавляем в матрицу калибровки"""
        for key in self.name_attributes:
            self.mean[key] /= self.iteration

        self.matrix_calibration.append(
            [value for key, value in self.mean.items()]
        )
