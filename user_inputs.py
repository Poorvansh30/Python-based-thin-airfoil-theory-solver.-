"""
user input file
Central file for all user-defined parameters.
Edit the required parameters here and just run the main file. (main.py)
"""

import numpy as np

# NACA Airfoil 
NACA_M = 6      # first digit  (max camber * 100)
NACA_P = 4   # second digit (max camber location * 10)
# Last two digits of airfoil are irrelevant because we are approximating it to a thin airfoil and last two digits tell us the thickness of the airfoil
NACA_LABEL = 'NACA 6412' # enter the airfoil full name (that you want to analyse)

# Custom Airfoils 
CUSTOM_1 = lambda x: 0.08*x*(1-x**2)
CUSTOM_2 = lambda x: 0.06* np.sin(np.pi * x)
CUSTOM_3 = lambda x: 0.05 * np.log(x*(1-x) + 1)

CUSTOM_LABELS = ["Custom 1", "Custom 2", "Custom 3"]

# Flight Conditions 
U_INF        = 20.0    # free stream velocity (m/s)
RHO          = 1.225   # air density (kg/m^3)
AOA_DESIGN     = 3.0     # design angle of attack (degrees)
AOA_START    = -3.0    
AOA_END      = 12.0
AOA_INTERVAL = 3.0     # AOA range for Cl, Cm and Fourier Calculations (degrees)

# Discretization Points
N = 1000
