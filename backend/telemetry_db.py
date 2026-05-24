import sqlite3
from pathlib import Path

DB_PATH = Path("data/telemetry.db")


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with connect() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                satellite_id TEXT NOT NULL,
                attitude_error_deg REAL NOT NULL,
                angular_rate_deg_s REAL NOT NULL,
                torque_command_nm REAL NOT NULL,
                battery_percent REAL NOT NULL,
                temperature_c REAL NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                satellite_id TEXT NOT NULL,
                anomaly_type TEXT NOT NULL,
                value REAL NOT NULL,
                limit_value REAL NOT NULL
            )
            """
        )

        conn.commit()


def insert_telemetry(packet):
    with connect() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO telemetry (
                timestamp,
                satellite_id,
                attitude_error_deg,
                angular_rate_deg_s,
                torque_command_nm,
                battery_percent,
                temperature_c
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                packet["timestamp"],
                packet["satellite_id"],
                packet["attitude_error_deg"],
                packet["angular_rate_deg_s"],
                packet["torque_command_nm"],
                packet["battery_percent"],
                packet["temperature_c"],
            ),
        )

        conn.commit()


def insert_anomaly(timestamp, satellite_id, anomaly_type, value, limit_value):
    with connect() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO anomalies (
                timestamp,
                satellite_id,
                anomaly_type,
                value,
                limit_value
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                satellite_id,
                anomaly_type,
                value,
                limit_value,
            ),
        )

        conn.commit()


def get_latest_telemetry():
    with connect() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT t1.timestamp,
                   t1.satellite_id,
                   t1.attitude_error_deg,
                   t1.angular_rate_deg_s,
                   t1.torque_command_nm,
                   t1.battery_percent,
                   t1.temperature_c
            FROM telemetry t1
            INNER JOIN (
                SELECT satellite_id, MAX(timestamp) AS latest_time
                FROM telemetry
                GROUP BY satellite_id
            ) t2
            ON t1.satellite_id = t2.satellite_id
            AND t1.timestamp = t2.latest_time
            ORDER BY t1.satellite_id
            """
        )

        return cursor.fetchall()


def get_recent_anomalies(limit=10):
    with connect() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp,
                   satellite_id,
                   anomaly_type,
                   value,
                   limit_value
            FROM anomalies
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()