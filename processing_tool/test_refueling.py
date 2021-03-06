import os
import numpy as np
from refueling import Average, Fresh, Swap

# @property
def file_loading():
    # print(os.path.split(os.getcwd()))
    with open("test.PDC") as f:
        content = f.readlines()
    return content

def test_Average(data=None):
    if data is None:
        data = file_loading()
    array, nd = Average(pdc=data).average_burnup()
    assert array.shape == (6,4)

def test_Fresh(data=None):
    if data is None:
        data = file_loading()
    array, nd = Fresh("1,2", pdc=data).refueling()
    assert array.shape == (6,4)

def test_Swap(data=None):
    if data is None:
        data = file_loading()
    array, nd = Swap("1,2", pdc=data).swap()
    assert array.shape == (6,4)