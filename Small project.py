import matplotlib.pyplot as plt
import numpy as np

# Step 1: get inputs
loads_input = input("Enter forces (lb) separated by commas: ")
loads = [float(f) for f in loads_input.split(',')]  # convert to list of floats

A = float(input("Enter cross-sectional area (square feet): "))
delta_L_input = input("Enter change in lengths (m) separated by commas, or 'auto' to calculate: ")
L = float(input("Enter original length (m): "))
sigma_y = float(input("Enter yield stress (psi): "))

# Step 2: convert area to square inches
A = A * 144  # ft² → in²

# Step 3: calculate stress and strain for all loads
stress_values = []
strain_values = []

for i, F in enumerate(loads):
    stress = F / A
    # Optional: calculate delta_L automatically if user wants
    if delta_L_input.lower() == 'auto':
        strain = stress / (28e6)  # Using E = 28e6 psi for 304 SS
        delta_L = strain * L
    else:
        delta_L_list = [float(x) for x in delta_L_input.split(',')]
        delta_L = delta_L_list[i]
        strain = delta_L / L
    
    # Step 4: ensure stress does not exceed yield
    if stress > sigma_y:
        print(f"Warning: stress {stress:.0f} psi for load {F} lb exceeds yield stress!")
        stress = sigma_y
        strain = sigma_y / (28e6)  # recalc strain at yield
    
    stress_values.append(stress)
    strain_values.append(strain)

# Step 5: plot stress vs strain graph
plt.figure(figsize=(6,4))
plt.plot(strain_values, stress_values, marker='o', color='b')
plt.title("Elastic Behavior (Stress vs Strain)")
plt.xlabel("Strain, m/m")
plt.ylabel("Stress, psi")
plt.grid(True)
plt.show()