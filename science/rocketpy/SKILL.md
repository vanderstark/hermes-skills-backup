---
name: rocketpy
description: "Simulate model rockets: trajectory, motor, stability."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rocketry, simulation, physics, aerospace, education, rocketpy]
    related_skills: [sympy, matplotlib, uncertainty-and-units]
---

# RocketPy — Model Rocket Simulation & Rocketry Fundamentals

RocketPy is an open-source Python library for high-fidelity model/high-power
rocket flight simulation: 6-DOF trajectory, motor thrust curves, stability
margin, apogee prediction, and recovery (parachute) events. This skill covers
both **using RocketPy** and the **underlying physics concepts** for anyone
learning rocketry from scratch (hobby water rockets through solid-motor model
rockets).

## When to use this skill

- User wants to design or simulate a model rocket (water rocket, Estes-style
  motor rocket, high-power rocket)
- User asks about rocket physics: thrust, drag, stability, center of
  gravity/pressure, apogee, parachute deployment
- User wants to predict flight performance (max altitude, velocity, landing
  point) before building
- User is learning rocketry fundamentals and wants a simulator to experiment with

## Installation

```bash
pip install rocketpy
# Optional extras for full functionality (weather data, advanced plotting):
pip install "rocketpy[all]"
```

Verify:
```bash
python3 -c "from rocketpy import Environment, SolidMotor, Rocket, Flight; print('OK')"
```

## Core RocketPy Workflow (4 objects)

1. **Environment** — launch site: location, altitude, atmospheric model (wind, pressure, density by altitude)
2. **Motor** (`SolidMotor`, `HybridMotor`, or `LiquidMotor`) — thrust curve, propellant mass, burn time, nozzle geometry
3. **Rocket** — body geometry (radius, mass, inertia), motor attached, aerodynamic surfaces (nose cone, fins, tail), parachutes
4. **Flight** — combines Environment + Rocket + launch rail conditions, runs the simulation, gives results (apogee, max velocity, out-of-rail speed, landing point, stability margin over time)

### Minimal Example

```python
from rocketpy import Environment, SolidMotor, Rocket, Flight

# 1. Environment — launch site
env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)
env.set_date((2024, 3, 15, 12))  # year, month, day, hour (UTC)
env.set_atmospheric_model(type="standard_atmosphere")

# 2. Motor — example solid motor (replace with real thrust curve/specs)
motor = SolidMotor(
    thrust_source="path/to/thrust_curve.eng",  # or a constant/array
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# 3. Rocket — body + aerodynamics
rocket = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="path/to/drag_curve.csv",
    power_on_drag="path/to/drag_curve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)
rocket.add_motor(motor, position=-1.255)
rocket.set_rail_buttons(0.082, -0.618)

rocket.add_nose(length=0.55829, kind="von karman", position=1.278)
rocket.add_trapezoidal_fins(
    n=3, root_chord=0.120, tip_chord=0.060, span=0.110,
    position=-1.04956, cant_angle=0,
)
rocket.add_parachute(
    "Main", cd_s=10.0, trigger=800,  # deploy at 800m above ground
    sampling_rate=105, lag=1.5,
)
rocket.add_parachute(
    "Drogue", cd_s=1.0, trigger="apogee", sampling_rate=105, lag=1.5,
)

# 4. Flight — run simulation
flight = Flight(rocket=rocket, environment=env, rail_length=5.2,
                 inclination=85, heading=0)

flight.info()          # prints summary: apogee, max speed, stability, etc.
flight.plots.trajectory_3d()
flight.plots.linear_kinematics_data()
```

### Reading Results

```python
print(f"Apogee: {flight.apogee} m")
print(f"Apogee time: {flight.apogee_time} s")
print(f"Max velocity: {flight.max_speed} m/s")
print(f"Out-of-rail velocity: {flight.out_of_rail_velocity} m/s")
print(f"Static margin at liftoff: {rocket.static_margin(0)} calibers")
```

**Static margin** (stability) is in calibers (body diameters). Rule of thumb:
**1.0–2.0 calibers is stable** for most model rockets. Below 1.0 = likely
unstable (will tumble); above 2.5-3.0 = overstable (weathercocks badly in wind).

