# coding: utf-8
import argparse
from serial import SerialException

from utils.calibration import ProxyCalibrationData
from utils.reading_serial import ReadComPort, TestReadComPort
from interfaces.render import RenderPyGame


parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store', dest='type_program',
                    help='Calibration | PyGame | Test')

# parser.add_argument('-t', action='store_true', default=False,
#                     dest='boolean_switch',
#                     help='Set a switch to true')
# parser.add_argument('-f', action='store_false', default=False,
#                     dest='boolean_switch',
#                     help='Set a switch to false')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()
print 'type_program =', results.type_program

try:
    if results.type_program == "Calibration":
        read_port = ReadComPort(type_file=ReadComPort.CALIBRATION_FILE)
        obj = ProxyCalibrationData(read_port)
    elif results.type_program == "Test":
        read_port = TestReadComPort()
    else:
        read_port = ReadComPort()
except SerialException:
    print "Please connect USB ARDUINO"
else:
    if results.type_program == "PyGame":
        obj = RenderPyGame(read_port)
    if results.type_program == "Test":
        read_port.get_array_for_test()
    else:
        try:
            obj.run()
        except Exception as error:
            print error
        finally:
            read_port.close()
