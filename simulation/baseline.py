import os

import numpy as np
import pandas as pd


DT = 0.1
TOTAL_TIME = 100.0
STEPS = int(TOTAL_TIME / DT)

# Same small-angle model as the HWIL run, without sensor noise or C process I/O.
INERTIA = np.array([10.0, 12.0, 8.0])
KP = 0.8
KD = 2.0

theta = np.array([0.3, -0.2, 0.15])
omega = np.array([0.02, -0.01, 0.015])

rows = []

for i in range(STEPS):
    time_s = i * DT

    torque = -KP * theta - KD * omega

    alpha = torque / INERTIA
    omega = omega + alpha * DT
    theta = theta + omega * DT

    rows.append(
        {
            "time_s": time_s,
            "theta_x_rad": theta[0],
            "theta_y_rad": theta[1],
            "theta_z_rad": theta[2],
            "omega_x_rad_s": omega[0],
            "omega_y_rad_s": omega[1],
            "omega_z_rad_s": omega[2],
            "torque_x_Nm": torque[0],
            "torque_y_Nm": torque[1],
            "torque_z_Nm": torque[2],
        }
    )

os.makedirs("data", exist_ok=True)

df = pd.DataFrame(rows)
df.to_csv("data/baseline_telemetry_output.csv", index=False)

print("Baseline simulation complete.")
print("Telemetry saved to data/baseline_telemetry_output.csv")
print("Final attitude error:")
print(theta)
