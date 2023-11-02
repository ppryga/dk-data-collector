import argparse
import csv
import logging

from pynput.keyboard import Listener, Key

from AccelerometerDataParser import AccelerometerDataParser
from Config import Configuration
from Communication import SerialCommunication

data_collect = True
app_configuration = None


def on_press(key):
    if key == Key.esc:
        global data_collect
        data_collect = False


def configure_logging(log_level):
    level = logging.WARNING
    match log_level:
        case "debug":
            level = logging.DEBUG
        case "info":
            level = logging.INFO
        case "waning":
            level = logging.WARNING
        case "error":
            level = logging.ERROR
        case "critical":
            level = logging.CRITICAL
        case _:
            print("Unknown logging level, going to use default: {0}".format(level))

    logging.basicConfig(level=level)


def collect_data(configuration):
    """Collect data from  a DK over a communication channel. Data to be collected are selected by a user.
       Selected sensor to collect data are provided by configuration.

       :param configuration: Global application configuration with variety of items depending on e.g. communication
       channel selected or type of sensor to collect data for.
       :type configuration: Configuration
    """

    # Add possibility to stop data collection from keyboard by pressing ESC button
    listener = Listener(on_press=on_press)
    listener.start()

    # use write to store data e.g. in CSV format
    writer = None

    if configuration.output_file:
        output_file = open(configuration.output_file, 'a')
        writer = csv.writer(output_file)

    target_comm = SerialCommunication(configuration.serial_port, configuration.baudrate)

    logging.info("Starting data collection from: {0}".format(configuration))

    acceleration_data = []
    try:
        while data_collect:
            data = target_comm.read_data_until()

            # TODO add storage of raw data is enabled by configuration
            logging.debug("Received data: {0}".format(data))

            parsed_data = AccelerometerDataParser.parse_data(data, configuration.log)
            if parsed_data:
                acceleration_data.append(parsed_data)

                if writer:
                    writer.writerow(parsed_data)

        logging.info("Ending data collection")

        listener.join()

    except KeyboardInterrupt:
        logging.warning("End data collection due to exception")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--list_ports", action="store_true", help="Print list all available serial ports")
    args_parser.add_argument("--log-level", choices=["debug", "info", "waning", "error", "critical"], default="warning")

    args_subparsers = args_parser.add_subparsers()

    data_collection_parser = args_subparsers.add_parser("data-collection", help="Start sensor data collection")
    data_collection_parser.add_argument("-s", "--serial", required=True, metavar="SERIAL_PORT",
                                        help="Serial port to connect. For Linux users it is /dev/ttyACMn where `n` is "
                                             "the port number. For Windows users it is COMn, where `n` is the port"
                                             " number.")
    data_collection_parser.add_argument("-b", "--baudrate", required=True, help="Serial communication baudrate")
    data_collection_parser.add_argument("-f", "--sensor", choices=["all", "accelerometer"], default="all",
                                        help="Selects sensor to collect data. By efault it is set to `all` to collect"
                                             " all sensors data")
    data_collection_parser.add_argument("-o", "--output_file", metavar="PATH",
                                        help="Path to the output file. If the file doesn't exist it will be created."
                                             " Data are appended to end of file.")
    data_collection_parser.add_argument("-v", "--verbose", action="store_true",
                                        help="Enable verbose output according to selected verbosity level")

    args = args_parser.parse_args()

    if args.list_ports:
        SerialCommunication.print_serial_ports_list()
    else:
        global app_configuration
        app_configuration = Configuration(args)

        configure_logging(app_configuration.log_level)

        print("Data acquisition for sensor {0} started over serial port: {1} [{2} BAUD]", app_configuration.sensor,
              app_configuration.serial_port, app_configuration.baudrate)

        # Here we progress with data acquisition
        collect_data(app_configuration)

        print("End of data acquisition")
