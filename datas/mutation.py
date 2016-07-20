# coding: utf-8


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
        import settings

        return data.decode().strip().split(
            settings.ARDUINO_PACKAGE_STRING_SEPARATOR
        )
