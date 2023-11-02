
class Configuration:
    """ The class stores global application configuration """

    def __init__(self, args):
        self.__serial_port = args.serial
        self.__baudrate = args.baudrate
        self.__sensor = args.sensor
        self.__log = args.log
        self.__log_level = args.log_level
        self.__output_file = args.output_file

    @property
    def serial_port(self):
        return self.__serial_port

    @property
    def baudrate(self):
        return self.__baudrate

    @property
    def sensor(self):
        return self.__sensor

    @property
    def log(self):
        return self.__log

    @property
    def log_level(self):
        return self.__log_level

    @property
    def output_file(self):
        return self.__output_file
