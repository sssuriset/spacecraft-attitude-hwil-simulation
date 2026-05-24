# Results

The current run shows the controller reducing the initial pointing error to a small final value.

Representative output:

    Final pointing error: 0.00030531 rad
    Maximum pointing error: 0.40203531 rad
    Torque-limited telemetry samples: 20
    Torque saturation events: 2
    Final health state: OK

The maximum pointing error occurs near the start of the run, where the initial attitude error is largest. The final pointing error is much smaller, which shows that the PD controller damps the initial error in this simplified model.

## Saturation counts

The project reports two saturation metrics.

`torque_limited_sample` counts telemetry samples where the raw controller command exceeded the actuator limit.

`saturation_events_so_far` counts transitions into saturation. This avoids treating every saturated telemetry sample as a separate event.

## Plots

The plot script writes figures to the `results` folder:

    attitude_error.png
    angular_velocity.png
    torque_command_raw.png
    torque_applied.png
    pointing_error.png

The raw torque command plot shows what the controller requested. The applied torque plot shows what the actuator model allowed.

## Interpretation

This run supports the project’s main goal: testing the flow from sensor sampling to C control logic to actuator limiting to telemetry output.

It does not prove high-fidelity spacecraft attitude performance. The model omits quaternion kinematics, coupled rigid-body dynamics, actuator delay, gyroscope bias, and reaction wheel momentum storage.
