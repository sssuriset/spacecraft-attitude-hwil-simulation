# Spacecraft Attitude HWIL Simulation

This project simulates a spacecraft attitude control system using a hardware-in-the-loop style architecture. The system separates spacecraft dynamics, sensor measurements, actuator commands, scheduled flight software tasks, and telemetry output.

The spacecraft is modeled in Python. The flight software controller is implemented in C. The Python simulation sends sensor-like data to the compiled C controller, receives actuator torque commands, applies actuator limits, and updates the spacecraft attitude state.

## Project Motivation

Spacecraft flight software must operate with noisy sensor data, actuator limits, scheduled control loops, and telemetry constraints. This project models those ideas in a simplified attitude control problem.

The goal is not to model a full spacecraft. The goal is to demonstrate the structure of a GN&C and avionics software workflow.

## Features

- 3-axis spacecraft attitude stabilization model
- C-based flight software attitude controller
- HWIL-style separation between plant dynamics and controller logic
- Sensor noise model
- Reaction wheel torque saturation
- RTOS-style task scheduling
- Health-monitor telemetry
- CSV telemetry output
- Python result plotting

## System Architecture

The system has two main parts:

1. Python spacecraft simulation
2. C flight software controller

The Python simulation models the spacecraft state, sensor noise, actuator limits, and telemetry logging.

The C controller receives a sensor packet containing attitude error and angular velocity. It computes reaction wheel torque commands using a proportional-derivative control law.

## Data Flow

```text
True spacecraft state
        |
        v
Noisy sensor model
        |
        v
C flight software controller
        |
        v
Reaction wheel torque command
        |
        v
Actuator saturation model
        |
        v
Spacecraft dynamics update
        |
        v
Telemetry CSV and plots