import csv
from datetime import datetime
import math
from sys import stdout

import numpy
from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import settings


class ReadComPort(object):

    RESULT_FILE = "result"
    CALIBRATION_FILE = "calibration"

    def __init__(self, type_file=None):
        self.com_port = Serial(
            settings.PORT,
            settings.BAUDRATE,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE
        )

        self.type_file = type_file
        if not type_file:
            self.type_file = ReadComPort.RESULT_FILE

        self.path_file = self.__get_file_path(self.type_file)
        self.file_csv = open(self.path_file, 'wb')

        field_names = SensorData.data
        self.data_sensor = SensorData()
        if self.type_file == ReadComPort.CALIBRATION_FILE:
            field_names = CalibrationSensorData.calibration_data
            self.calibration_sensor_data = CalibrationSensorData()

        self.writer = csv.DictWriter(
            self.file_csv, fieldnames=field_names, delimiter=';'
        )
        self.writer.writeheader()

    def _read_data(self):
        package = self.com_port.read_until()
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
        if len(package) != 9:
            return False
        for data in package:
            if not data or float(data) == 0.0:
                return False
        return True

    def get_array_for_test(self):
        for i in range(0, 1000):
            package = self.read_arduino_data()
            print(i)
            tt = SensorData()
            tt.set_received_data(package)

    @staticmethod
    def __get_file_path(type_file):
        key_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path_file = (
            settings.RESULT_DIR + "{type_file}{key}.csv".format(
                type_file=type_file, key=key_file_name
            )
        )
        return path_file

    def save_data_to_csv(self, count_space=0):
        self.data_sensor.set_received_data(self.read_arduino_data(), count_space)
        if self.type_file == ReadComPort.CALIBRATION_FILE:
            self.writer.writerow(self.data_sensor.get_dict_calibration_data())
        else:
            self.writer.writerow(self.data_sensor.get_dict_data())
        return self.data_sensor

    def calibration(self):
        for iteration in range(1, 1000):
            self.calibration_sensor_data.get_iteration_data(
                self.read_arduino_data()
            )
            stdout.write("\r%d/1000" % iteration)
            stdout.flush()
        stdout.write("\r           \r")
        return self.calibration_sensor_data

    def close(self):
        self.com_port.close()
        self.file_csv.close()


class TestReadComPort(ReadComPort):

    START = 's'
    PACKAGE_LEN = 36

    def _read_data(self):
        self.com_port.reset_output_buffer()
        self.com_port.write(TestReadComPort.START)
        self.com_port.reset_input_buffer()
        package = self.com_port.read(TestReadComPort.PACKAGE_LEN)
        return package

    def read_arduino_data(self, level=0):
        if level > 100:
            return list()
        data = self._read_data()
        if self.validate_package(data):
            return data
        return self.read_arduino_data(level + 1)

    def get_array_for_test(self):
        for i in range(0, 1000):
            package = self.read_arduino_data()
            print(i)
            tt = SensorData()
            tt.set_received_data(package)

    @staticmethod
    def validate_package(package):
        if len(package) != 36:
            return False
        return True

    @staticmethod
    def parse_package(package):
        if len(package) != 36:
            return False
        return True


class SensorData(object):

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
        "altitude_value_z",
        "altitude_value",
        "time_stamp",
        "count_space",
    ]

    xl_x_value = 0
    xl_y_value = 0
    xl_z_value = 0

    gyro_x_value = 0
    gyro_y_value = 0
    gyro_z_value = 0

    altitude_value = 0

    time_stamp = 0
    time_delta = 0
    altitude_value_z = 0
    altitude_value_z_dot = 0
    count_space = 0

    SCALE_USEC = 0.1 ** 6
    ACC_GRAVITY = 0.97
    SCALE_ACC = 0.1 ** 6

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
        self.time_delta = 0
        self.altitude_value_z = 0
        self.altitude_value_z_dot = 0
        self.count_space = 0

        self.i = 0

    def set_received_data(self, package, count_space=0):

        result = package
        # ay = numpy.arctan2(
        #     float(result[0]), math.sqrt(
        #         math.pow(float(result[1]), 2) + math.pow(float(result[2]), 2)
        #     )
        # ) * 180 / math.pi
        #
        # ax = numpy.arctan2(
        #     float(result[1]), math.sqrt(
        #         math.pow(float(result[0]), 2) + math.pow(float(result[2]), 2)
        #     )
        # ) * 180 / math.pi
        #
        # az = numpy.arctan2(
        #     float(result[2]), math.sqrt(
        #         math.pow(float(result[0]) , 2) + math.pow(float(result[1]), 2)
        #     )
        # ) * 180 / math.pi

        self.time_delta = SensorData.SCALE_USEC * float(result[8])

        self.altitude_value_z += (
            self.altitude_value_z_dot * self.time_delta +
            0.25 * (self.xl_z_value + SensorData.SCALE_ACC * float(result[2])) *
            self.time_delta ** 2
        )
        self.altitude_value_z_dot += (
            0.5 * (self.xl_z_value + SensorData.SCALE_ACC * float(result[2])) *
            self.time_delta
        )

        self.xl_x_value = SensorData.SCALE_ACC * float(result[0])
        self.xl_y_value = SensorData.SCALE_ACC * float(result[1])
        self.xl_z_value = (
            SensorData.SCALE_ACC * float(result[2]) - SensorData.ACC_GRAVITY
        )
        self.gyro_x_value = SensorData.SCALE_ACC * float(result[3])
        self.gyro_y_value = SensorData.SCALE_ACC * float(result[4])
        self.gyro_z_value = SensorData.SCALE_ACC * float(result[5])
        self.altitude_value = float(result[6])
        self.time_stamp = int(result[7])
        self.count_space = count_space

    def get_dict_data(self):
        result = {}
        for key in self.data:
            if hasattr(self, key):
                result[key] = getattr(self, key)
        return result


class CalibrationSensorData(SensorData):
    matrix_calibration = list()

    calibration_data = [
        "xl_x_value",
        "xl_y_value",
        "xl_z_value",
    ]

    def __init__(self):
        self.mean_dict = {
            "xl_x_value": 0,
            "xl_y_value": 0,
            "xl_z_value": 0,
        }
        self.iteration = 0
        self.matrix_calibration = list()
        super(CalibrationSensorData, self).__init__()

    def get_iteration_data(self, packages):
        self.mean_dict = {
            "xl_x_value": 0,
            "xl_y_value": 0,
            "xl_z_value": 0,
        }
        self.iteration = 0
        self.set_received_data(packages)
        for key in self.calibration_data:
            self.mean_dict[key] += getattr(self, key)
            self.iteration += 1

    def run_mean_and_push(self):
        for key in self.calibration_data:
            self.mean_dict[key] /= self.iteration
        self.matrix_calibration.append(
            [
                self.mean_dict["xl_x_value"],
                self.mean_dict["xl_y_value"],
                self.mean_dict["xl_z_value"]
            ]
        )

    def get_dict_calibration_data(self):
        return self.mean_dict


class ProxySensorData(object):
    def __init__(self, read_port):
        self.read_port = read_port

    def run(self, count_space=0):
        return self.read_port.save_data_to_csv(count_space)


class FakeSensorData(SensorData):

    def set_received_data(self):
        self.xl_x_value = 0
        self.xl_y_value = 0
        self.xl_z_value = 0

