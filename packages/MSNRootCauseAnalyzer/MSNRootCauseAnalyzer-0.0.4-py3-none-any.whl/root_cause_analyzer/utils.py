import inspect
import math
import numpy as np
import scipy.stats as stats
from enum import Enum

class MathOperations(Enum):
    ADDITION = "+"
    MULTIPLICATION = "*"
    DIVISION = "/"

def get_enum_member(enum_class, value):
    for member in enum_class:
        if member.value == value:
            return member
    return None

def safe_div(a, b):
    if a == 0 and b == 0:
        return 0
    if b == 0:
        return 1
    return a / b


def get_pvalue( mean1, mean2, std1, std2, n1, n2):
    """z-test"""
    se = np.sqrt((std1/np.sqrt(n1))**2 + (std2/np.sqrt(n2))**2)
    z = (mean1 - mean2) / se
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return p


def get_current_line():
    return inspect.currentframe().f_back.f_lineno


def get_current_function():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    caller_name = caller_frame.f_code.co_name
    return caller_name

