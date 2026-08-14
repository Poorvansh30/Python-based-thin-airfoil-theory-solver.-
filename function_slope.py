import numpy as np

"""
This function accepts z = func(x) and then calculates derivative using the definition of derivative
(first principle)
"""
def dz_dx(z):
    
    slope = np.zeros(len(z))
    for i in range(1,len(z)): 
        slope[i] = (z[i] - z[i-1])/(1/(len(z)-1))
    slope[0] = slope[1]  #to make both func and slope array of the same size
    return slope

"""
 This function computes slope at a point. If point does not belong to the discretized domain, 
 it linearly interpolates the slope to get the slope at that particular points
"""
def slope_at_point(x, slope):
   
    x_cords = float(input("enter the x cordinate at which you want the slope: "))
    for i in range(0, len(slope)): 
        if x[i] < x_cords <= x[i+1]:
            m = (slope[i+1]-slope[i])*(len(slope)-1)
            c = slope[i] - (m*x[i]) 
            slope_x = m*x_cords + c
            return slope_x
            

