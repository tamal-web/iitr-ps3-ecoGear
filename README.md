# Eco-Gear Controller Report
## Submission by- Tamal Krishna Chhabra (AUP)

## Overview
This report documents the design and performance of the robust Eco-Gear Controller developed for the Sentry Rover. The controller is designed to navigate complex terrains while optimizing for energy efficiency and strict time limits. It moves beyond hardcoded parameters, utilizing real-time physics calculations to adapt to any track configuration.

## Core Control Strategy
The controller implements a physics-first approach with the following key features:

*   **Physics-Based Optimization**: Continuously calculates the "Optimal Cruise Speed" where aerodynamic drag forces exactly balance rolling resistance ($F_{drag} = F_{roll}$), ensuring theoretical minimum energy waste on flat terrain.
*   **Dynamic Friction Adaptation**: Monitors the surface friction coefficient ($\mu$). On low-traction surfaces (Ice, Mud), it drastically reduces torque output (Safety Factor 0.25) to stay within the linear region of the tire slip curve, preventing energy-wasting wheel spin.
*   **Predictive Look-Ahead**: Scans the upcoming 40m of track.
    *   **Sprints** before steep hills (>11% grade) to build essential momentum.
    *   **Slows down** before low-friction zones to ensure safe traversing.
*   **Gravity-Aware Soft Start**: Calculates the precise torque required to overcome gravity roll-back and static friction on uphills, ensuring smooth launches without stalling or burning out tires.
*   **Pulse-and-Glide**: On long flat sections, utilizes a hysteresis control loop to pulse acceleration and then coast, exploiting the vehicle's momentum.
*   **Adaptive Pacing**: Adjusts minimum speed targets based on track length. Long endurance tracks (>400m) maintain a higher average speed to combat strict time limits, while shorter tracks prioritize aerodynamic efficiency.

## Robustness & Testing
The controller has been rigorously stressed-tested against **16 diverse track configurations**, passing 100% of cases.

### Test Suite Highlights:
| Track Type | Challenge | Result |
| :--- | :--- | :--- |
| **Practice Track** | Mixed terrain, baseline efficiency | **PASSED** (1.5x Ideal Energy) |
| **Ice Wall** | Steep gradient + Very low friction (0.35) | **PASSED** |
| **The Wall** | Extreme 25% vertical grade | **PASSED** |
| **Endurance Hell** | 1000m continuous slight uphill | **PASSED** |
| **Desktop Desert** | 1.5km long-distance reliability | **PASSED** |
| **Variable Friction** | Rapidly changing surface grip | **PASSED** |

## Performance Improvements
Through iterative tuning, the controller achieved significant efficiency gains:
*   **Practice Track Efficiency**: Improved from **2.1x** to **1.5x** ideal energy by refining sprint thresholds and optimizing cruise speeds.
*   **Stall Prevention**: Eliminated deadlocks on 0-speed starts and low-friction inclines.
*   **Time Compliance**: Successfully balanced energy saving with aggressive limits, clearing tight sprints ("Sprint Finish") and long hauls ("Marathon") alike.

## Conclusion
The Eco-Gear Controller represents a robust, adaptive solution capable of handling extreme edge cases (ice, cliffs, endurance) while maintaining a focus on energy minimization. It requires no per-track tuning, making it a truly general-purpose autonomous control system for the Sentry Rover.
