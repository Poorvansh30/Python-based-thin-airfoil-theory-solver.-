import numpy as np
import matplotlib.pyplot as plt
from circuilation_distribution import circ_dist

"""
We first build the vortex sheet here on the mean camber line.
func : camber function
aoa  : angle of attack in radians
n    : discretization points
u_inf: free stream velocity 
This function then returns the coordinates of the vortex element (x_v, y_v) with strength dGamma 
"""


def build_vortex_sheet(func, aoa, u_inf, n):
    
    eps = 0.01
    theta = np.linspace(eps, np.pi - eps, n)
    x_v = 0.5*(1 - np.cos(theta))
    y_v = func(x_v)
    gamma, A_o, A = circ_dist(func, aoa, n, 15, u_inf)
    dtheta = theta[1]-theta[0]
    ds = 0.5*(np.sin(theta))*dtheta
    gamma_theta = gamma(theta)
    dGamma = gamma_theta * ds
   
    return x_v, y_v, dGamma    #x coords of vortex, y coords of vortex, dgamma

"""
This function calculates and returns the total velocity components (free stream + induced) at a point (xp, yp)
u = total velocity along x 
v = total velocity along y 
For the velocity calculation, vector form is used which is 
dgamma(dl cross r)/ (2*pi*r^2)

Zip is used to arrange discretized vortex sheet and coordinates together 
"""

def velocity_at_points(xp, yp, func, aoa, u_inf, n):
    
    # build vortex sheet internally — no need to pass dGamma
    x_v, y_v, dGamma = build_vortex_sheet(func, aoa, u_inf, n)
    
    # initialise with free stream
    alpha = np.radians(aoa)
    u = u_inf * np.cos(alpha) * np.ones_like(xp, dtype=float)
    v = u_inf * np.sin(alpha) * np.ones_like(yp, dtype=float)

    # Biot-Savart
    for xv, yv, g in zip(x_v, y_v, dGamma):
        dx = xp - xv
        dy = yp - yv
        r2 = dx**2 + dy**2
        r2 = np.where(r2 < 1e-8, 1e-8, r2)
        u +=  g / (2 * np.pi) * dy / r2          #Calculated using vector form of biot savarts law
        v += -g / (2 * np.pi) * dx / r2

    return u, v

"""
This function plots the velocity contour over the 4c * 3c domain
"""
def field(func, aoa, u_inf, n):
    
    
    x_v, y_v, dGamma = build_vortex_sheet(func, aoa, u_inf, n)  # Building vortex sheet
    aoa_deg = np.rad2deg(aoa)
    
                                       # defining the domain — 4c x 3c, c=1
    xg = np.linspace(-1.5, 2.5, 80)    # 4c along x, centred on airfoil
    yg = np.linspace(-1.5, 1.5, 60)    # 3c along y
    X, Y = np.meshgrid(xg, yg)         # meshgrid is used to make a mesh like structure in the domain
    
    
   
    alpha = np.radians(aoa)
    u = u_inf * np.cos(alpha) * np.ones_like(X)   # initialise with free stream
    v = u_inf * np.sin(alpha) * np.ones_like(Y)
 

    for xv, yv, g in zip(x_v, y_v, dGamma):
        dx = X - xv
        dy = Y - yv
        r2 = dx**2 + dy**2
        r2 = np.where(r2 < 1e-8, 1e-8, r2)
        u +=  g / (2 * np.pi) * dy / r2
        v += -g / (2 * np.pi) * dx / r2          #Calculates velocity at each point in the grid 

   
    speed = np.sqrt(u**2 + v**2)       # Scalar magnitude at each point for the color coding

    
    plt.figure(figsize=(12, 6))

    cf = plt.contourf(X, Y, speed, levels=50, cmap='jet')    #Plotting the contour
    
    plt.colorbar(cf, label='Velocity magnitude (m/s)')
    plt.streamplot(X, Y, u, v, color='white', linewidth=0.8, density=1.5)  #used to define direction of the vector

  
    plt.plot(x_v, y_v, 'k-', linewidth=2, label='Camber line')     # plotting camber line for reference

    plt.xlim(-1.5, 2.5)
    plt.ylim(-1.5, 1.5)
    plt.xlabel('x/c')
    plt.ylabel('y/c')
    plt.title(f'Velocity Field — alpha = {aoa_deg} deg')
    plt.legend()
    plt.grid(False)     
    plt.tight_layout()
    plt.show()
