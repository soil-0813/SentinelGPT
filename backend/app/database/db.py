import sqlite3
import json
import logging

logger = logging.getLogger(__name__)

DATABASE_NAME = "sentinelgpt.db"


def initialize_database():
    """
    Create all required tables.
    """

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id TEXT PRIMARY KEY,
        attack_type TEXT,
        severity TEXT,
        risk_score INTEGER,
        incident_data TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyst_reports (
        incident_id TEXT,
        report TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executive_summaries (
        incident_id TEXT,
        summary TEXT
    )
    """)

    conn.commit()
    conn.close()

    logger.info("Database initialized successfully")


def save_incident(incident: dict):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO incidents
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        incident["incident_id"],
        incident["attack_type"],
        incident["severity"],
        incident["risk_score"],
        json.dumps(incident)
    ))

    conn.commit()
    conn.close()


def save_analyst_report(
    incident_id: str,
    report: str
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analyst_reports
        VALUES (?, ?)
        """,
        (incident_id, report)
    )

    conn.commit()
    conn.close()


def save_executive_summary(
    incident_id: str,
    summary: str
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO executive_summaries
        VALUES (?, ?)
        """,
        (incident_id, summary)
    )

    conn.commit()
    conn.close()


def get_all_incidents():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM incidents
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data