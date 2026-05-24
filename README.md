# Spacecraft Attitude HWIL Simulation

Small attitude-control testbed for a spacecraft pointing problem. Python simulates the plant, sensor noise, actuator limits, and telemetry logging. C handles the control step and task scheduler logic.

This is a software HWIL-style simulation, not a physical hardware-in-the-loop setup. The useful part is the split between plant dynamics, noisy measurements, C flight software logic, actuator limiting, and logged telemetry.

## What it does

The simulation starts with an initial 3-axis attitude error and angular velocity. At fixed task rates, it:

- samples noisy attitude and angular-rate measurements
- sends the measurement packet to a persistent C controller process
- computes a PD torque command in C
- clips the applied torque to model actuator limits
- advances a simplified spacecraft attitude model in Python
- uses a C scheduler library to decide when sensor, control, telemetry, and health tasks run
- writes telemetry to a CSV file
- generates plots for attitude error, angular velocity, raw torque command, applied torque, and pointing error

## Why this project exists

The goal is not to build a full spacecraft ADCS model. The goal is to practice the software structure around one:

- plant simulation
- flight-software control logic
- task-rate scheduling
- telemetry generation
- actuator saturation checks
- health-state reporting

That structure is closer to how spacecraft software is tested than a single script that only plots the dynamics.

## Model

The attitude model is intentionally simple. It uses a small-angle, decoupled 3-axis rotational model.

    alpha = torque / inertia
    omega_next = omega + alpha dt
    theta_next = theta + omega dt

The controller uses a PD law.

    torque_cmd = -Kp theta - Kd omega

The current gains are:

    Kp = 0.8
    Kd = 2.0

The plant applies a torque limit after the C controller returns the raw command. The telemetry stores both values.

    torque_cmd_*       raw controller command
    torque_applied_*   torque after actuator limiting

## Task rates

The scheduler tracks four task rates:

| Task | Period |
|---|---:|
| Sensor | 0.01 s |
| Control | 0.02 s |
| Telemetry | 0.10 s |
| Health | 1.00 s |

The Python simulation calls the C scheduler through a shared library. Missed releases are skipped instead of replayed, so the simulation records one task execution at the current step if the loop falls behind.

## Requirements

Python packages:

- numpy
- pandas
- matplotlib

System tools:

- gcc
- make

On macOS, the default Apple Clang toolchain is fine.

Install Python packages with:

    python3 -m pip install numpy pandas matplotlib

## Run

Build the C controller and scheduler:

    make

Run the HWIL-style simulation:

    python3 simulation/run_hwil.py

Or use:

    make run

Generate plots:

    python3 simulation/plot.py

Or use:

    make plots

Run the simple Python-only baseline:

    make baseline

Run the C controller test:

    make test-ctrl

Run the C scheduler test:

    make test-sched

Clean build outputs:

    make clean

## Outputs

The main simulation writes:

    data/hwil_telemetry_output.csv

The baseline run writes:

    data/baseline_telemetry_output.csv

Plots are saved in:

    results/

Main plot outputs:

    attitude_error.png
    angular_velocity.png
    torque_command_raw.png
    torque_applied.png
    pointing_error.png

## Current result

A representative run gives:

    Final pointing error: 0.00030531 rad
    Maximum pointing error: 0.40203531 rad
    Torque-limited telemetry samples: 20
    Torque saturation events: 2
    Final health state: OK

The torque-limited telemetry samples value counts telemetry samples where the raw controller command exceeded the actuator limit. The torque saturation events value counts transitions into saturation.

## Limitations

This is a compact testbed. It does not include:

- quaternion attitude propagation
- gyroscope bias or drift
- reaction wheel momentum storage
- actuator delay
- coupled rigid-body dynamics
- orbital environment effects
- real hardware or serial I/O

Those omissions are intentional for this version. The current project focuses on control-loop structure, scheduler integration, telemetry, and actuator-limit behavior.
