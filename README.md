# Thin Airfoil Theory Simulator

A modular Python tool that implements classical **Thin Airfoil Theory** to analyze NACA and custom-designed airfoils — computing camber geometry, Fourier coefficients, lift/moment coefficients, circulation distribution, and the induced velocity field — without requiring a full CFD setup.

Built for **AE 244: Assignment 2** (IIT Bombay), as a faster analytical companion to the CFD (ANSYS) analysis done in Assignment 1.

> **Author:** Poorvansh Jain (24B0061), B.Tech Aerospace Engineering, IIT Bombay

---

## Overview

Thin Airfoil Theory lets you approximate an airfoil's aerodynamic behavior directly from its camber line, without meshing or solving the full Navier–Stokes equations. This project implements the theory end-to-end:

1. Define a camber line — either a standard **NACA 4-digit** airfoil or any **custom function** `y = f(x)`.
2. Compute its slope numerically.
3. Decompose the slope into a Fourier series to get **A₀, A₁, A₂** and hence **C_l** and **C_m**.
4. Build a bound-vortex sheet along the camber line and compute the **circulation distribution γ(θ)**.
5. Use the Biot–Savart law to compute the **induced velocity field** around the airfoil and visualize it as a streamline/contour plot.
6. Cross-validate bound circulation two ways: by integrating γ(θ) directly, and via a **velocity line integral** around a rectangular control volume.

Results for the NACA 6412 airfoil are validated against ANSYS CFD data from Assignment 1.

---

## Features

- **Camber line generation** for NACA 4-digit (thin-airfoil approximation) or arbitrary custom functions
- **Numerical slope computation** (finite differences) with linear interpolation to query slope at any point
- **Fourier coefficient solver** (A₀, A₁, A₂, …, A_p) via trapezoidal integration over the θ-transformed chord
- **C_l and C_m vs α** computation and comparison against CFD results
- **Circulation distribution γ(θ)** along the vortex sheet, satisfying the Kutta condition
- **Vector field / velocity contour plots** around the airfoil using the Biot–Savart law
- **Bound circulation** via two independent methods (distribution integration vs. closed-loop velocity line integral)
- Fully **modular**, file-per-function structure with a single central `user_inputs.py` for configuration

---

## Repository Structure

```
.
├── main.py                        # Orchestrates all functions; produces all plots/results
├── user_inputs.py                 # Central config: NACA params, custom airfoils, flight conditions
├── camber_line_plot.py            # Camber line generation (NACA + custom) and plotting
├── function_slope.py              # Numerical slope (dz/dx) computation and point-slope interpolation
├── fourier_coefficients.py        # A0, Am, lift coefficient (Cl), moment coefficient (Cm)
├── circuilation_distribution.py   # Bound vortex sheet strength gamma(theta)
├── velocity.py                    # Biot-Savart induced velocity field + vector/contour plotting
├── velocity_line_integral.py      # Circulation via closed-loop line integral (validation method)
└── README.md
```

---

## Theory Summary

The camber line is transformed using `x = 0.5(1 − cos θ)`, and the local slope `dz/dx` is expanded in a Fourier cosine series:

- **A₀** = α − (1/π) ∫₀^π (dz/dx) dθ
- **Aₙ** = (2/π) ∫₀^π (dz/dx) cos(nθ) dθ

From these:

- **C_l** = π (2A₀ + A₁)
- **C_m,LE** = −(π/2) (A₀ + A₁ − 0.5·A₂)

The circulation distribution along the vortex sheet is:

γ(θ) = 2U∞ [A₀(1 + cos θ)/sin θ + Σₙ Aₙ sin(nθ)]

which satisfies the Kutta condition (γ = 0 at the trailing edge, θ = π). Each vortex element's contribution to velocity elsewhere in the flow is computed via the Biot–Savart law, and total bound circulation is cross-checked using a closed rectangular contour integral of velocity (Γ = ∮ V·ds).

For full step-by-step algorithms (with flowcharts) for each function, see the accompanying assignment report/presentation.

---

## Getting Started

### Requirements

- Python 3.8+
- `numpy`
- `matplotlib`

```bash
pip install numpy matplotlib
```

### Running

1. Open `user_inputs.py` and set your parameters:
   - `NACA_M`, `NACA_P` — NACA airfoil digits (max camber, max camber location)
   - `CUSTOM_1`, `CUSTOM_2`, `CUSTOM_3` — your own camber functions `y = f(x)`, normalized to a unit chord (0 at x=0 and x=1)
   - `U_INF`, `RHO` — flight condition
   - `AOA_DESIGN`, `AOA_START`, `AOA_END`, `AOA_INTERVAL` — angle-of-attack sweep
   - `N` — discretization points

2. Run the main script:

```bash
python main.py
```

This generates all plots: camber lines, camber slope, Fourier coefficients vs α, C_l & C_m vs α, circulation distribution, bound circulation values, and the velocity field around the airfoil — for both the NACA airfoil and your 3 custom designs.

---

## Sample Results (NACA 6412)

| Quantity | This Tool (Thin Airfoil Theory) | ANSYS CFD |
|---|---|---|
| C_l trend vs α | Linear (slope 2π), no stall | Matches closely at low α; saturates near stall due to viscous separation |
| C_m,LE | Negative, roughly linear in α | Slightly more negative; deviation grows with α (drag/separation effects) |
| Bound circulation @ α = 3° | ~8.27 (distribution integration) / ~8.30 (line integral) | — |

Key limitations of the thin-airfoil approach (as observed against CFD):
- No viscosity → no boundary layer, no stall, no wake
- Small-angle and thin-airfoil assumptions break down at high α or high thickness
- Cannot predict drag

---

## Custom Airfoil Designs

Three exploratory custom camber functions were analyzed alongside the NACA 6412 baseline to study how camber shape affects A₀/A₁/A₂, C_l, C_m, and the induced velocity field. See the report for full plots and discussion.

---

## Acknowledgements

Developed as part of AE 244 (Aerospace Vehicle Design), IIT Bombay. Team contribution details and acknowledgements are documented in the accompanying assignment report.

## References

- Anderson, J.D., *Fundamentals of Aerodynamics* — Thin Airfoil Theory
- Assignment 1 CFD (ANSYS) results, used for validation
