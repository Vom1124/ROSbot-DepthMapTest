import os
import sys
import time
import math
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
# from numpy.random import rand
import math
from tqdm import tqdm
LB=np.array([[0, 1, 2, 2, 2],
     [0, 2, 4, 3, 4],
     [0, 2, 4, 3, 4],
     [0, 10, 46, 46, 57],
     [0, 20, 51, 43, 57]])
RB=np.array([[2, 2, 2, 2, 3],
     [4, 3, 4, 3, 4],
     [4, 2, 4, 3, 4],
     [59, 59, 58, 45, 28],
     [58, 58, 56, 45, 30]])
D=float(40)
CD=(np.sum(np.divide(abs(LB-RB), abs(LB)+abs(RB)))) # Canberra Distance
CD=math.nan
status=math.isnan(CD)
print("","Canberra Distance", type(CD), status)