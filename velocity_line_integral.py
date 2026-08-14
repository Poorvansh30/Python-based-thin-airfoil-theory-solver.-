import numpy as np
from velocity import velocity_at_points

"""
 Computes circulation Gamma = closed integral of V.ds along a rectangular boundary enclosing the airfoil.
 Boundary: x from -1.5 to 2.5, y from -1.5 to 1.5 (as specified in the instructions)
"""

def circulation_integral(func, aoa, u_inf, n):
   
    
    n_seg = n   # points per side of rectangle
    
    Gamma = 0.0   # initialise circulation
    
    # Bottom edge: left to right at y = -1.5
    xb = np.linspace(-1.5, 2.5, n_seg)
    yb = np.full_like(xb, -1.5)
    ub, vb = velocity_at_points(xb, yb, func, aoa, u_inf, n)
    Gamma += np.sum(ub * (xb[1]-xb[0]))   #since dy = 0 along bottom edge and dx is uniform
    
    # Right edge: bottom to top at x = 2.5
    yr = np.linspace(-1.5, 1.5, n_seg)
    xr = np.full_like(yr, 2.5)
    ur, vr = velocity_at_points(xr, yr, func, aoa, u_inf, n)
    Gamma += np.sum(vr * (yr[1]-yr[0]))
    
    # Top edge: right to left at y = 1.5
    xt = np.linspace(2.5, -1.5, n_seg)
    yt = np.full_like(xt, 1.5)
    ut, vt = velocity_at_points(xt, yt, func, aoa, u_inf, n)
    Gamma += np.sum(ut * (xt[1] - xt[0]))

    
    # Left edge: top to bottom at x = -1.5
    yl = np.linspace(1.5, -1.5, n_seg)
    xl = np.full_like(yl, -1.5)
    ul, vl = velocity_at_points(xl, yl, func, aoa, u_inf, n)
    Gamma += np.sum(vl * (yl[1] - yl[0]))
    
    return Gamma