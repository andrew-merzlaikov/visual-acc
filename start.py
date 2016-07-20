# coding: utf-8
import argparse
from datas.actions import VisualisationAction, CalibrationAction

parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store', dest='type_program',
                    help='Calibration | PyGame | Test')

parser.add_argument('--version', action='version', version='%(prog)s 1.2')

results = parser.parse_args()
print 'type_program =', results.type_program

if results.type_program == "PyGame":
    action = VisualisationAction()
    action.run()


if results.type_program == "Calibration":
    action = CalibrationAction()
    action.run()


# try:
#     if results.type_program == "Calibration":
#         read_port = ReadComPort(type_file=ReadComPort.CALIBRATION_FILE)
#         obj = ProxyCalibrationData(read_port)
#     elif results.type_program == "Test":
#         read_port = TestReadComPort()
#     else:
#         read_port = ReadComPort()
# except SerialException:
#     print "Please connect USB ARDUINO"
# else:
#     if results.type_program == "PyGame":
#         obj = RenderPyGame(read_port)
#     if results.type_program == "Test":
#         read_port.get_array_for_test()
#     else:
#         try:
#             obj.run()
#         except Exception as error:
#             print error
#         finally:
#             read_port.close()
