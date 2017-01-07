# encoding:utf-8
"""
Sample script to run a virtual_gp task
"""
from geoprocessing import common


def run_demo(number):
    number.value *= 10
    return [common.Integer('result_number', number.value)]


CONFIG_INFO = {
    'main_function': run_demo,
    'inputs': [common.Integer],
    'outputs': [common.Integer]
}


