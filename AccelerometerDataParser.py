import codecs
import logging

from AccelerometerData import AccelerometerData


class AccelerometerDataParser:
    """
    The class delivers parsing functionality of a bytes to accelerometer data.

    The expected input to of data to be correctly pared is following:

    b'accel; 0;081405;0;-260377;-9;-903318;0;001331;0;-02130;0;000000;'

    where:
        b'accel;' is marker that these are accelerometer data. The marker is always start of a set of data.

        b'0;' is integer acceleration in X axis.
        b'081405;0;' is fractional acceleration in X axis.
        b'0;' is integer acceleration in Y axis.
        b'-260377;' is fractional acceleration in Y axis.
        b'-9;' is integer acceleration in Z axis.
        b'-903318;' is fractional acceleration in Z axis.
        b'0;' is integer angular velocity for X axis.
        b'001331;' is fractional angular velocity for X axis.
        b'0;' is integer angular velocity for Y axis.
        b'-02130;' is fractional angular velocity for Y axis.
        b'0;' is integer angular velocity for Z axis.
        b'000000;' is fractional angular velocity for Y axis.

    Fractional part is represented as: value * (10)^(6). To get floating point representation use following formula:
    val_int + val_frac * 10^(-6)

    Examples:
        0.25:  val_int =  0, val_frac =  250000
        -0.25: val_int =  0, val_frac = -250000
        -1.0:  val_int = -1, val_frac =  0
        -1.25: val_int = -1, val_frac = -250000
    """

    @staticmethod
    def parse_data(data, log=False):
        """
        Parse data and store them in AccelerometerData.

        :param data: Data to be parsed
        :type data: bytes
        :param log: Enable additional logging
        :type log: bool

        :return: None: if data were not possible to be parsed
        :return: AccelerometerData: if data were correctly parsed
        """
        data_int = []
        # Split data accelerator[x,y,z], gyroscope[x,y,z] into separate values
        # Last expected element is 'LF'
        split_data = data.split(b';')
        # If the received data don't start with b`accel` stop parsing and return None.
        # The provided data were incorrect.
        if split_data[0] != b'accel':
            return None

        for x in split_data[1:]:
            if x != b'\r\n':
                data_int.append(int(codecs.decode(x)))

        # Convert data from separate values into floats.
        # It is expected that data are split into integer and fractional part, where
        # fractional part is represented as integer that has to be multiplied by -10^6.
        # So the actual value is sum: int_part + frac_part * (-10^6)
        data_out = [data_int[0] + data_int[1] * 0.000001, data_int[2] + data_int[3] * 0.000001,
                    data_int[4] + data_int[5] * 0.000001, data_int[6] + data_int[7] * 0.000001,
                    data_int[8] + data_int[9] * 0.000001, data_int[10] + data_int[11] * 0.000001]

        if log:
            logging.debug("acc[x,y,x]=[{0}, {1}, {2}]; gyr[x,y,z]= [{3}, {4}, {5}]".format(
                data_out[0], data_out[1], data_out[2], data_out[3], data_out[4], data_out[5]))

        return AccelerometerData(data_out)