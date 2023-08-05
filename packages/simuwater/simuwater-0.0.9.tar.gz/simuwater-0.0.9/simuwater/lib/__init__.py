# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 10:47:59 2021

@author: mumuz
"""

import ctypes
import os
import platform

LIB_PATH = os.path.abspath(os.path.dirname(__file__))

if platform.architecture()[0] == '32bit':
    LIB_PATH += '\\x86'
else:
    LIB_PATH += '\\x64'
ctypes.cdll.LoadLibrary(LIB_PATH + '\\sqlite3.dll')
SIMUWATER = ctypes.cdll.LoadLibrary(LIB_PATH + '\\simuwater.dll')
OUTPUT = ctypes.cdll.LoadLibrary(LIB_PATH + '\\simuwater_output.dll')