# coding: utf-8
import argparse
from serial import SerialException

from utils.calibration import ProxyCalibrationData
from utils.reading_serial import ReadComPort
from visual.render import RenderPyGame


parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store', dest='type_program',
                    help='Calibration | PyGame ')

# parser.add_argument('-t', action='store_true', default=False,
#                     dest='boolean_switch',
#                     help='Set a switch to true')
# parser.add_argument('-f', action='store_false', default=False,
#                     dest='boolean_switch',
#                     help='Set a switch to false')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()
print 'type_program     =', results.type_program

try:
    if results.type_program == "Calibration":
        read_port = ReadComPort(type_file=ReadComPort.CALIBRATION_FILE)
        obj = ProxyCalibrationData(read_port)
    else:
        read_port = ReadComPort()
except SerialException:
    print "Please connect USB ARDUINO"
else:
    if results.type_program == "PyGame":
        obj = RenderPyGame(read_port)

    try:
        obj.run()
    except Exception as error:
        print error
    finally:
        read_port.close()
