# 1D Seasonal Climate Simulation

## Objective
Simulate spatio-temporal temperature distributions across 18 latitude bands over a 365-day orbital cycle with an axial tilt of 23.44°.

## Model Architecture
- **Grid Resolution:** 18 latitude bands (10° width per band)
- **Solar Physics:** Daily top-of-atmosphere insolation based on solar declination and sunset hour angles
- **Thermal Transport:** Budyko meridional heat diffusion ($D = 3.8 \text{ W/m}^2\text{K}$)
- **Thermal Capacity:** 50m ocean mixed-layer heat capacity ($C = 2.1 \times 10^8 \text{ J/m}^2\text{K}$)

## Key Results
- **Equator Mean:** 286.38 K (Seasonal Range: 285.6 K – 287.1 K)
- **North Pole Mean:** 257.93 K (Seasonal Range: 254.9 K – 261.2 K)
- **Thermal Behavior:** Smooth seasonal heat transfer across the equator, demonstrating hemispheric thermal lag.