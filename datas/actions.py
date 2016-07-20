# coding: utf-8
import pygame
from pygame.locals import *

from datas.data import VisualisationData, CalibrationData
from datas.interfaces import RenderPyGame
from datas.port import ArduinoSerialPortString
import settings
from utils.importer import ImporterCSV


class ActionException(Exception):
    u""" Ошибка при работе с запуском """
    pass


class BaseAction(object):
    u""" Базовый клас для работы с активной частью приложения """

    def run(self):
        u""" Метод запуска работы приложения """
        raise NotImplementedError


class VisualisationAction(BaseAction):
    u""" Визуализация каждого измерения """

    def __init__(self):
        u""" Инициализируем рабочую область """

        self.data = VisualisationData()
        self.serial_port = ArduinoSerialPortString()
        self.interface = RenderPyGame()
        self.importer = ImporterCSV(
            file_name=self.__class__.__name__,
            field_names=self.data.name_attributes
        )

    def run(self):
        u""" Запуск визуального представления объекта """
        self.interface.pre_run()
        while True:
            event = pygame.event.poll()

            if event.type == QUIT:
                break
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                break

            try:
                self.data.set_received_data(self.serial_port.read())
                self.data.mutation_data()
                self.importer.save_data_to_csv(self.data.get_dict_data())
            except Exception as error:
                print error
            else:
                self.interface.figure.draw(
                    self.data, self.interface.rotate_around_y_mode
                )

            pygame.display.flip()
        self.importer.close()
        self.serial_port.close()


class CalibrationAction(BaseAction):
    u""" Калибровка измерений """

    def __init__(self):
        u""" Инициализируем рабочую область """

        self.data = CalibrationData()
        self.serial_port = ArduinoSerialPortString()
        self.interface = RenderPyGame()
        self.importer = ImporterCSV(
            file_name=self.__class__.__name__,
            field_names=self.data.name_attributes
        )
        self.count_space = 0

    def run(self):
        u""" Запуск калибровки """
        self.interface.pre_run()

        while True:
            event = pygame.event.poll()
            if event.type == QUIT:
                break
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                break

            if event.type == KEYDOWN and event.key == K_SPACE:
                # Создаем демностративный текст о нажатие пробела
                self.count_space += 1
                text = "{star} {count_space} {star}".format(
                    star="*" * 20, count_space=self.count_space
                )

                # Запускаем итерации количество которых указанно в настройках
                # далее находим среднее арефметическое и обновляем матрицу
                # калибровки
                # Итерация считается успешно выполненной если она прошла
                # валидацию
                iteration = 0
                while iteration <= settings.COUNT_ITERATION:
                    try:
                        self.data.run_iteration(self.serial_port.read())
                    except Exception as error:
                        print error
                    else:
                        iteration += 1
                        osd_status = "{iteration}/{count_iteration}".format(
                            iteration=iteration,
                            count_iteration=settings.COUNT_ITERATION
                        )
                        # Отрисовываем созданный текст и положение
                        # текущие фигуры
                        self.interface.figure.draw(
                            self.data, self.interface.rotate_around_y_mode,
                            text=text, osd_status=osd_status
                        )
                try:
                    self.data.math_mean_and_append_matrix()
                    self.data.mutation_data()
                    self.importer.save_data_to_csv(self.data.get_dict_data())
                except Exception as error:
                    print error
                else:
                    self.interface.figure.draw(
                        self.data, self.interface.rotate_around_y_mode,
                        text=text
                    )

            pygame.display.flip()
        self.importer.close()
        self.serial_port.close()
