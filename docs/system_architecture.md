# System Architecture

This project models a spacecraft attitude control system using a hardware-in-the-loop style software structure. The simulation separates the spacecraft plant dynamics from the flight software controller.

## Architecture Overview

The system contains two main components:

1. Python spacecraft simulation
2. C flight software controller

The Python simulation acts as the spacecraft hardware environment. It models the spacecraft attitude state, angular velocity, sensor measurements, actuator limits, and telemetry output.

The C controller acts as flight software. It receives a sensor packet containing attitude error and angular velocity. It computes reaction wheel torque commands using a proportional-derivative control law.

## Data Flow

The simulation follows this sequence:

1. The spacecraft dynamics model stores the true attitude and angular velocity.
2. The sensor task samples the true state and adds simulated measurement noise.
3. The noisy sensor packet is passed to the C flight software controller.
4. The C controller computes torque commands.
5. The actuator model applies torque saturation limits.
6. The spacecraft dynamics model updates the attitude state.
7. Telemetry is logged to a CSV file.
8. Python plotting scripts generate result figures.

## RTOS-Style Task Rates

The simulation uses different task rates to approximate a real-time flight software structure.

| Task | Rate | Period |
|---|---:|---:|
| Sensor task | 100 Hz | 0.01 s |
| Control task | 50 Hz | 0.02 s |
| Telemetry task | 10 Hz | 0.10 s |
| Health task | 1 Hz | 1.00 s |

The plant dynamics are integrated at a 0.01 s timestep. Telemetry is logged separately at 10 Hz.

## HWIL-Style Design

This is not physical hardware-in-the-loop yet. It is a software HWIL-style architecture because the controller is separated from the plant model and communicates through defined inputs and outputs.

The controller does not directly access the true spacecraft state. It only receives sensor-like measurements and returns actuator-like torque commands.

This structure can later be extended to physical HWIL by replacing the Python sensor and actuator interface with serial communication to a microcontroller.