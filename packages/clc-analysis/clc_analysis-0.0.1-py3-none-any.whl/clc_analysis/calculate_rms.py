import numpy as np
import math


def calculate_rms(buffer): return math.sqrt(np.mean(np.square(buffer)))