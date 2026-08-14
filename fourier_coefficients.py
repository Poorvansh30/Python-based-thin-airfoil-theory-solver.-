import numpy as np
from function_slope import dz_dx

"""
This function computes A_0 and remaining fourier coefficients (A_m)
func = User defined function/ NACA airfoil function
aoa = Input Angle of attack
n = number points for discretization points 
m = used for calculation of mth Fourier coefficient
"""
def A_o(func, aoa, n): 
    theta = np.linspace(0, np.pi, num = n, endpoint = True)
    x = 0.5*(1 - np.cos(theta))
    z = func(x)
    #if constant function is passed
    if isinstance(z,(int,float)):
        z=np.full_like(x, float(z))
    slope = dz_dx(z)
    first_fourier = aoa - (1/np.pi)*(np.trapezoid(slope, theta))
    return first_fourier


#Since every other fourier coefficient is independent of AOA, no need to input AOA
def A_m(func, m, n):  #m corresponds to mth fourier coefficient
    theta = np.linspace(0, np.pi, num = n, endpoint = True)
    x = 0.5*(1 - np.cos(theta))
    z = func(x)
    """
    If block is used here inorder to convert constant function into an array for slope calculation.
    """
    if isinstance(z,(int,float)):
        z=np.full_like(x, float(z))
    slope = dz_dx(z)
    m_fourier = (2/np.pi)*(np.trapezoid(slope*np.cos(m*theta), theta))
    return m_fourier

"""
Computes Lift coefficient using by calling the above fourier functions.
""" 
def lift_coefficient(func ,aoa, n): 
    return np.pi*((2*A_o(func, aoa, n)) + A_m(func, 1, n))

"""
Computes Moment coefficient using by calling the above fourier functions.
""" 
def moment_coefficient(func, aoa, n): 
    return (-np.pi/2)*(A_o(func, aoa, n) + A_m(func, 1, n) - (0.5*A_m(func, 2, n)))
