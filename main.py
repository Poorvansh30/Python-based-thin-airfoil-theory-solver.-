import numpy as np
import matplotlib.pyplot as plt


from user_inputs import *
from camber_line_plot import *
from function_slope import *
from fourier_coefficients import *
from velocity import *
from circuilation_distribution import *
from velocity_line_integral import *

"""
This main file will import all the required parameters (from user input files) and 
all the necessary functions required to plot and calculate all the deliverables for the assignment. 
"""


"""
Obtaining all the functions and their labels for Camber.
"""
naca_label = NACA_LABEL; naca_func = naca_func()
camber_custom = list(zip(CUSTOM_LABELS, custom_funcs()))

"""
Plotting the NACA camber line and their slope
"""
plt.figure(); plot_camber_line([(naca_label, naca_func)], title=f'{naca_label} Camber Line', n=N)
plt.figure(); plot_camber_slope([(naca_label, naca_func)], title=f'{naca_label} Camber Slope', n=N)

"""
Plotting the Custom camber lines
"""
plt.figure()
plot_camber_line(camber_custom, title='Custom Airfoil Camber Lines', n=N)


"""
Plotting Fourier Coefficients for AOA Range (for NACA airfoil)
"""
aoa = np.radians(np.arange(AOA_START, AOA_END + 0.001, AOA_INTERVAL))
a_0 = A_o(naca_func, aoa, n = N); a_1 = A_m(naca_func, 1, n = N); a_2 = A_m(naca_func, 2, n = N)
a_1 = a_1*np.ones(len(aoa)); a_2 = a_2*np.ones(len(aoa))

plt.figure()
plt.plot(np.rad2deg(aoa), a_0); plt.plot(np.rad2deg(aoa), a_1); plt.plot(np.rad2deg(aoa), a_2)
plt.grid(True); plt.xlabel("AOA (in degrees)"); plt.ylabel("Fourier Coefficients"); plt.title('NACA Fourier coefficients vs AOA (deg)')
plt.legend(["$A_0$", "$A_1$", "$A_2$"])

"""
Plotting values of Cl and Cm for NACA Airfoil
"""
c_l = lift_coefficient(naca_func, aoa, n=N); c_m = moment_coefficient(naca_func, aoa, n = N)
plt.figure(); plt.plot(np.rad2deg(aoa), c_l); plt.xlabel("AOA (in degrees)"); plt.ylabel("$C_l$"); plt.grid(True); plt.title("NACA 6412 $C_l$ vs AOA")
plt.figure(); plt.plot(np.rad2deg(aoa), c_m); plt.xlabel("AOA (in degrees)"); plt.ylabel("$C_m$ about leading edge"); plt.grid(True); plt.title("NACA 6412 $C_m$ vs AOA")

"""
Plotting Circuilation distribution as a function of theta
"""
u_inf = U_INF; aoa_design = np.radians(AOA_DESIGN)
theta = np.linspace(0.02, np.pi, num = N)
gamma, a0, A = circ_dist(naca_func, aoa_design, N, 15, u_inf)
plt.figure()
plt.plot(theta, gamma(theta)); plt.xlabel(r'$\theta$ (radians)'); plt.ylabel(r'$\gamma(\theta)$')
plt.title(r'$\gamma(\theta)$ at $\alpha$ = ' + f'{AOA_DESIGN} degrees'); plt.grid(True)

"""
Calculating Bound Circuilation using: (a) Integration of circuilation distribution
                                      (b) Line integral of Velocity (Stoke's Theorem)
"""
# (a) Integrate gamma(theta) * ds along camber line
ds = 0.5 * np.sin(theta)       # x was defined as 0.5*(1-cos(theta)),ans assuming small angle, ds = dx
bound_circ_dist_integ = np.trapezoid(gamma(theta) * ds, theta)
print(f"Bound Circulation (gamma.ds integral) = {bound_circ_dist_integ:.4f}")
# (b) Line integral of velocity around rectangular contour
bound_circ_line_integ = -1*circulation_integral(naca_func, aoa_design, u_inf, N)
print(f"Bound Circulation (Stoke's theorem) = {bound_circ_line_integ:.4f}")

"""
Plotting velocity contour
"""
field(naca_func, aoa_design, u_inf, n = N)

"""
Plotting Cl vs AOA and Cm vs AOA for all 4 airfoils on same graph (3 Custom and 1 NACA)
"""
# Calculating and plotting Cl for Custom Airfoil 1, 2 and 3 and NACA 6412
c_l1 = lift_coefficient(CUSTOM_1, aoa, n = N); c_l2 = lift_coefficient(CUSTOM_2, aoa, n = N); c_l3 = lift_coefficient(CUSTOM_3, aoa, n = N)
plt.figure(); 
plt.plot(np.rad2deg(aoa), c_l1); plt.plot(np.rad2deg(aoa), c_l2); plt.plot(np.rad2deg(aoa), c_l3); plt.plot(np.rad2deg(aoa), c_l)
plt.grid(True); plt.legend(["Custom Airfoil 1", "Custom Airfoil 2", "Custom Airfoil 3", "NACA"]); 
plt.xlabel('AOA (in degrees)'); plt.ylabel('$C_l$'); plt.title('Lift Coefficients vs AOA')
# Calculating and plotting Cm for Airfoil 1, 2 and 3 and NACA 6412
c_m1 = moment_coefficient(CUSTOM_1, aoa, n = N); c_m2 = moment_coefficient(CUSTOM_2, aoa, n = N); c_m3 = moment_coefficient(CUSTOM_3, aoa, n = N)
plt.figure()
plt.plot(np.rad2deg(aoa), c_m1); plt.plot(np.rad2deg(aoa), c_m2); plt.plot(np.rad2deg(aoa), c_m3); plt.plot(np.rad2deg(aoa), c_m)
plt.grid(True); plt.legend(["Custom Airfoil 1", "Custom Airfoil 2", "Custom Airfoil 3", "NACA"]); 
plt.xlabel('AOA (in degrees)'); plt.ylabel('$C_m$'); plt.title('Moment Coefficients vs AOA')

"""
Plotting velocity contours for Custom airfoils
"""
field(CUSTOM_1, aoa_design, u_inf, n = N); plt.title(f"Custom Airfoil 1 velocity contour at AOA = {AOA_DESIGN} degrees")
field(CUSTOM_2, aoa_design, u_inf, n = N); plt.title(f"Custom Airfoil 2 velocity contour at AOA = {AOA_DESIGN} degrees")
field(CUSTOM_3, aoa_design, u_inf, n = N); plt.title(f"Custom Airfoil 3 velocity contour at AOA = {AOA_DESIGN} degrees")




