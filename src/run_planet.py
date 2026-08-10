from src.planet import Planet

earth = Planet(
    name="Earth",
    star_luminosity=1.0,
    orbital_distance=1.0,
    albedo=0.30,
    atmospheric_emissivity=0.80,
)


effective_temperature = earth.effective_temperature()
surface_temperature = earth.surface_temperature()


print(f"Planet: {earth.name}")
print(f"Effective temperature: {effective_temperature:.2f} K")
print(f"Surface temperature: {surface_temperature:.2f} K")
print(f"Surface temperature: {surface_temperature - 273.15:.2f} °C")