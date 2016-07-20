# coding: utf-8
import pygame
from pygame.locals import *

from datas.data import VisualisationData
from datas.interfaces import RenderPyGame
from datas.port import ArduinoSerialPortString
from utils.importer import ImporterCSV


class ActionException(Exception):
    u""" Ошибка при работе с запуском """
    pass


class BaseAction(object):
    pass


class VisualisationAction(BaseAction):
    def __init__(self):
        self.data = VisualisationData()
        self.serial_port = ArduinoSerialPortString()
        self.interface = RenderPyGame()
        self.importer = ImporterCSV(
            file_name=self.__class__.__name__,
            field_names=self.data.name_attributes
        )
        self.count_space = 0

    def run(self):
        self.interface.pre_run()

        frames = 0
        ticks = pygame.time.get_ticks()

        while True:
            event = pygame.event.poll()

            if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            ):
                break

            if event.type == KEYDOWN and event.key == K_SPACE:
                self.count_space += 1
                print "{star} {count_space} {star}".format(
                    star="*" * 20, count_space=self.count_space
                )

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
            frames += 1

        fps = (frames * 1000) / (pygame.time.get_ticks() - ticks)
        print "fps:  {fps}".format(fps=fps)
        self.importer.close()
        self.serial_port.close()
