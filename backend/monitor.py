from backend.telemetry_db import insert_telemetry, insert_anomaly


ATTITUDE_ERROR_LIMIT_DEG = 8.0
ANGULAR_RATE_LIMIT_DEG_S = 2.5
TORQUE_LIMIT_NM = 0.18
BATTERY_LOW_LIMIT_PERCENT = 30.0
TEMPERATURE_HIGH_LIMIT_C = 45.0
TEMPERATURE_LOW_LIMIT_C = -10.0


class TelemetryMonitor:
    def __init__(self, bus):
        self.bus = bus
        self.processed_packets = 0

    def process_next_packet(self):
        packet = self.bus.consume()

        if packet is None:
            return False

        insert_telemetry(packet)
        self.check_anomalies(packet)
        self.processed_packets += 1

        return True

    def check_anomalies(self, packet):
        timestamp = packet["timestamp"]
        satellite_id = packet["satellite_id"]

        if abs(packet["attitude_error_deg"]) > ATTITUDE_ERROR_LIMIT_DEG:
            insert_anomaly(
                timestamp,
                satellite_id,
                "attitude_error_limit",
                packet["attitude_error_deg"],
                ATTITUDE_ERROR_LIMIT_DEG,
            )

        if abs(packet["angular_rate_deg_s"]) > ANGULAR_RATE_LIMIT_DEG_S:
            insert_anomaly(
                timestamp,
                satellite_id,
                "angular_rate_limit",
                packet["angular_rate_deg_s"],
                ANGULAR_RATE_LIMIT_DEG_S,
            )

        if abs(packet["torque_command_nm"]) > TORQUE_LIMIT_NM:
            insert_anomaly(
                timestamp,
                satellite_id,
                "torque_saturation",
                packet["torque_command_nm"],
                TORQUE_LIMIT_NM,
            )

        if packet["battery_percent"] < BATTERY_LOW_LIMIT_PERCENT:
            insert_anomaly(
                timestamp,
                satellite_id,
                "battery_low",
                packet["battery_percent"],
                BATTERY_LOW_LIMIT_PERCENT,
            )

        if packet["temperature_c"] > TEMPERATURE_HIGH_LIMIT_C:
            insert_anomaly(
                timestamp,
                satellite_id,
                "temperature_high",
                packet["temperature_c"],
                TEMPERATURE_HIGH_LIMIT_C,
            )

        if packet["temperature_c"] < TEMPERATURE_LOW_LIMIT_C:
            insert_anomaly(
                timestamp,
                satellite_id,
                "temperature_low",
                packet["temperature_c"],
                TEMPERATURE_LOW_LIMIT_C,
            )