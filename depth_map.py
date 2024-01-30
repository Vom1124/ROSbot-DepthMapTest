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

np.seterr(divide='ignore', invalid='ignore')#Ignoring the NaN on division

BLOCK_SIZE=5
Center_Element=int(BLOCK_SIZE/2)
Num_Disparities=16

lb=np.empty([BLOCK_SIZE,BLOCK_SIZE])
rb=np.empty([BLOCK_SIZE,BLOCK_SIZE])

# My Cost Function
def myCostFunction(LB,RB, bs, lb=lb,rb=rb):
    # print("LB",LB)
    # print("RB",RB)

    # global lb, rb
    CD=[]
    CD=(np.sum(np.divide(abs(LB-RB), (abs(LB)+abs(RB))))) # Canberra Distance
    # print("","Canberra Distance", CD)


    """
    Proposed metric
    """
    k1=LB<LB[Center_Element][Center_Element]
    # print(k1)
    lb[k1]=0
    lb=abs(LB-LB[Center_Element][Center_Element])

    k2=RB<RB[Center_Element][Center_Element]
    rb[k2]=0
    rb=abs(RB-RB[Center_Element][Center_Element])
    
    kk_thresh=abs(LB-RB)>5
    D_1=float((np.sum(abs(np.multiply(abs(lb-rb),kk_thresh)))))
    # print("D1", D_1)
    if math.isnan((CD)):
        D_sum=((D_1/(bs*bs)))
    elif math.isnan(float(D_1)):
        D_sum=((CD/(bs*bs)))
    else:
        D_sum = (((0.1*CD)+(0.9*D_1))/(bs*bs))
    # print("D_sum", D_sum)
    return D_sum


# Block-Matching algorithm
def myBM_Algo(iml, imr, w, h, BS=BLOCK_SIZE, NP=Num_Disparities):
    # Accepts the left and right image as input to perform stereo correspondence.
    # 'h' is the height, 'w' is the width, 'BS' is the block size, and 'NP' is the disparity range.
    DM = np.zeros([h,w]) # Initializing disparity map
    print("DMtyppe", type(DM), DM.dtype)
    
    Cost = np.empty([NP,1]) #Initializing cost function array to the disparity range
    # print(Cost)
    WS = int((BS-1)/2) # Initializing the window size
    Left_Block = np.empty([BLOCK_SIZE, BLOCK_SIZE]) # Initializing left block
    Right_Block = np.empty([BLOCK_SIZE, BLOCK_SIZE]) # Initializing right block
    
    for y in tqdm(range(WS,h-WS)):
        for x in range(WS,w-(WS+NP)):
            Left_Block = imr[(y-WS):(y+WS+1),(x-WS):(x+WS+1)]
            
            for k in range(0,NP):
                Right_Block = iml[(y-WS):(y+WS+1),(x-WS+k):(x+WS+k+1)]
                Cost[k] = myCostFunction(Left_Block,Right_Block, BS)
            
            # print("x,y",x,y)           
            idx = np.argmin(Cost)
            # print("idx",idx)
                
            DM[y,x] = abs(idx-1)
            
    # print(" Max of DM=", np.max(DM), "Min of DM =", np.min(DM))
    # DM_scaled = 16*(DM-np.min(DM))/(np.max(DM)-np.min(DM))
    # print("DM size=", DM.shape, "iml size=", iml.shape)
    # cv.waitKey(0)
    return DM


iml = np.ndarray.astype(cv.imread("tsukuba_l.png", 0),'float64')
imr = np.ndarray.astype(cv.imread("tsukuba_r.png", 0),'float64')
im_array_type=iml.dtype
im_disparity =  cv.imread("Rosbot codes/tsukuba_disp.png", 0)
plt.imshow(iml)
plt.show()

(h, w) = iml.shape[:2]
my_DM = myBM_Algo((iml), (imr), w, h)
kernel = np.ones((5, 5), np.float64)

plt.imshow(my_DM,'gray')
plt.show()
filterSize =(5,5) 
kernel = cv.getStructuringElement(cv.MORPH_RECT,  
                                   filterSize) 
tophat_img = cv.morphologyEx(my_DM,  
                              cv.MORPH_TOPHAT, 
                              kernel) 
plt.imshow( tophat_img,'gray') 
plt.title("Disparity Map")
plt.show()
# Stereo BM usin OpenCV
# stereo = cv.StereoBM_create(numDisparities=16, blockSize=17)
# my_DM = stereo.compute(iml,imr)
# plt.imshow(my_DM,'gray')
# plt.show()
# cv.waitKey(0)


        