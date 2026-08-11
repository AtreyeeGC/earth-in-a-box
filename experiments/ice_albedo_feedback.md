# Ice-Albedo Feedback & Climate Bistability

## Question
How does a temperature-dependent albedo feedback affect planetary dynamic equilibria?

## Setup
- **Cold Planet:** Starting T = 250 K, Luminosity = 1.00
- **Warm Planet:** Starting T = 280 K, Luminosity = 1.50
- **Simulation Duration:** 200 years (dt = 0.1)
- **Ice-Albedo Rule:**
  - $T \le 250\text{ K} \implies \alpha = 0.60$ (maximum ice cover)
  - $T \ge 290\text{ K} \implies \alpha = 0.20$ (ice-free)
  - Linear transition in between

## Results

| Planet | Starting Temp | Final Temp | Final Albedo | Climate State |
|:---|:---:|:---:|:---:|:---|
| **Cold Planet** | 250.00 K | 221.34 K | 0.60 | Snowball State |
| **Warm Planet** | 280.00 K | 291.30 K | 0.20 | Ice-Free Temperate |

## Conclusion
The ice-albedo interaction functions as a positive feedback mechanism:
1. **Cooling Branch:** When temperature drops, ice accumulation increases planetary albedo, reflecting more solar flux and accelerating cooling into a runaway snowball state.
2. **Warming Branch:** When stellar flux is sufficient, temperature rises, melting ice and lowering albedo, which increases solar absorption and stabilizes the planet in a warm, ice-free state.