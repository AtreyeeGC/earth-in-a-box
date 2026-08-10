from climate import equilibrium_temperature

temperature = equilibrium_temperature(
    luminosity=1.0,
    distance_au=1.0,
    albedo=0.30
)

print(f"Earth's effective temperature: {temperature:.2f} K")
print(f"Earth's effective temperature: {temperature - 273.15:.2f} °C")