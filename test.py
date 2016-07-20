from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import settings
# from getc
#
# START = b'r'
# PACKAGE_LEN = 36
#
# com_port = Serial(
#     settings.PORT,
#     settings.BAUDRATE,
# )
#
# print("connected to: " + com_port.portstr)
#
# count = 0
#
# com_port.write(bytes(" "))
#
# while True:
#     key = ord(getch())
#     if key == 27:  # ESC
#         break
#     elif key == 32:  # Space
#         com_port.write(bytes(" "))
#
#     print com_port.read_until()
#
# com_port.close()
