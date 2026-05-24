import random
import time

from backend.fleet_status import print_fleet_status
from backend.monitor import TelemetryMonitor
from backend.telemetry_bus import TelemetryBus
from backend.telemetry_db import initialize_database


def make_packet(satellite_id, step):
    base_time = time.time()

    attitude_error_deg = random.uniform(-5.0, 5.0)
    angular_rate_deg_s = random.uniform(-1.5, 1.5)
    torque_command_nm = random.uniform(-0.12, 0.12)
    battery_percent = random.uniform(45.0, 95.0)
    temperature_c = random.uniform(5.0, 35.0)

    if satellite_id == "SAT-2" and step == 6:
        attitude_error_deg = 12.4

    if satellite_id == "SAT-3" and step == 8:
        torque_command_nm = 0.24

    if satellite_id == "SAT-1" and step == 10:
        battery_percent = 24.0

    return {
        "timestamp": base_time + step,
        "satellite_id": satellite_id,
        "attitude_error_deg": attitude_error_deg,
        "angular_rate_deg_s": angular_rate_deg_s,
        "torque_command_nm": torque_command_nm,
        "battery_percent": battery_percent,
        "temperature_c": temperature_c,
    }


def run_demo():
    initialize_database()

    bus = TelemetryBus()
    monitor = TelemetryMonitor(bus)

    satellites = ["SAT-1", "SAT-2", "SAT-3"]

    for step in range(12):
        for satellite_id in satellites:
            packet = make_packet(satellite_id, step)
            bus.publish(packet)

        while monitor.process_next_packet():
            pass

    print_fleet_status()
    print(f"\nProcessed packets: {monitor.processed_packets}")


if __name__ == "__main__":
    run_demo()