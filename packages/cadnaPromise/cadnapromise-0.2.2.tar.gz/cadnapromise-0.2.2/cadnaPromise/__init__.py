from .promise import Promise 
import os
import warnings

__version__ = '0.2.2'

curr_loc = os.path.dirname(os.path.realpath(__file__))


cachePath = "/cache"
__compiler__ = 'g++'

if os.path.exists(curr_loc + cachePath):
    if os.path.isfile(curr_loc + cachePath + '/.CXX.txt'):
        with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
            __compiler__ = file.read()

