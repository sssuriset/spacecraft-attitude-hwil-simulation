# Control Design

This project uses a proportional-derivative attitude controller to stabilize a simplified 3-axis spacecraft attitude model.

## Control Objective

The control objective is to reduce spacecraft attitude error and angular velocity toward zero.

The attitude state is represented by a small-angle attitude error vector:

```text
theta = [theta_x, theta_y, theta_z]
```

The angular velocity vector is:

```text
omega = [omega_x, omega_y, omega_z]
```

The controller computes a commanded torque vector for the reaction wheels.

## Control Law

The flight software controller uses:

```text
torque = -kp * theta - kd * omega
```

where:

| Symbol | Meaning |
|---|---|
| theta | attitude error vector |
| omega | angular velocity vector |
| kp | proportional gain |
| kd | derivative gain |
| torque | commanded reaction wheel torque |

The proportional term reduces attitude error. The derivative term damps angular velocity.

## Gains Used

The controller currently uses:

```text
kp = 0.8
kd = 2.0
```

These gains were selected to produce stable damping for the simplified spacecraft inertia values used in the simulation.

## Spacecraft Dynamics Model

The simplified rotational dynamics are:

```text
alpha = torque / I
omega = omega + alpha * dt
theta = theta + omega * dt
```

where:

| Symbol | Meaning |
|---|---|
| I | spacecraft moment of inertia vector |
| alpha | angular acceleration |
| dt | simulation timestep |

This model assumes decoupled 3-axis rotational motion. It does not yet include full rigid-body cross-coupling or quaternion kinematics.

## Sensor Model

The flight software does not receive the true state directly. The simulation adds noise to the attitude and angular velocity measurements before sending them to the C controller.

```text
measured_theta = theta + noise
measured_omega = omega + noise
```

This approximates imperfect sensor measurements.

## Actuator Model

The reaction wheel torque command is limited using a saturation model.

```text
torque = clip(torque, -max_torque, max_torque)
```

The current actuator limit is:

```text
max_torque = 0.2 N m
```

This prevents the controller from commanding unrealistic torque values.

## RTOS-Style Control Timing

The control loop is not run continuously. The simulation uses scheduled task rates to approximate real-time flight software behavior.

| Task | Rate | Purpose |
|---|---:|---|
| Sensor task | 100 Hz | Samples noisy attitude and angular velocity measurements |
| Control task | 50 Hz | Calls the C flight software controller |
| Telemetry task | 10 Hz | Logs state, command, and health data |
| Health task | 1 Hz | Checks pointing error and actuator saturation |

The control task uses the most recent sensor packet. This is closer to an embedded flight software pattern than directly evaluating the controller at every simulation line.

## Health Monitoring

The simulation computes pointing error magnitude using:

```text
pointing_error = norm(theta)
```

It also records whether the actuator command reaches the torque limit:

```text
torque_saturated = abs(torque) >= max_torque
```

These values are logged into the telemetry CSV file.

## Result Interpretation

The attitude error plot shows whether the spacecraft points toward the desired attitude. A stable controller should drive all attitude error components toward zero.

The angular velocity plot shows whether rotational motion is being damped. A stable controller should reduce angular velocity toward zero.

The torque command plot shows actuator effort. Saturation events occur when the commanded torque reaches the actuator limit.

The pointing error plot combines all three attitude error components into one scalar metric. A lower final pointing error indicates better final stabilization.

## Current Limitations

This controller is intentionally simple. It is useful for demonstrating GN&C structure and flight software integration, but it is not yet a high-fidelity spacecraft attitude controller.

Main limitations:

- small-angle attitude model
- no quaternion dynamics
- no gyroscope bias estimation
- no actuator delay model
- no reaction wheel momentum storage model
- no full rigid-body coupling