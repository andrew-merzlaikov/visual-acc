from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import settings

START = b'r'
PACKAGE_LEN = 36

com_port = Serial(
    settings.PORT,
    settings.BAUDRATE,
)

print("connected to: " + com_port.portstr)

count = 0

com_port.write(bytes(" "))
while True:
    com_port.write(bytes(0x04))
    for line in com_port.read():
        print str(line)

com_port.close()
