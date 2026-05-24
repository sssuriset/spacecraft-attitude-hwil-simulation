from backend.telemetry_db import get_latest_telemetry, get_recent_anomalies


def print_fleet_status():
    latest_packets = get_latest_telemetry()
    recent_anomalies = get_recent_anomalies(limit=8)

    print("\nFleet Status")
    print("============")

    if not latest_packets:
        print("No telemetry packets stored.")
    else:
        print(
            f"{'Satellite':<12} "
            f"{'Att Err':>9} "
            f"{'Rate':>9} "
            f"{'Torque':>9} "
            f"{'Battery':>9} "
            f"{'Temp':>9}"
        )

        for row in latest_packets:
            (
                timestamp,
                satellite_id,
                attitude_error_deg,
                angular_rate_deg_s,
                torque_command_nm,
                battery_percent,
                temperature_c,
            ) = row

            print(
                f"{satellite_id:<12} "
                f"{attitude_error_deg:>8.2f}° "
                f"{angular_rate_deg_s:>8.2f} "
                f"{torque_command_nm:>8.3f} "
                f"{battery_percent:>8.1f}% "
                f"{temperature_c:>8.1f}C"
            )

    print("\nRecent Anomalies")
    print("================")

    if not recent_anomalies:
        print("No anomalies detected.")
    else:
        print(
            f"{'Satellite':<12} "
            f"{'Type':<24} "
            f"{'Value':>10} "
            f"{'Limit':>10}"
        )

        for row in recent_anomalies:
            timestamp, satellite_id, anomaly_type, value, limit_value = row

            print(
                f"{satellite_id:<12} "
                f"{anomaly_type:<24} "
                f"{value:>10.2f} "
                f"{limit_value:>10.2f}"
            )