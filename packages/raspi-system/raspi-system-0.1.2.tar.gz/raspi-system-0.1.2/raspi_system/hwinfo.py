

import subprocess
from collections import namedtuple

HwModelInfo = namedtuple("HwModelInfo", "code ecosystem main variant revision ram note")

_rpi_models = [
    HwModelInfo('0002', 'rpi', 'Pi', 'Model B Rev 1', '', '256MB', ''),
    HwModelInfo('0003', 'rpi', 'Pi', 'Model B Rev 1', '', '256MB', 'ECN0001'),
    HwModelInfo('0004', 'rpi', 'Pi', 'Model B Rev 2', '', '256MB', ''),
    HwModelInfo('0005', 'rpi', 'Pi', 'Model B Rev 2', '', '256MB', ''),
    HwModelInfo('0006', 'rpi', 'Pi', 'Model B Rev 2', '', '256MB', ''),

    HwModelInfo('0007', 'rpi', 'Pi', 'Model A', '', '256MB', ''),
    HwModelInfo('0008', 'rpi', 'Pi', 'Model A', '', '256MB', ''),
    HwModelInfo('0009', 'rpi', 'Pi', 'Model A', '','256MB', ''),

    HwModelInfo('000d', 'rpi', 'Pi', 'Model B Rev 2', '', '512MB', ''),
    HwModelInfo('000e', 'rpi', 'Pi', 'Model B Rev 2', '', '512MB', ''),
    HwModelInfo('000f', 'rpi', 'Pi', 'Model B Rev 2', '', '512MB', ''),

    HwModelInfo('0010', 'rpi', 'Pi', 'Model B+', '', '512MB', ''),
    HwModelInfo('0013', 'rpi', 'Pi', 'Model B+', '', '512MB', ''),
    HwModelInfo('900032', 'rpi', 'Pi', 'Model B+', '', '512MB', ''),

    HwModelInfo('0011', 'rpi', 'CM', 'Compute Module', '', '512MB', ''),
    HwModelInfo('0014', 'rpi', 'CM', 'Compute Module', '', '512MB', 'Embest, China'),

    HwModelInfo('0012', 'rpi', 'Pi', 'Model A+', '', '256MB', ''),
    HwModelInfo('0015', 'rpi', 'Pi', 'Model A+', '', '256MB', 'Embest, China'),
    HwModelInfo('0015', 'rpi', 'Pi', 'Model A+', '', '512MB', 'Embest, China'),

    HwModelInfo('a01041', 'rpi', 'Pi 2', 'Model B', 'v1.1', '1GB', 'Sony, UK'),
    HwModelInfo('a21041', 'rpi', 'Pi 2', 'Model B', 'v1.1', '1GB', 'Embest, China'),
    HwModelInfo('a22042', 'rpi', 'Pi 2', 'Model B', 'v1.2', '1GB', ''),

    HwModelInfo('900092', 'rpi', 'Pi Zero', '', 'v1.2', '512MB', ''),
    HwModelInfo('900093', 'rpi', 'Pi Zero', '', 'v1.3', '512MB', ''),
    HwModelInfo('9000C1', 'rpi', 'Pi Zero', 'W', '', '512MB', ''),

    HwModelInfo('a02082', 'rpi', 'Pi 3', 'Model B', 'v1.2', '1GB', 'Sony, UK'),
    HwModelInfo('a22082', 'rpi', 'Pi 3', 'Model B', 'v1.2', '1GB', 'Embest, China'),
    HwModelInfo('a020d3', 'rpi', 'Pi 3', 'Model B', 'v1.3', '1GB', 'Sony, UK'),

    HwModelInfo('a03111', 'rpi', 'Pi 4', '', 'v1.1', '1GB', 'Sony, UK'),
    HwModelInfo('b03111', 'rpi', 'Pi 4', '', 'v1.1', '2GB', 'Sony, UK'),
    HwModelInfo('b03112', 'rpi', 'Pi 4', '', 'v1.2', '2GB', 'Sony, UK'),
    HwModelInfo('c03111', 'rpi', 'Pi 4', '', 'v1.1', '4GB', 'Sony, UK'),
    HwModelInfo('c03112', 'rpi', 'Pi 4', '', 'v1.2', '4GB', 'Sony, UK'),
    HwModelInfo('c03114', 'rpi', 'Pi 4', '', 'v1.4', '4GB', 'Sony, UK'),
    HwModelInfo('d03114', 'rpi', 'Pi 4', '', 'v1.4', '8GB', 'Sony, UK'),

    HwModelInfo('c03130', 'rpi', 'Pi 400', '', 'v1.1', '4GB', 'Sony, UK'),

    HwModelInfo('a03140', 'rpi', 'CM4', '', 'v1.0', '1GB', 'Sony, UK'),
    HwModelInfo('b03140', 'rpi', 'CM4', '', 'v1.0', '2GB', 'Sony, UK'),
    HwModelInfo('c03140', 'rpi', 'CM4', '', 'v1.0', '4GB', 'Sony, UK'),
    HwModelInfo('d03140', 'rpi', 'CM4', '', 'v1.0', '8GB', 'Sony, UK'),
]

rpi_models = {info.code: info for info in _rpi_models}


def model_string():
    result = subprocess.check_output(['cat', '/proc/device-tree/model'])
    result = result.strip().rstrip('\x00')
    return result


def model_revcode():
    revision = "0000"
    f = open('/proc/cpuinfo', 'r')
    for line in f:
        if line[0:8] == 'Revision':
            length = len(line)
            revision = line[11:length - 1]
    f.close()
    return revision


def model_info():
    return rpi_models[model_revcode()]


def _is(main):
    return rpi_models[model_revcode()].main == main


def is_pi4():
    try:
        return _is('Pi 4')
    except KeyError:
        return True


def is_pi3():
    return _is('Pi 3')


if __name__ == '__main__':
    print("Full Model String   : {0}".format(model_string()))
    print("Model Revision Code : {0}".format(model_revcode()))
    info = model_info()
    print("Model Info  :")
    print("  Ecosystem : {0}".format(info.ecosystem))
    print("  Main      : {0}".format(info.main))
    print("  Variant   : {0}".format(info.variant))
    print("  Revision  : {0}".format(info.revision))
    print("  RAM       : {0}".format(info.ram))
    print("")
    print("Is Pi4 : {}".format(is_pi4()))
    print("Is Pi3 : {}".format(is_pi3()))
