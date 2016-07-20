# coding: utf-8
import settings


class BaseEncoder(object):
    u""" Базовый клас зашифровки данных """

    @classmethod
    def encode(cls, data):
        u""" Метод зашифровки должен возращать результат зашифровки """
        raise NotImplementedError


class BaseDecoder(object):
    u""" Базовый клас расшифрования данных """

    @classmethod
    def decode(cls, data):
        u""" Метод расшифровки должен возращать результат расшифровки """
        raise NotImplementedError


class ArduinoDecoderStringData(BaseDecoder):
    u""" Расшивровщик данных полученных ввиде строки """
    @classmethod
    def decode(cls, data):
        package = data.decode().strip().split(
            settings.ARDUINO_PACKAGE_STRING_SEPARATOR
        )
        return [float(value) for value in package]


class BaseMathMutation(object):
    u""" Базовый класс для преобразования данных """

    @classmethod
    def mutation(cls, data):
        u""" Метод математического преобразования """
        raise NotImplementedError


class MutationScaleData(BaseMathMutation):
    u""" Преобразуем данные используя коэфициент """
    name_attributes = [
        "xl_x_value",
        "xl_y_value",
        "xl_z_value",
        "gyro_x_value",
        "gyro_y_value",
        "gyro_z_value",
    ]

    @classmethod
    def mutation(cls, data):
        for attr in cls.name_attributes:
            if hasattr(data, attr):
                scale_value = (
                    getattr(data, attr) * settings.ARDUINO_SCALE_ACC_GYRO
                )
                setattr(data, attr, scale_value)


class MutationGravityData(BaseMathMutation):
    u""" Преобразуем данные отнимаю гравитационную постоянную """

    attr = "xl_z_value"

    @classmethod
    def mutation(cls, data):
        if hasattr(data, cls.attr):
            value = (
                getattr(data, cls.attr) * settings.GRAVITY
            )
            setattr(data, cls.attr, value)


class MutationCalibrationData(object):
    u""" Калибровка данных путем работы с матрицей """

    attr_matrix = "matrix_calibration"

    def __init__(self, data):
        self.matrix = data.matrix_calibration

    def math(self):
        pass
