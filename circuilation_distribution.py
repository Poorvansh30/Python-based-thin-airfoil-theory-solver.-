from fourier_coefficients import A_o, A_m
import numpy as np

"""
This function calculates gamma (theta) as a function and returns it. It calculates A0, A1, A2..... 
till Ap and then sums them to obtain the gamma distribution. 
Since the summation series is Convergent, We thought p = 15 would be enough and thus in calculations
We have used p = 15
func : camber function
aoa  : angle of attack in radians
n    : discretization points
p    : number of fourier terms to sum
u_inf: free stream velocity 
""" 
def circ_dist(func, aoa, n, p, u_inf):
    
    # compute A0 once
    A0 = A_o(func, aoa, n)
    
    # compute all An coefficients up to p
    A = np.zeros(p+1)        # A[0] unused, A[1] to A[p]
    for i in range(1, p+1):
        A[i] = A_m(func, i, n)
    
    # build gamma as function of theta
    def gamma(theta):
        # A0 term
        result = A0 * (1 + np.cos(theta)) / np.sin(theta)
        
        # Summation terms
        for i in range(1, p+1):
            result += A[i] * np.sin(i * theta)
        
        return (2*u_inf)*result
    
    return gamma, A0, A

