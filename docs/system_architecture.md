# System Architecture

This project separates the attitude-control test into three parts:

1. Python plant simulation
2. C flight-software logic
3. Telemetry and plotting

The Python side owns the spacecraft state. It stores attitude error, angular velocity, inertia, actuator limits, and sensor noise. Each simulation step advances the plant with the applied torque.

The C controller owns the control law. It receives one sensor packet and returns one raw torque command. During the main run, Python keeps the C controller open as a persistent process instead of launching a new process for every control update.

The C scheduler owns task timing. Python calls the scheduler through a shared library. The scheduler decides when the sensor, control, telemetry, and health tasks are due.

## Main run path

    Python plant -> noisy sensor packet -> C controller -> raw torque command -> actuator limit -> Python plant

The telemetry stores both the raw command and the applied command. That makes actuator saturation visible instead of hiding it inside the plant update.

## C files

`attitude_controller.c` contains the PD control step.

`main.c` provides the controller executable. It supports one-shot command-line use and streaming stdin/stdout use.

`scheduler.c` contains the task timing logic.

`scheduler_test.c` checks the scheduler counts over a short run.

## Python files

`run_hwil.py` is the main simulation.

`baseline.py` is a Python-only reference run without C process I/O or noisy sensors.

`plot.py` reads the main telemetry CSV and writes figures.

## Scheduler behavior

If the loop falls behind, the scheduler skips missed releases instead of replaying them. That matches the simulation goal: one task execution is recorded at the current step, and old missed periods are not replayed.
