import numpy as np
import pandas as pd
import os

# simulation settings
dt = 0.1
total_time = 100.0
steps = int(total_time / dt)

# spacecraft inertia, simplified 3-axis rigid body
I = np.array([10.0, 12.0, 8.0])

# initial attitude error in radians
theta = np.array([0.3, -0.2, 0.15])

# initial angular velocity in rad/s
omega = np.array([0.02, -0.01, 0.015])

# controller gains
kp = 0.8
kd = 2.0

# storage
time_log = []
theta_log = []
omega_log = []
torque_log = []

for i in range(steps):
    t = i * dt

    # PD attitude controller
    torque = -kp * theta - kd * omega

    # angular acceleration
    alpha = torque / I

    # update angular velocity and attitude error
    omega = omega + alpha * dt
    theta = theta + omega * dt

    # log data
    time_log.append(t)
    theta_log.append(theta.copy())
    omega_log.append(omega.copy())
    torque_log.append(torque.copy())

# convert logs to arrays
theta_log = np.array(theta_log)
omega_log = np.array(omega_log)
torque_log = np.array(torque_log)

# create output folder
os.makedirs("data", exist_ok=True)

# save telemetry
df = pd.DataFrame({
    "time_s": time_log,
    "theta_x_rad": theta_log[:, 0],
    "theta_y_rad": theta_log[:, 1],
    "theta_z_rad": theta_log[:, 2],
    "omega_x_rad_s": omega_log[:, 0],
    "omega_y_rad_s": omega_log[:, 1],
    "omega_z_rad_s": omega_log[:, 2],
    "torque_x_Nm": torque_log[:, 0],
    "torque_y_Nm": torque_log[:, 1],
    "torque_z_Nm": torque_log[:, 2],
})

df.to_csv("data/telemetry_output.csv", index=False)

print("Simulation complete.")
print("Telemetry saved to data/telemetry_output.csv")
print("Final attitude error:")
print(theta)