# Results

This document summarizes the main simulation outputs from the spacecraft attitude HWIL simulation.

## Simulation Summary

The HWIL-style simulation connects a Python spacecraft dynamics model to a C flight software controller. The controller receives noisy sensor measurements and returns reaction wheel torque commands. The Python simulation applies actuator saturation, updates the spacecraft attitude state, and logs telemetry.

The simulation includes:

- noisy attitude and angular velocity measurements
- C-based proportional-derivative attitude control
- reaction wheel torque saturation
- RTOS-style task scheduling
- telemetry logging
- health-monitor values

## Terminal Output

A representative simulation run produced:

```text
Final pointing error: 0.00015004 rad
Maximum pointing error: 0.40203901 rad
Torque saturation events: 20
```

The final pointing error is much smaller than the initial pointing error. This indicates that the controller stabilized the spacecraft attitude.

The maximum pointing error occurs near the beginning of the simulation because the spacecraft starts with a nonzero attitude error and angular velocity.

The torque saturation count shows how many telemetry samples recorded actuator commands at the torque limit.

## Attitude Error

The attitude error plot shows the three components of the attitude error vector over time.

A stable response should show all three components damping toward zero. In the simulation, the attitude error initially oscillates because the controller is correcting both the attitude error and the angular velocity. The oscillations decrease over time as the derivative term damps the motion.

## Angular Velocity

The angular velocity plot shows the rotational rate of the spacecraft about each axis.

A successful stabilization response should reduce angular velocity toward zero. In the simulation, the angular velocity components decay as the controller applies opposing torque commands.

## Reaction Wheel Torque Commands

The torque command plot shows the commanded actuator torque for each axis.

The initial torque commands are larger because the attitude error and angular velocity are largest near the start of the run. As the spacecraft stabilizes, the torque commands decrease toward zero.

Torque saturation occurs when the controller requests more torque than the actuator limit allows. The actuator model clips the command to the maximum allowed value.

## Pointing Error Magnitude

The pointing error magnitude combines the three attitude error components into one scalar value.

```text
pointing_error = norm(theta)
```

This metric is useful because it gives one value for the total attitude error. The final pointing error is small, which indicates that the controller successfully stabilized the spacecraft.

## Interpretation

The results show that the simulated spacecraft reaches a stable attitude despite noisy sensor measurements and actuator torque limits.

The project demonstrates the software structure of a GN&C and avionics workflow rather than a high-fidelity spacecraft dynamics model. The main result is the successful integration of:

- a simulated spacecraft plant
- noisy sensor packets
- C flight software control logic
- actuator saturation
- scheduled task execution
- telemetry and health monitoring

## Limitations

The results should be interpreted within the assumptions of the model. The simulation uses a simplified small-angle attitude model and decoupled axis dynamics. It does not yet include full quaternion kinematics, gyroscope bias estimation, actuator delay, or reaction wheel momentum storage.

These limitations are documented so that future versions can extend the simulation toward higher-fidelity spacecraft attitude control.