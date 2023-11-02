class AccelerometerData:
    ACC_X_IDX = 0
    ACC_Y_IDX = 1
    ACC_Z_IDX = 2
    GYR_X_IDX = 3
    GYR_Y_IDX = 4
    GYR_Z_IDX = 5

    def __init__(self, data):
        """
        Constructor of the class expects to get an list of a data with 6 float elements:
        [acc_x,acc_y,acc_z, gyr_x, gyr_y, gyr_z], where acc stands for acceleration
        gyr stands for gyroscope.

        :param data: List of 6 float values
        :type data: list
        """
        assert (len(data) == 6)
        self.__data = data

    def __iter__(self):
        """
        The method is responsible for iterator initialization.
        Part of interface required for iterator functionality.
        :return: Iterator object
        """
        # use negative value to skip initial condition in __next__. In such case first call to __next__ returns
        # first element
        self.__iter_idx = -1

        return self

    def __next__(self):
        """
        The method moves iterator to point to next item and returns that item.
        Part of interface for iterator functionality.
        :return: Element of the data iterated over. That could be one of acceleration values: [x,y,z] or one of
        angular velocity values: [x,y,z].
        """
        self.__iter_idx += 1

        if self.__iter_idx < len(self.__data):
            return self.__data[self.__iter_idx]
        else:
            raise StopIteration

    # TODO add further calculations to data if required
    # TODO add getters and setters of data
