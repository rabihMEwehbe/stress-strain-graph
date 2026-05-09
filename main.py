import matplotlib.pyplot as plt
import numpy as np


def get_inputs():
    loads_input = input("Enter forces (lb) separated by commas: ")
    loads = [float(f) for f in loads_input.split(',')]

    area_ft2 = float(input("Enter cross-sectional area (ft²): "))
    length = float(input("Enter original length (m): "))
    sigma_y = float(input("Enter yield stress (psi): "))
    delta_L_input = input("Enter ΔL values or 'auto': ")

    return loads, area_ft2, length, sigma_y, delta_L_input


def compute_stress_strain(loads, area_ft2, length, sigma_y, delta_L_input):
    E = 28e6  # psi (typical steel assumption)

    area_in2 = area_ft2 * 144  # ft² → in²

    stress_values = []
    strain_values = []

    for i, F in enumerate(loads):
        stress = F / area_in2

        if delta_L_input.lower() == "auto":
            strain = stress / E
        else:
            delta_L_list = [float(x) for x in delta_L_input.split(',')]
            strain = delta_L_list[i] / length

        # yield warning (elastic model only)
        if stress \u003e sigma_y:
            print(f"Warning: Load {F} lb exceeds yield stress!")

        stress_values.append(stress)
        strain_values.append(strain)

    return np.array(strain_values), np.array(stress_values), E


def analyze(strain, stress):
    E_est = np.polyfit(strain[:3], stress[:3], 1)[0]
    return E_est


def plot_results(strain, stress, sigma_y, E):
    plt.figure(figsize=(7, 5))

    plt.plot(strain, stress, marker='o', linewidth=2, label="Stress–Strain Curve")

    plt.axhline(y=sigma_y, linestyle='--', color='r', label="Yield Stress")

    plt.title("Stress–Strain Behavior (Elastic Region)")
    plt.xlabel("Strain (m/m)")
    plt.ylabel("Stress (psi)")
    plt.grid(True)
    plt.legend()

    plt.text(
        0.0005,
        max(stress) * 0.8,
        f"E ≈ {E:.2e} psi",
        fontsize=10,
        bbox=dict(facecolor='white', alpha=0.7)
    )

    plt.show()


def main():
    loads, area, length, sigma_y, delta_L_input = get_inputs()

    strain, stress, E = compute_stress_strain(
        loads, area, length, sigma_y, delta_L_input
    )

    E_est = analyze(strain, stress)

    print("\n--- Material Summary ---")
    print(f"Young's Modulus (input assumption): {E:.2e} psi")
    print(f"Estimated Modulus (from data): {E_est:.2e} psi")
    print(f"Max Stress: {np.max(stress):.2f} psi")
    print(f"Max Strain: {np.max(strain):.6e}")

    plot_results(strain, stress, sigma_y, E)


if __name__ == "__main__":
    main()
