"""" Class arduino deals with the communication with the arduino,
both sending and receiving values.
Also, the LEDs have a check whether the right colors are being displayed.
"""

import serial
from serial.tools.list_ports import comports


class Arduino:

    def __init__(self):
        port = self.get_port()
        if port is None:
            exit()
        self.arduino = serial.Serial(port, baudrate=115200)
        self.red = 0
        self.yellow = 0
        self.green = 0
        self.pot_x = 0
        self.pot_y = 0

    def handle_input(self):
        rec = self.arduino.readline()  # read the arduino serial communication
        if rec.decode()[0] == 'x':
            self.pot_x = int(rec[1:])
        elif rec.decode()[0] == 'y':
            self.pot_y = int(rec[1:])
        elif rec.decode()[0] == 'l':
            if rec[1] != self.red or rec[2] != self.yellow or rec[3] != self.green:  # check whether the LEDs are the right color
                self.set_led(self.red, self.yellow, self.green)  # if not, set the LEDs to the right color
        return self.pot_x, self.pot_y

    def set_led(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.arduino.write(bytes("{}{}{}".format(red, yellow, green), 'ascii'))  # communicate LEDs to arduino

    def get_port(self):
        """ Helper function to find and select the port to which your
        arduino is connected.
        """
        ports = comports()
        if len(ports) > 1:
            for index, port in enumerate(ports):
                print("{}: {}".format(index, port.device))
            nr = input("Which device to use? [0-{}] ".format(len(ports) - 1))
            return ports[int(nr)].device
        elif len(ports) == 1:
            print("One device found:")
            print("{}".format(ports[0].device))
            return ports[0].device
        else:
            print("No devices found.")
            return None
