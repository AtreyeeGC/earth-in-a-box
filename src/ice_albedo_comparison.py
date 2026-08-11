import matplotlib.pyplot as plt

from src.feedbacks import ice_albedo
from src.time_model import temperature_step


# --------------------------------------------------
# Simulation settings
# --------------------------------------------------

DISTANCE = 1.0
ALBEDO_UNUSED = 0.30

TOTAL_YEARS = 200
TIME_STEP = 0.1


# --------------------------------------------------
# Planet configurations
# --------------------------------------------------

PLANETS = {
    "Cold Planet": {
        "starting_temperature": 250.0,
        "luminosity": 1.00,
    },
    "Warm Planet": {
        "starting_temperature": 280.0,
        "luminosity": 1.50,
    },
}


# --------------------------------------------------
# Run simulations
# --------------------------------------------------

results = {}


for name, parameters in PLANETS.items():

    temperature = parameters["starting_temperature"]
    luminosity = parameters["luminosity"]

    years = [0.0]
    temperatures = [temperature]
    albedos = [ice_albedo(temperature)]

    steps = int(TOTAL_YEARS / TIME_STEP)

    for step in range(1, steps + 1):

        current_year = step * TIME_STEP

        albedo = ice_albedo(temperature)

        temperature = temperature_step(
            temperature=temperature,
            luminosity=luminosity,
            distance_au=DISTANCE,
            albedo=albedo,
            years=TIME_STEP,
            emissivity=1.0,
        )

        years.append(current_year)
        temperatures.append(temperature)
        albedos.append(albedo)

    results[name] = {
        "years": years,
        "temperatures": temperatures,
        "albedos": albedos,
    }


# --------------------------------------------------
# Print results
# --------------------------------------------------

print()
print("=== Ice-Albedo Comparison ===")
print()

for name, result in results.items():

    final_temperature = result["temperatures"][-1]
    final_albedo = result["albedos"][-1]

    print(name)
    print(
        f"  Final temperature: "
        f"{final_temperature:.2f} K"
    )
    print(
        f"  Final albedo: "
        f"{final_albedo:.2f}"
    )
    print()


# --------------------------------------------------
# Plot temperature
# --------------------------------------------------

plt.figure(figsize=(10, 6))

for name, result in results.items():

    plt.plot(
        result["years"],
        result["temperatures"],
        linewidth=2,
        label=name,
    )

plt.xlabel("Time (years)")
plt.ylabel("Temperature (K)")

plt.title(
    "Earth in a Box — Ice-Albedo Feedback"
)

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()

plt.savefig(
    "ice_albedo_comparison.png",
    dpi=200,
)

plt.show()