import os
import sys
import time

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
# from numpy.random import rand
import math
from tqdm import tqdm

np.seterr(divide='ignore', invalid='ignore')#Ignoring the NaN on division

BLOCK_SIZE=5
Center_Element=int(BLOCK_SIZE/2)
Num_Disparities=16

# My Cost Function
def myCostFunction(LB,RB):
    # print("LB",LB)
    # print("RB",RB)
 
    CD=(np.sum(np.divide(abs(LB-RB), abs(LB)+abs(RB)))) # Canberra Distance
    print("","Canberra Distance", CD)


    """
    Proposed metric
    """
    k1=LB<LB[Center_Element][Center_Element]
    LB[k1]=0
    LB=abs(LB-LB[Center_Element][Center_Element])

    k2=RB<RB[Center_Element][Center_Element]
    RB[k2]=0
    RB=abs(RB-RB[Center_Element][Center_Element])
    
    kk_thresh=abs(LB-RB)>5
    D_1=(np.sum(abs(np.multiply(abs(LB-RB),kk_thresh))))
    print("D1", D_1)
    D_sum = ( (0.1*CD) + (0.9*D_1) )/(BLOCK_SIZE*BLOCK_SIZE)
    # print("D_sum", D_sum, type(D_sum), D_sum.dtype)
    return D_sum


# Block-Matching algorithm
def myBM_Algo(iml, imr, w, h, BS, NP):
    # Accepts the left and right image as input to perform stereo correspondence.
    # 'h' is the height, 'w' is the width, 'BS' is the block size, and 'NP' is the disparity range.
    DM = np.zeros([h,w]) # Initializing disparity map
    # print("DMtyppe", type(DM), DM.dtype)
    LB = np.empty([BS, BS]) # Initializing left block
    RB = np.empty([BS, BS]) # Initializing right block
    
    Cost = np.empty([NP,1]) #Initializing cost function array to the disparity range
    print(Cost)
    WS = int((BS-1)/2) # Initializing the window size
    
    for y in tqdm(range(WS,h-WS)):
        for x in range(WS,w-(WS+NP)):
            Left_Block = imr[(y-WS):(y+WS+1),(x-WS):(x+WS+1)]
            
            for k in range(0,NP):
                Right_Block = iml[(y-WS):(y+WS+1),(x-WS+k):(x+WS+k+1)]
                
                Cost[k] = myCostFunction(Left_Block,Right_Block)
                
            print(Cost)       
            print("x,y",x,y)           
            idx = np.argmin(Cost)
            print("idx",idx)
                
            DM[y,x] = abs(np.argmin(Cost))
            
    # print(" Max of DM=", np.max(DM), "Min of DM =", np.min(DM))
    #DM_scaled = 16*(DM-np.min(DM))/(np.max(DM)-np.min(DM))
    # print("DM size=", DM.shape, "iml size=", iml.shape)

    # cv.waitKey(0)
    return DM

    
iml = np.ndarray.astype(cv.imread("Rosbot codes/tsukuba_l.png", 0),'int32')
imr = np.ndarray.astype(cv.imread("Rosbot codes/tsukuba_r.png", 0),'int32')
im_array_type=iml.dtype
im_disparity =  cv.imread("Rosbot codes/tsukuba_disp.png", 0)
plt.imshow(iml)
plt.show()

(h, w) = iml.shape[:2]

my_DM = myBM_Algo(iml, imr, w, h , BLOCK_SIZE, Num_Disparities)
plt.imshow(my_DM,'gray')
plt.title("Disparity Map")
plt.show()
# Stereo BM usin OpenCV
# stereo = cv.StereoBM_create(numDisparities=16, blockSize=17)
# my_DM = stereo.compute(iml,imr)
# plt.imshow(my_DM,'gray')
# plt.show()
# cv.waitKey(0)


        