# PowermeterSample_v3.py

import os
import sys

from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32, byref, create_string_buffer,c_bool, c_char_p, c_int,c_int16, c_double, sizeof, c_voidp, c_short
from TLPM import TLPM
import time


# -*- coding: utf-8 -*-
"""
Uses the Thorlabs TLPM_64.dll in order to communicate with the power meters
"""

from ctypes import *
from enum import Enum


# If you're using Python 3.7 or older change add_dll_directory to chdir
if sys.version_info < (3, 8):
    os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
else:
    os.add_dll_directory(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")

lib = cdll.LoadLibrary(r"TLPM_64.dll")



tlPM = TLPM()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("devices found: " + str(deviceCount.value))

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print(c_char_p(resourceName.raw).value)
    break

tlPM.close()

tlPM = TLPM()
#resourceName = create_string_buffer(b"COM1::115200")
#print(c_char_p(resourceName.raw).value)
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message)
print(c_char_p(message.raw).value)

time.sleep(2)

print("")

wavelength1 = c_double(632)
tlPM.setWavelength(wavelength1)

Attibute1 = c_short()
wavelength2 =  c_double()

tlPM.getWavelength(Attibute1, byref(wavelength2))

print(Attibute1.value)
print(wavelength2.value)
print("")

time.sleep(2)


power_measurements = []
times = []
count = 0
while count < 10:
    power =  c_double()
    tlPM.measPower(byref(power))
    power_measurements.append(power.value)
    times.append(datetime.now())
    print(power.value)
    count+=1
    time.sleep(1)

tlPM.close()
print('End program')

