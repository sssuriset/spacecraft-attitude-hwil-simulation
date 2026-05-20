import numpy as np
import pandas as pd
import subprocess
import os

# simulation settings
dt = 0.01
total_time = 100.0
steps = int(total_time / dt)

# RTOS-style task rates
sensor_period = 0.01      # 100 Hz
control_period = 0.02     # 50 Hz
telemetry_period = 0.10   # 10 Hz
health_period = 1.00      # 1 Hz

next_sensor_time = 0.0
next_control_time = 0.0
next_telemetry_time = 0.0
next_health_time = 0.0

# spacecraft inertia, simplified 3-axis rigid body
I = np.array([10.0, 12.0, 8.0])

# simulated sensor noise levels
theta_noise_std = 0.001
omega_noise_std = 0.0005

# actuator torque limit
max_torque = 0.2

# fixed random seed for repeatable simulation results
np.random.seed(7)

# initial attitude error in radians
theta = np.array([0.3, -0.2, 0.15])

# initial angular velocity in rad/s
omega = np.array([0.02, -0.01, 0.015])

# latest sampled sensor values and actuator command
measured_theta = theta.copy()
measured_omega = omega.copy()
torque = np.zeros(3)

# path to compiled C flight software controller
controller_path = "./flight_software/controller_test"

# storage
time_log = []
theta_log = []
omega_log = []
torque_log = []
pointing_error_log = []
torque_saturation_log = []

def call_c_controller(t, theta, omega):
    command = [
        controller_path,
        str(t),
        str(theta[0]),
        str(theta[1]),
        str(theta[2]),
        str(omega[0]),
        str(omega[1]),
        str(omega[2]),
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("C controller failed.")

    torque_values = result.stdout.strip().split()
    torque = np.array([
        float(torque_values[0]),
        float(torque_values[1]),
        float(torque_values[2]),
    ])

    return torque

for i in range(steps):
    t = i * dt

    # sensor task, 100 Hz
    if t >= next_sensor_time:
        measured_theta = theta + np.random.normal(0.0, theta_noise_std, 3)
        measured_omega = omega + np.random.normal(0.0, omega_noise_std, 3)
        next_sensor_time += sensor_period

    # control task, 50 Hz
    if t >= next_control_time:
        torque = call_c_controller(t, measured_theta, measured_omega)
        torque = np.clip(torque, -max_torque, max_torque)
        next_control_time += control_period

    # spacecraft dynamics update, plant integration
    alpha = torque / I
    omega = omega + alpha * dt
    theta = theta + omega * dt

    # health task, 1 Hz
    if t >= next_health_time:
        pointing_error = np.linalg.norm(theta)
        torque_saturated = np.any(np.abs(torque) >= max_torque)
        next_health_time += health_period

    # telemetry task, 10 Hz
    if t >= next_telemetry_time:
        pointing_error = np.linalg.norm(theta)
        torque_saturated = np.any(np.abs(torque) >= max_torque)

        time_log.append(t)
        theta_log.append(theta.copy())
        omega_log.append(omega.copy())
        torque_log.append(torque.copy())
        pointing_error_log.append(pointing_error)
        torque_saturation_log.append(int(torque_saturated))

        next_telemetry_time += telemetry_period

theta_log = np.array(theta_log)
omega_log = np.array(omega_log)
torque_log = np.array(torque_log)

os.makedirs("data", exist_ok=True)

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
    "pointing_error_rad": pointing_error_log,
    "torque_saturated": torque_saturation_log,
})

df.to_csv("data/hwil_telemetry_output.csv", index=False)

print("HWIL-style simulation complete.")
print("Telemetry saved to data/hwil_telemetry_output.csv")
print("Final attitude error:")
print(theta)
print(f"Final pointing error: {np.linalg.norm(theta):.8f} rad")
print(f"Maximum pointing error: {max(pointing_error_log):.8f} rad")
print(f"Torque saturation events: {sum(torque_saturation_log)}")