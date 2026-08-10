from src.planet import Planet


planets = [
    Planet(
        name="Earth",
        star_luminosity=1.0,
        orbital_distance=1.0,
        albedo=0.30,
        atmospheric_emissivity=0.80,
    ),

    Planet(
        name="Hot Planet",
        star_luminosity=2.0,
        orbital_distance=1.0,
        albedo=0.30,
        atmospheric_emissivity=0.80,
    ),

    Planet(
        name="Ice Planet",
        star_luminosity=1.0,
        orbital_distance=1.0,
        albedo=0.70,
        atmospheric_emissivity=0.80,
    ),

    Planet(
        name="Distant Planet",
        star_luminosity=1.0,
        orbital_distance=2.0,
        albedo=0.30,
        atmospheric_emissivity=0.80,
    ),
]


print("EARTH IN A BOX — PLANETARY LABORATORY")
print("=" * 55)

for planet in planets:
    effective = planet.effective_temperature()
    surface = planet.surface_temperature()

    print(f"\n{planet.name}")
    print(f"  Effective temperature: {effective:.2f} K")
    print(f"  Surface temperature:   {surface:.2f} K")
    print(f"  Surface temperature:   {surface - 273.15:.2f} °C")