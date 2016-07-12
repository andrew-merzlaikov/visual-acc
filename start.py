from utils.reading_serial import ReadComPort, ProxyPlotData
from visual.render import RenderPyGame

read_port = ReadComPort()

try:
    # obj = ProxyPlotData(read_port)
    # obj.run()

    obj = RenderPyGame(read_port)
    obj.render()
except Exception as error:
    print error

read_port.close()
