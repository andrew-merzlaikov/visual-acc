import math
import numpy
from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import settings


class ReadComPort(object):

    def __init__(self):
        self.com_port = Serial(
            settings.PORT,
            settings.BAUDRATE,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE
        )

    def _read_data(self):
        self.com_port.read_until()
        package = self.com_port.read_until()
        # print(package)
        return package.decode().strip().split(";")

    def read_arduino_data(self, level=0):
        if level > 100:
            return list()
        try:
            data = self._read_data()
        except UnicodeDecodeError:
            data = list()
        if self.validate_package(data):
            return data
        return self.read_arduino_data(level+1)

    @staticmethod
    def validate_package(package):
        if len(package) != 8:
            return False
        for data in package:
            if not data:
                return False
        return True

    def get_array_for_test(self):
        for i in range(0, 1000):
            package = self.read_arduino_data()
            print(i)
            tt = PlotData()
            tt.set_received_data(package)

    def close(self):
        self.com_port.close()


class PlotData(object):

    association = {
        "xl_x_line": "xl_x_value",
        "xl_y_line": "xl_y_value",
        "xl_z_line": "xl_z_value",
        "gyro_x_line": "gyro_x_value",
        "gyro_y_line": "gyro_y_value",
        "gyro_z_line": "gyro_z_value",
        "altitude_line": "altitude_value",

    }

    data = [
        "xl_x_value",
        "xl_y_value",
        "xl_z_value",
        "gyro_x_value",
        "gyro_y_value",
        "gyro_z_value",
        "altitude_value",
        "time_stamp",
    ]

    xl_x_value = 0
    xl_y_value = 0
    xl_z_value = 0

    gyro_x_value = 0
    gyro_y_value = 0
    gyro_z_value = 0

    altitude_value = 0

    time_stamp = 0

    i = 0

    def __init__(self):
        self.xl_x_value = 0
        self.xl_y_value = 0
        self.xl_z_value = 0

        self.gyro_x_value = 0
        self.gyro_y_value = 0
        self.gyro_z_value = 0

        self.altitude_value = 0

        self.time_stamp = 0

        self.i = 0

    def set_received_data(self, package):

        result = package
        ay = numpy.arctan2(
            float(result[0]), math.sqrt(
                math.pow(float(result[1]), 2) + math.pow(float(result[2]), 2)
            )
        ) * 180 / math.pi

        ax = numpy.arctan2(
            float(result[1]), math.sqrt(
                math.pow(float(result[0]), 2) + math.pow(float(result[2]), 2)
            )
        ) * 180 / math.pi

        az = numpy.arctan2(
            float(result[2]), math.sqrt(
                math.pow(float(result[0]), 2) + math.pow(float(result[1]), 2)
            )
        ) * 180 / math.pi

        data_x = float(result[3])
        data_y = float(result[4])
        data_z = float(0)

        self.xl_x_value = data_x
        self.xl_y_value = data_y
        self.xl_z_value = data_z
        self.gyro_x_value = float(result[3])
        self.gyro_y_value = float(result[4])
        self.gyro_z_value = float(result[5])
        self.altitude_value = float(result[6])
        self.time_stamp = int(result[7])


class ProxyPlotData(object):
    def __init__(self, read_port):
        self.read_port = read_port
        self.validation = PlotData()

    def run(self):

        self.validation.set_received_data(self.read_port.read_arduino_data())
        return self.validation


class FakePlotData(PlotData):

    def set_received_data(self):
        self.xl_x_value = 0
        self.xl_y_value = 0
        self.xl_z_value = 0
