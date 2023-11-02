import serial.tools.list_ports
from serial import Serial, LF

serial_reading = True


class SerialCommunication:
    """
    The class is responsible for communication with a DK over serial port
    """

    def __init__(self, serial_port, baudrate):
        """
        Serial port communication class constructor.

        :param serial_port: Name of serial port to connect to. In case of Linux/Unix it is a path to file representing
        the port e.g. /dev/ttyACM1.
        :type serial_port: str
        :param baudrate: Desired communication baud rate.
        :type baudrate: int
        """
        self.__serial_port = Serial(port=serial_port, baudrate=baudrate)

    def read_data(self, size=1):
        """
        Read data from serial port.

        :param size: number of bytes to read. By default, it is set to 1.
        :type size: int
        :return Data read from serial port
        :rtype bytes
        """
        return self.__serial_port.read(size)

    def read_data_until(self, expected_byte=LF, size=None):
        """
        Read data from serial port until expected_byte is found in received data or
        requested size of data was read.

        :param expected_byte: Byte value to stop reading when received
        :type expected_byte: bytes
        :param size: Number of bytes to read
        :type size: int
        :return: Data read from serial port
        """
        return self.__serial_port.read_until(expected_byte, size)

    @classmethod
    def print_serial_ports_list(cls):
        """
        This is a support method that provides a mean to list all available serial ports.
        The list is printed in a terminal used to run the application.
        """
        usb_ports = serial.tools.list_ports.comports()

        if len(usb_ports) == 0:
            print("There are no serial ports available in the system.")
        else:
            print("There are {0} serial ports available:".format(len(usb_ports)))
            for port, desc, hwid in usb_ports:
                print("\t# Port: {0}: {1} [{2}]".format(port, desc, hwid))
