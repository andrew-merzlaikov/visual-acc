from msvcrt import getch


class ProxyCalibrationData(object):
    def __init__(self, read_port):
        self.read_port = read_port
        self.count_space = 0
        self.calibration_data = None

    def run(self):
        print "ESC - exit; Space - next vector; Enter - Start math"
        while True:
            key = ord(getch())
            if key == 27:  # ESC
                break
            elif key == 32:  # Space
                self.count_space += 1
                if self.count_space != 7:
                    print "{star} {count_space} {star}".format(
                        star="*" * 20, count_space=self.count_space
                    )
                    print "Please wait .... "
                    self.calibration_data = self.read_port.calibration()
                    self.calibration_data.run_mean_and_push()
                    self.read_port.writer.writerow(
                        self.calibration_data.get_dict_calibration_data()
                    )
                    print "Ready"
                else:
                    print "{star} Please keydown Enter {star}".format(
                        star="*" * 20
                    )
            elif key == 13:  # Enter
                self._math_for_calbration()

    def _math_for_calbration(self):
        pass
