import ctypes
import os
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / "flight_software" / "ctrl"

DT = 0.01
TOTAL_TIME = 100.0
STEPS = int(TOTAL_TIME / DT)

# Small-angle, decoupled-axis model. This is not full rigid-body attitude motion.
INERTIA = np.array([10.0, 12.0, 8.0])
MAX_TORQUE = 0.2

THETA_NOISE_STD = 0.001
OMEGA_NOISE_STD = 0.0005

POINTING_WARN_RAD = 0.05
POINTING_FAULT_RAD = 0.35


class Scheduler(ctypes.Structure):
    _fields_ = [
        ("sensor_dt", ctypes.c_double),
        ("ctrl_dt", ctypes.c_double),
        ("telem_dt", ctypes.c_double),
        ("health_dt", ctypes.c_double),
        ("next_sensor", ctypes.c_double),
        ("next_ctrl", ctypes.c_double),
        ("next_telem", ctypes.c_double),
        ("next_health", ctypes.c_double),
    ]


def load_scheduler():
    candidates = [
        ROOT / "flight_software" / "libsched.dylib",
        ROOT / "flight_software" / "libsched.so",
    ]

    for candidate in candidates:
        if candidate.exists():
            lib = ctypes.CDLL(str(candidate))
            break
    else:
        raise FileNotFoundError("Build the C scheduler first with: make")

    lib.scheduler_init.argtypes = [ctypes.POINTER(Scheduler)]

    for name in ("due_sensor", "due_control", "due_telemetry", "due_health"):
        fn = getattr(lib, name)
        fn.argtypes = [ctypes.POINTER(Scheduler), ctypes.c_double]
        fn.restype = ctypes.c_int

    return lib


def start_controller():
    if not CONTROLLER.exists():
        raise FileNotFoundError("Build the C controller first with: make")

    return subprocess.Popen(
        [str(CONTROLLER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def controller_step(proc, time_s, theta, omega):
    packet = (
        f"{time_s:.12f} "
        f"{theta[0]:.12f} {theta[1]:.12f} {theta[2]:.12f} "
        f"{omega[0]:.12f} {omega[1]:.12f} {omega[2]:.12f}\n"
    )

    proc.stdin.write(packet)
    proc.stdin.flush()

    line = proc.stdout.readline()

    if not line:
        err = proc.stderr.read()
        raise RuntimeError(f"C controller stopped unexpectedly.\n{err}")

    values = line.strip().split()

    if len(values) != 3:
        raise RuntimeError(f"Bad controller output: {line!r}")

    return np.array([float(value) for value in values])


def health_state(pointing_error, raw_torque, applied_torque):
    saturated = np.any(np.abs(raw_torque - applied_torque) > 1.0e-12)

    if pointing_error >= POINTING_FAULT_RAD:
        return "POINTING_FAULT"

    if saturated:
        return "TORQUE_LIMITED"

    if pointing_error >= POINTING_WARN_RAD:
        return "POINTING_WARN"

    return "OK"


def main():
    scheduler_lib = load_scheduler()
    scheduler = Scheduler()
    scheduler_lib.scheduler_init(ctypes.byref(scheduler))

    controller = start_controller()

    rng = np.random.default_rng(7)

    theta = np.array([0.3, -0.2, 0.15])
    omega = np.array([0.02, -0.01, 0.015])

    measured_theta = theta.copy()
    measured_omega = omega.copy()

    raw_torque = np.zeros(3)
    applied_torque = np.zeros(3)
    current_health = "OK"

    last_saturated = False
    saturation_events = 0

    rows = []

    try:
        for i in range(STEPS):
            time_s = i * DT

            if scheduler_lib.due_sensor(ctypes.byref(scheduler), time_s):
                measured_theta = theta + rng.normal(0.0, THETA_NOISE_STD, 3)
                measured_omega = omega + rng.normal(0.0, OMEGA_NOISE_STD, 3)

            if scheduler_lib.due_control(ctypes.byref(scheduler), time_s):
                raw_torque = controller_step(
                    controller, time_s, measured_theta, measured_omega
                )

                # Actuator limiting is modeled at the plant interface.
                applied_torque = np.clip(raw_torque, -MAX_TORQUE, MAX_TORQUE)

                saturated = np.any(np.abs(raw_torque - applied_torque) > 1.0e-12)

                if saturated and not last_saturated:
                    saturation_events += 1

                last_saturated = saturated

            alpha = applied_torque / INERTIA
            omega = omega + alpha * DT
            theta = theta + omega * DT

            pointing_error = float(np.linalg.norm(theta))

            if scheduler_lib.due_health(ctypes.byref(scheduler), time_s):
                current_health = health_state(pointing_error, raw_torque, applied_torque)

            if scheduler_lib.due_telemetry(ctypes.byref(scheduler), time_s):
                torque_limited = int(
                    np.any(np.abs(raw_torque - applied_torque) > 1.0e-12)
                )

                rows.append(
                    {
                        "time_s": time_s,
                        "theta_x_rad": theta[0],
                        "theta_y_rad": theta[1],
                        "theta_z_rad": theta[2],
                        "omega_x_rad_s": omega[0],
                        "omega_y_rad_s": omega[1],
                        "omega_z_rad_s": omega[2],
                        "torque_cmd_x_Nm": raw_torque[0],
                        "torque_cmd_y_Nm": raw_torque[1],
                        "torque_cmd_z_Nm": raw_torque[2],
                        "torque_applied_x_Nm": applied_torque[0],
                        "torque_applied_y_Nm": applied_torque[1],
                        "torque_applied_z_Nm": applied_torque[2],
                        "pointing_error_rad": pointing_error,
                        "torque_limited_sample": torque_limited,
                        "saturation_events_so_far": saturation_events,
                        "health_state": current_health,
                    }
                )
    finally:
        if controller.stdin:
            controller.stdin.close()

        controller.wait(timeout=2)

    out_dir = ROOT / "data"
    out_dir.mkdir(exist_ok=True)

    df = pd.DataFrame(rows)
    out_file = out_dir / "hwil_telemetry_output.csv"
    df.to_csv(out_file, index=False)

    print("HWIL-style simulation complete.")
    print(f"Telemetry saved to {out_file}")
    print("Final attitude error:")
    print(theta)
    print(f"Final pointing error: {np.linalg.norm(theta):.8f} rad")
    print(f"Maximum pointing error: {df['pointing_error_rad'].max():.8f} rad")
    print(f"Torque-limited telemetry samples: {df['torque_limited_sample'].sum()}")
    print(f"Torque saturation events: {saturation_events}")
    print(f"Final health state: {current_health}")


if __name__ == "__main__":
    main()
