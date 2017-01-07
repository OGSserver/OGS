# encoding:utf-8
"""
Common classes and functions for geoprocessing package.
"""
from data import datatypes


class _Parameter(object):
    """
    Class to contain parameters and their options.
    Do not call directly.
    """

    name = None
    value = None
    type = None


class Integer(_Parameter):
    """
    Class to hold integer parameters
    """

    def __init__(self, name, value):
        self.name = name
        self.type = int
        self.value = self.type(value)


class Float(_Parameter):
    """
    Class to hold float parameters
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value


class String(_Parameter):
    """
    Class to hold string parameters
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value


class List(_Parameter):
    """
    Class to hold list parameters
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Raster(_Parameter):
    """
    Class to hold raster parameters
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.type = datatypes.Raster


class Features(_Parameter):
    """
    Class to hold features parameters
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.type = datatypes.Features


if __name__ == '__main__':
    num = Float(10)
    print(num.value)

