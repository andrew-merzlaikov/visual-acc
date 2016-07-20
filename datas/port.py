# coding: utf-8
from serial.serialutil import SerialException
from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import settings

from datas.validators import (
    BaseValidator, ArduinoValidatorDataFromString,
    ArduinoValidatorDataFromByte
)
from datas.mutation import (
    BaseDecoder, BaseEncoder, ArduinoDecoderStringData
)


class BaseSerialPort(object):
    u""" Базовый класс для работы с интерфейсом RS-232 """

    # Список валидаторов
    validators = []

    # Шифровщик сообщения и расшифровщик сообщения
    encoder = BaseEncoder
    decoder = BaseDecoder

    def __del__(self):
        u""" Деструктор который закрывает порт RS-232 """
        self.close()

    def __init__(self):
        u""" Констркутор класа для работы с серийным интерфейсом """
        try:
            self.com_port = Serial(
                settings.PORT,
                settings.BAUDRATE,
                bytesize=EIGHTBITS,
                parity=PARITY_NONE,
                stopbits=STOPBITS_ONE
            )
        except SerialException:
            raise SerialException(
                "Пожалуйсто подключите к порту "
                "{port} USB кабель с Arduino".format(port=settings.PORT)
            )

        for validator in self.validators:
            assert issubclass(validator, BaseValidator), (
                "Валидатор {validator} должен быть наследником от "
                "datas.validators.BaseValidator".format(validator=validator)
            )

        assert issubclass(self.decoder, BaseDecoder), (
            "Расшифровщик {decode} должен быть наследником от "
            "datas.mutation.BaseDecoder".format(decode=self.decoder)
        )
        assert issubclass(self.encoder, BaseEncoder), (
            "Зашифровщик {encoder} должен быть наследником от "
            "datas.mutation.BaseEncoder".format(encoder=self.encoder)
        )

    def send_data(self, msg):
        u""" Отправка данных """
        raise NotImplementedError

    def read_data(self):
        u""" Чтение данных """
        raise NotImplementedError

    def read(self):
        u""" Запуск чтения данных """
        data = self.read_data()
        for validator in self.validators:
            validator.check_read_data(data)
        return self.decoder.decode(data)

    def send(self, message):
        u""" Запуск отправки данных """
        data = self.send_data(message)
        for validator in self.validators:
            validator.check_send_data(data)
        return self.encoder.encode(data)

    def close(self):
        u""" Закрываем порт """
        self.com_port.close()


class ArduinoSerialPortString(BaseSerialPort):
    u""" Интерфейс для чтения строковых данных с Arduino"""
    validators = [ArduinoValidatorDataFromString]

    decoder = ArduinoDecoderStringData

    def read_data(self):
        return self.com_port.read_until()
