import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/hwil_telemetry_output.csv")

os.makedirs("results", exist_ok=True)

# attitude error plot
plt.figure()
plt.plot(df["time_s"], df["theta_x_rad"], label="theta x")
plt.plot(df["time_s"], df["theta_y_rad"], label="theta y")
plt.plot(df["time_s"], df["theta_z_rad"], label="theta z")
plt.xlabel("Time (s)")
plt.ylabel("Attitude Error (rad)")
plt.title("Spacecraft Attitude Error")
plt.legend()
plt.grid(True)
plt.savefig("results/attitude_error.png", dpi=300)
plt.show()

# angular velocity plot
plt.figure()
plt.plot(df["time_s"], df["omega_x_rad_s"], label="omega x")
plt.plot(df["time_s"], df["omega_y_rad_s"], label="omega y")
plt.plot(df["time_s"], df["omega_z_rad_s"], label="omega z")
plt.xlabel("Time (s)")
plt.ylabel("Angular Velocity (rad/s)")
plt.title("Spacecraft Angular Velocity")
plt.legend()
plt.grid(True)
plt.savefig("results/angular_velocity.png", dpi=300)
plt.show()

# torque command plot
plt.figure()
plt.plot(df["time_s"], df["torque_x_Nm"], label="torque x")
plt.plot(df["time_s"], df["torque_y_Nm"], label="torque y")
plt.plot(df["time_s"], df["torque_z_Nm"], label="torque z")
plt.xlabel("Time (s)")
plt.ylabel("Torque Command (N m)")
plt.title("Reaction Wheel Torque Commands")
plt.legend()
plt.grid(True)
plt.savefig("results/torque_command.png", dpi=300)
plt.show()

# pointing error magnitude plot
plt.figure()
plt.plot(df["time_s"], df["pointing_error_rad"], label="pointing error")
plt.xlabel("Time (s)")
plt.ylabel("Pointing Error Magnitude (rad)")
plt.title("Pointing Error Magnitude")
plt.legend()
plt.grid(True)
plt.savefig("results/pointing_error.png", dpi=300)
plt.show()

print("Plots saved to results folder.")