# Control Design

The controller uses a 3-axis PD law.

    torque_cmd = -Kp theta - Kd omega

where:

    theta = measured attitude error
    omega = measured angular velocity
    Kp = 0.8
    Kd = 2.0

The controller is implemented in C. The Python simulation sends measured state values to the C process and reads back the torque command.

## Plant model

The plant uses a small-angle, decoupled-axis rotational model.

    alpha = torque / inertia
    omega_next = omega + alpha dt
    theta_next = theta + omega dt

The inertia vector is:

    [10.0, 12.0, 8.0] kg m^2

This model is valid only as a simplified pointing-error model. It is not a full rigid-body spacecraft attitude model.

## Actuator limiting

The C controller returns a raw command. The Python plant applies the actuator limit.

    torque_applied = clip(torque_cmd, -0.2, 0.2)

Both values are logged.

    torque_cmd_*       raw controller command
    torque_applied_*   command after torque limiting

This makes it possible to see when the controller requested more torque than the actuator model could provide.

## Sensor noise

The sensor task adds Gaussian noise to the plant state before the controller sees it.

    theta noise std = 0.001 rad
    omega noise std = 0.0005 rad/s

The controller does not see the exact plant state.

## Health state

The health task reports one of four states:

    OK
    POINTING_WARN
    POINTING_FAULT
    TORQUE_LIMITED

`TORQUE_LIMITED` is set when the raw command differs from the applied command. `POINTING_WARN` and `POINTING_FAULT` are based on pointing-error thresholds.
