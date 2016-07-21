# coding: utf-8

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

import settings

# TODO: Нужно переделать архитектуру интерфейсов

class OpenGlObject(object):

    def __init__(self):
        pass

    @staticmethod
    def _draw_text(position, text_string):
        font = pygame.font.SysFont("Courier", 18, True)
        text_surface = font.render(
            text_string, True,
            (255, 255, 255, 255), (0, 0, 0, 255)
        )
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(
            text_surface.get_width(), text_surface.get_height(), GL_RGBA,
            GL_UNSIGNED_BYTE, text_data
        )

    def draw(self, sensor_data, rotate_around_y_mode,
             text=None, osd_status=None):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0.0, -7.0)

        if not text:
            osd_text = "Y: " + str(
                "{0:.2f}".format(sensor_data.xl_y_value)
            ) + ", X: " + str(
                "{0:.2f}".format(sensor_data.xl_x_value)
            )
            if rotate_around_y_mode:
                osd_line = osd_text + ", Z: " + str(
                    "{0:.2f}".format(sensor_data.xl_z_value)
                )
            else:
                osd_line = osd_text
        else:
            osd_line = text

        self._draw_text((-2, -2, 2), osd_line)

        if osd_status:
            self._draw_text((-3, -3, 2), osd_status)
        else:
            self._draw_text((-3, -3, 2), "                       ")

        if rotate_around_y_mode:
            glRotatef(sensor_data.xl_z_value, 0.0, 1.0, 0.0)
        else:
            glRotatef(0.0, 0.0, 1.0, 0.0)
        glRotatef(sensor_data.xl_y_value, 1.0, 0.0, 0.0)
        glRotatef(-1 * sensor_data.xl_x_value, 0.0, 0.0, 1.0)

        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 0.2, -1.0)
        glVertex3f(-1.0, 0.2, -1.0)
        glVertex3f(-1.0, 0.2, 1.0)
        glVertex3f(1.0, 0.2, 1.0)

        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(1.0, -0.2, 1.0)
        glVertex3f(-1.0, -0.2, 1.0)
        glVertex3f(-1.0, -0.2, -1.0)
        glVertex3f(1.0, -0.2, -1.0)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 0.2, 1.0)
        glVertex3f(-1.0, 0.2, 1.0)
        glVertex3f(-1.0, -0.2, 1.0)
        glVertex3f(1.0, -0.2, 1.0)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, -0.2, -1.0)
        glVertex3f(-1.0, -0.2, -1.0)
        glVertex3f(-1.0, 0.2, -1.0)
        glVertex3f(1.0, 0.2, -1.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-1.0, 0.2, 1.0)
        glVertex3f(-1.0, 0.2, -1.0)
        glVertex3f(-1.0, -0.2, -1.0)
        glVertex3f(-1.0, -0.2, 1.0)

        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(1.0, 0.2, -1.0)
        glVertex3f(1.0, 0.2, 1.0)
        glVertex3f(1.0, -0.2, 1.0)
        glVertex3f(1.0, -0.2, -1.0)
        glEnd()


class RenderPyGame(object):

    rotate_around_y_mode = 0
    count_space = 0

    def __init__(self):
        self.rotate_around_y_mode = True
        self.figure = OpenGlObject()
        self.count_space = 0

    def _resize(self, width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def pre_run(self):
        pygame.init()
        video_flags = pygame.OPENGL | pygame.DOUBLEBUF
        screen = pygame.display.set_mode(
            (settings.WIGHT, settings.HEIGHT), video_flags
        )
        pygame.display.set_caption("Press Esc to quit")
        self._resize(settings.WIGHT, settings.HEIGHT)