## Rocketry Fundamentals (for teaching/explaining, not just simulating)

### Water Rockets (simplest — good for absolute beginners)
- Principle: Newton's 3rd law — pressurized air pushes water out the nozzle, reaction thrusts the rocket
- Optimal water fill ratio: **~1/3 of bottle volume** (too much water = heavy/slow, too little = short burn)
- Key build points: fins for stability (center of gravity must be ahead of center of pressure), nose cone for drag reduction, sturdy launcher with pressure release mechanism
- No thrust curve/motor object needed to reason about it, but RocketPy can still model it as a custom low-fidelity thrust profile if the user wants quantitative analysis

### Solid Motor Rockets (Estes/Aerotech class)
- Motor code format: `letter + number + number` (e.g. `C6-5`)
  - Letter = total impulse class (A=2.5 Ns, B=5, C=10, D=20... doubles each letter)
  - First number = average thrust in Newtons
  - Second number = ejection charge delay in seconds (time after burnout before parachute charge fires)
- **Recovery**: parachute/streamer deployed by a timed ejection charge, ideally near apogee
- Thrust curves for real motors: available from **ThrustCurve.org** in `.eng` format, directly loadable into RocketPy's `SolidMotor(thrust_source=...)`

### Stability — Center of Gravity (CG) vs Center of Pressure (CP)
- **CG** must be **ahead of (forward of)** CP for passive aerodynamic stability
- Rule of thumb: CG should be at least **1 body diameter ("1 caliber") ahead of CP**
- CP can be estimated via the **Barrowman equations** (nose shape + fin geometry) — RocketPy computes this automatically from the `add_nose`/`add_trapezoidal_fins` geometry
- Moving mass forward (nose weight) moves CG forward; larger/more-aft fins move CP aft — both increase stability

### Key Physics Concepts to Explain When Asked
- **Thrust**: force from expelling mass (propellant or water) at high velocity — governed by momentum conservation (Tsiolkovsky rocket equation for staged/multi-burn reasoning)
- **Drag**: opposes motion, scales with velocity² and frontal area — minimized by streamlined nose cones and smooth surface finish
- **Apogee**: highest point of flight, occurs when vertical velocity = 0 (before descent/recovery phase)
- **Angle of attack / weathercocking**: wind causes a stable rocket to turn into the wind during ascent, reducing altitude but not causing instability
- **Rail exit velocity**: must be high enough (typically >15 m/s, "rule of thumb 4-6x rail length in calibers of rocket length") for fins to provide effective stabilizing force before leaving the rail

## Safety Notes (always include when discussing real launches)

- Launch only in **large open fields**, clear of power lines, buildings, dry vegetation, and people
- Follow **local model rocketry regulations/club rules** (e.g. national association certification for high-power motors)
- Never attempt to make your own solid propellant/motor — use only commercially manufactured, certified motors
- Water rockets: don't exceed the bottle's rated pressure; use a proper launcher with remote/lanyard trigger, not hand-held

## Common Pitfalls

- **Missing thrust curve file**: `SolidMotor` needs a real `.eng` file or equivalent array — don't invent thrust values; pull from ThrustCurve.org or ask the user for their motor's datasheet
- **Units**: RocketPy is SI-only internally (meters, kg, seconds, Newtons) — convert imperial inputs before passing in
- **Negative/undefined static margin**: if `rocket.static_margin()` returns negative or wildly high values, check `coordinate_system_orientation` consistency between motor and rocket (must match: `"nozzle_to_combustion_chamber"` on motor pairs with `"tail_to_nose"` on rocket, positions measured from the same reference point)
- **Environment date/location**: forecasts require a real future date within API range if `set_atmospheric_model` uses live weather (GFS/NOAA); for historical/offline simulation use `"standard_atmosphere"` to avoid needing internet access

## Related Skills

- `sympy` — for hand-deriving/verifying trajectory equations symbolically
- `matplotlib`/`scientific-visualization` — for custom flight-data plots beyond RocketPy's built-ins
- `uncertainty-and-units` — for propagating measurement uncertainty in flight test analysis (e.g. altimeter reading, wind speed)
