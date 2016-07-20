# coding: utf-8


class ValidationException(Exception):
    u""" Ошибки возникающие при валидации данных """
    pass


class BaseValidator(object):
    u""" Базовый клас валидатора """
    @classmethod
    def check_read_data(cls, data):
        u""" Проверка входных данных """
        raise NotImplementedError

    @classmethod
    def check_send_data(cls, data):
        u""" Проверка входных данных """
        raise NotImplementedError


class ArduinoValidatorDataFromString(BaseValidator):
    u""" Вылидатор для проверки данных переданных строчкой """

    @classmethod
    def check_read_data(cls, data):
        import settings

        try:
            list_data = data.decode().strip().split(
                settings.ARDUINO_PACKAGE_STRING_SEPARATOR
            )
        except Exception as error:
            raise ValidationException(
                "Сообщение не может быть разобранно"
                " в список: {error}".format(error=error)
            )

        if len(list_data) != settings.ARDUINO_COUNT_SEND_ELEMENT:
            raise ValidationException(
                "Количество значений не равно"
                " {count_element}".format(
                    count_element=settings.ARDUINO_COUNT_SEND_ELEMENT
                )
            )
        for data in list_data:
            if not data or float(data) == 0.0:
                raise ValidationException(
                    "Пакет с данными имеет в себе пустое"
                    " или пропущенное значение"
                )

    @classmethod
    def check_send_data(cls, data):
        pass


class ArduinoValidatorDataFromByte(BaseValidator):
    u""" Вылидатор для проверки данных переданных в виде байт """

    @classmethod
    def check_read_data(cls, data):
        pass

    @classmethod
    def check_send_data(cls, data):
        pass
