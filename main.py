import matplotlib.pyplot as plt
import numpy as np

def get_inputs():
    loads_input = input("Enter forces (lb) separated by commas: ")
    loads = [float(f) for f in loads_input.split(',')]

    A = float(input("Enter cross-sectional area (ft^2): "))
    L = float(input("Enter original length (m): "))
    sigma_y = float(input("Enter yield stress (psi): "))

    delta_L_input = input("Enter change in length values or 'auto': ")

    return loads, A, L, sigma_y, delta_L_input

def compute_stress_strain(loads, A, L, sigma_y, delta_L_input):
    A = A * 144  # ft² ? in²

    stress_values = []
    strain_values = []

    for i, F in enumerate(loads):
        stress = F / A

        if delta_L_input.lower() == 'auto':
            E = 28e6  # psi (304 SS approximation)
            strain = stress / E
        else:
            delta_L_list = [float(x) for x in delta_L_input.split(',')]
            strain = delta_L_list[i] / L

        if stress \u003e sigma_y:
            stress = sigma_y
            strain = sigma_y / 28e6

        stress_values.append(stress)
        strain_values.append(strain)

    return np.array(strain_values), np.array(stress_values)

def analyze_material(strain, stress):
    # Young's Modulus from elastic region (first 2-3 points)
    n = min(3, len(strain))
    E = np.polyfit(strain[:n], stress[:n], 1)[0]

    max_stress = np.max(stress)
    max_strain = np.max(strain)

    return E, max_stress, max_strain

def plot_curve(strain, stress, E):
    plt.figure(figsize=(7,5))
    plt.plot(strain, stress, marker='o', label='Stress-Strain Curve')

    plt.title("Material Stress-Strain Behavior")
    plt.xlabel("Strain (m/m)")
    plt.ylabel("Stress (psi)")
    plt.grid(True)

    plt.text(0.0005, max(stress)*0.8,
             f"Young's Modulus ˜ {E:.2e} psi",
             fontsize=10)

    plt.legend()
    plt.show()

def main():
    loads, A, L, sigma_y, delta_L_input = get_inputs()

    strain, stress = compute_stress_strain(loads, A, L, sigma_y, delta_L_input)

    E, max_stress, max_strain = analyze_material(strain, stress)

    print("\n--- Material Summary ---")
    print(f"Young's Modulus: {E:.2e} psi")
    print(f"Max Stress: {max_stress:.2f} psi")
    print(f"Max Strain: {max_strain:.5f}")

    plot_curve(strain, stress, E)


if __name__ == "__main__":
    main()
