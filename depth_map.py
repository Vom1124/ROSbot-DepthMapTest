import os
import sys
import time

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
# from numpy.random import rand
import math
from tqdm import tqdm

# Block-Matching algorithm
def myBM_Algo(iml, imr, w, h, BS, NP):
    # Accepts the left and right image as input to perform stereo correspondence.
    # 'h' is the height, 'w' is the width, 'BS' is the block size, and 'NP' is the disparity range.
    DM = np.zeros([h,w]) # Initializing disparity map
    LB = np.empty([BS, BS]) # Initializing left block
    RB = np.empty([BS, BS]) # Initializing right block
    
    Cost = np.empty([NP,1]) #Initializing cost function array to the disparity range
    WS = int((BS-1)/2) # Initializing the window size
    
    for y in tqdm(range(WS,h-WS)):
        for x in range(WS,w-(WS+NP)):
            LB = imr[(y-WS):(y+WS+1),(x-WS):(x+WS+1)]
            
            for k in range(0,NP):
                RB = iml[(y-WS):(y+WS+1),(x-WS+k):(x+WS+k+1)]
                
                Cost[k] = myCostFunction(LB,RB, BS)
                # print(Cost)                  

            idx = np.argmin(Cost)
            
            DM[y,x] = idx
            
    # print(" Max of DM=", np.max(DM), "Min of DM =", np.min(DM))
    DM_scaled = 16*(DM-np.min(DM))/(np.max(DM)-np.min(DM))
    # print("DM size=", DM.shape, "iml size=", iml.shape)
    plt.imshow(DM_scaled,'gray')
    plt.title("Disparity Map")
    plt.show()
    # cv.wa5itKey(0)
    # return DM

def myCostFunction(LB, RB, BS):
    D_sum=0
    for i in range(BS):
        for j in range(BS):
            D = abs(int(LB[i,j])-int(RB[i,j]))
            D_sum+= D
    return D_sum
    
iml = np.asarray(cv.imread("Rosbot codes/tsukuba_l.png", 0))
imr = np.asarray(cv.imread("Rosbot codes/tsukuba_r.png", 0))
im_disparity =  cv.imread("Rosbot codes/tsukuba_disp.png", 0)
plt.imshow(iml)
plt.show()

(h, w) = iml.shape[:2]

my_DM = myBM_Algo(iml, imr, w, h , 7, 16)

# Stereo BM usin OpenCV
# stereo = cv.StereoBM_create(numDisparities=16, blockSize=17)
# my_DM = stereo.compute(iml,imr)
# plt.imshow(my_DM,'gray')
# plt.show()
# cv.waitKey(0)


        