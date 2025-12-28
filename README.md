# The Journey of the EcoGear Rover
> Submission by- Tamal Krishna Chhabra (AUP)
---
## The Mission
Imagine you are dropped onto an alien planet. You have a rover, a battery, and a finish line.
Your mission is simple but brutal:
*   Get to the destination before time runs out.
*   Don't waste a single joule of energy.
*   Survive treacherous terrain where one slip means failure.

This project was about building the **Brain** (Controller) for that rover.

## The Thought Process
At first, I tried to tell the rover exactly what to do. "Go speed 5 here," "Gear 2 there."
It failed.
Why? Because the world changes.
*   A flat road becomes a 25% vertical wall.
*   Asphalt turns into ice instantly.

I realized the rover needed to **think**, not just follow orders. It needed to understand the physics of its own existence.

## The Physics Within (How it Works)
I taught the controller to maximize reliability using three core laws of physics:

### 1. The Art of Friction
*   **The Problem:** Spinning wheels burn energy fast and go nowhere.
*   **The Physics:** Traction Limit = $\mu \times Normal Force$.
*   ** The Solution:** The controller "feels" the ground. If it detects ice (Low $\mu$), it drastically cuts torque (Safety Factor 0.25). It treats the throttle like a scalpel, not a hammer.

### 2. The Battle with Drag
*   **The Problem:** Going fast is expensive. Air resistance grows with the square of speed ($v^2$).
*   **The Solution:** I derived the "Golden Speed." This is the exact velocity where Aerodynamic Drag equals Rolling Resistance. Cruising here creates the perfect balance of speed and efficiency.

### 3. Seeing the Future
*   **The Problem:** Hitting a steep hill at slow speed kills your battery.
*   **The Solution:** A 40-meter Look-Ahead system.
*   *See a wall?* Sprint now to carry momentum up.
*   *See a cliff?* Coast early and let gravity do the work.

## The Evolution
My first robust design was a tank—it could go anywhere, but it was hungry.
*   **Initial Practice Run:** 22s time, but **2.1x** the ideal energy.
*   **The Flaw:** It was blindly sprinting on small hills where it didn't need to.

**The Polish:**
*   I taught it to distinguish "Steep" from "Impossible."
*   I added **Adaptive Pacing**: On short tracks, it drives gently. On endless deserts (1km+), it speeds up to beat the clock.
*   **Final Result:** Efficiency improved to **1.5x Ideal**.

## The Gauntlet (Robustness)
To prove the brain was ready, I threw 16 nightmares at it. It conquered every single one.

| Track Name | The Challenge | The Outcome |
| :--- | :--- | :--- |
| **The Wall** | A 25% vertical climb | **PASSED** (Conquered with momentum) |
| **Ice Wall** | Steep AND slippery | **PASSED** (Surgical traction control) |
| **Endurance Hell** | 1000m of uphill grind | **PASSED** (Optimized pacing) |
| **Desktop Desert** | 1.5km marathon | **PASSED** (Reliability test) |
| **Sprint Finish** | Tight time limit | **PASSED** ( aggressive energy dump) |

## What I Learnt
*   **Physics is universal:** A controller based on $F=ma$ works on *any* track. Hardcoded if-statements do not.
*   **Momentum is a battery:** You can "store" energy in your speed. Using a downhill to power an uphill is the ultimate efficiency hack.
*   **Resilience > Speed:** Finishing 1 second early is useless if you burned 50% more fuel.

The final Eco-Gear Controller isn't just a script; it's an adaptive pilot ready for any terrain the simulator throws at it.
