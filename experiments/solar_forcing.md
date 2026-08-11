# Solar Forcing Experiment

## Question

How does planetary equilibrium temperature respond to changes
in stellar luminosity?

## Setup

Planet:
- Orbital distance: 1 AU
- Albedo: 0.30
- Starting temperature: 250 K
- Forcing begins: year 50
- Simulation duration: 150 years
- Time step: 0.1 years

## Results

| Solar luminosity | Equilibrium temperature |
|------------------:|------------------------:|
| -2% | 253.30 K |
|  0% | 254.59 K |
| +1% | 255.22 K |
| +2% | 255.85 K |
| +5% | 257.71 K |

## Conclusion

Increasing stellar luminosity increases the planet's
equilibrium temperature.

The relationship is nonlinear and follows approximately:

T ∝ L^(1/4)

because outgoing thermal radiation follows the
Stefan-Boltzmann relationship:

F = σT⁴.

The simulation also demonstrates that the planet does not
instantaneously reach its new equilibrium. Because the climate
system has heat capacity, temperature changes gradually over time.