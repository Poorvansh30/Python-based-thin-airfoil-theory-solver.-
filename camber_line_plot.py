

import numpy as np
import matplotlib.pyplot as plt
from function_slope import dz_dx
from user_inputs import NACA_M, NACA_P, NACA_LABEL, CUSTOM_1, CUSTOM_2, CUSTOM_3, CUSTOM_LABELS, N

"""
 This Function builds and returns NACA camber function using parameters from user inputs file.
 Using lambda wrapper to return a callable function func, so that we can use it for other functions like Slope calculation,
 Circuilation distribution etc.
"""
def naca_func():
   
    m = NACA_M / 100.0    # max camber as fraction of chord
    p = NACA_P / 10.0     # max camber location as fraction of chord
    if m == 0:
        
        func = lambda x: np.zeros_like(np.asarray(x, dtype=float)) #if m = 0, p = 0, division by zero would throw an error
    else:
        func = lambda x: np.where(
            x < p,
            (m / p**2) * (2*p*x - x**2),
            (m / (1-p)**2) * (1 - 2*p + 2*p*x - x**2)
        )

    return func


"""
Here, We accept custom functions that the user wants to analyse using Thin airfoil method. Custom functions
already comes lambda wrapped
"""
def custom_funcs():
    
    return [CUSTOM_1, CUSTOM_2, CUSTOM_3]


"""
This function accepts a tuple of the format (label, func) where label is the name of the airfoil (for ef NACA 6412)
and func is function associated with that airfoil. It plots the normalisec camber line plot
"""
def plot_camber_line(funcs_labels, title="Camber Lines",  n=N ):
    
    x = np.linspace(0, 1, n)
    for label, func in funcs_labels:
        z = func(x)                                    # Calculate the function value at these discretized x values
        plt.plot(x, z, lw=2, label=label)

    
    plt.xlabel('x/c');  plt.ylabel('z/c')
    plt.title(title)
    plt.xlim(-0.05, 1.05)                              # x limits set for proper visualisation of graphs
    plt.ylim(-0.3, 0.8)                                # Similarly y limits are set to ensure camber is visible 
    plt.legend();  plt.grid(True, alpha=0.4)
    plt.show()

""" 
This function also accepts a tuple (same as above) and plots the slope of the normalised camber line
"""
def plot_camber_slope(funcs_labels, title="Camber Slopes", n=N ):
    
    x = np.linspace(0, 1, n)
    for label, func in funcs_labels:
        z     = func(x)
        slope = dz_dx(z)                            # Calculates the slope using the function defined in function_slope
        plt.plot(x, slope, lw=2, label=label)

   
    plt.xlabel('x/c');  plt.ylabel('dz/dx')
    plt.title(title)
    plt.legend();  plt.grid(True, alpha=0.4)
    plt.show()
    
    