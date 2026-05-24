import os

import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("data/hwil_telemetry_output.csv")
os.makedirs("results", exist_ok=True)


def save_plot(filename):
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"results/{filename}", dpi=300)
    plt.show()


plt.figure()
plt.plot(df["time_s"], df["theta_x_rad"], label="theta x")
plt.plot(df["time_s"], df["theta_y_rad"], label="theta y")
plt.plot(df["time_s"], df["theta_z_rad"], label="theta z")
plt.xlabel("Time (s)")
plt.ylabel("Attitude error (rad)")
plt.title("Spacecraft attitude error")
save_plot("attitude_error.png")

plt.figure()
plt.plot(df["time_s"], df["omega_x_rad_s"], label="omega x")
plt.plot(df["time_s"], df["omega_y_rad_s"], label="omega y")
plt.plot(df["time_s"], df["omega_z_rad_s"], label="omega z")
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (rad/s)")
plt.title("Spacecraft angular velocity")
save_plot("angular_velocity.png")

plt.figure()
plt.plot(df["time_s"], df["torque_cmd_x_Nm"], label="command x")
plt.plot(df["time_s"], df["torque_cmd_y_Nm"], label="command y")
plt.plot(df["time_s"], df["torque_cmd_z_Nm"], label="command z")
plt.xlabel("Time (s)")
plt.ylabel("Raw torque command (N m)")
plt.title("Controller torque command")
save_plot("torque_command_raw.png")

plt.figure()
plt.plot(df["time_s"], df["torque_applied_x_Nm"], label="applied x")
plt.plot(df["time_s"], df["torque_applied_y_Nm"], label="applied y")
plt.plot(df["time_s"], df["torque_applied_z_Nm"], label="applied z")
plt.xlabel("Time (s)")
plt.ylabel("Applied torque (N m)")
plt.title("Torque after actuator limiting")
save_plot("torque_applied.png")

plt.figure()
plt.plot(df["time_s"], df["pointing_error_rad"], label="pointing error")
plt.xlabel("Time (s)")
plt.ylabel("Pointing error magnitude (rad)")
plt.title("Pointing error magnitude")
save_plot("pointing_error.png")

print("Plots saved to results folder.")
