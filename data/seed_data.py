"""
seed_data.py
Populates the SecureSphere AI database with initial required data.
Includes Scenarios from config and core Learning Center topics.
"""

import uuid
import logging
from typing import List, Dict

# Ensure we import from the root level configuration and data modules
import config
from data.db_manager import DatabaseManager

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
logger = logging.getLogger("SecureSphereSeed")
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def seed_scenarios(db: DatabaseManager) -> None:
    """
    Seeds the predefined scenarios from config.py into the database.
    Prevents duplicate entries by checking the scenario_id.

    Args:
        db (DatabaseManager): The initialized database manager instance.
    """
    logger.info("Seeding Scenarios...")

    for title, details in config.SCENARIOS.items():
        # Create a normalized ID (e.g., "Manufacturing Company" -> "manufacturing_company")
        scenario_id = title.lower().replace(" ", "_")

        # Check if the scenario already exists
        query_check = "SELECT 1 FROM scenarios WHERE scenario_id = ?"
        exists = db.fetch_one(query_check, (scenario_id,))

        if exists:
            logger.info(f"Scenario '{title}' already exists. Skipping.")
            continue

        # Insert the new scenario
        query_insert = """
            INSERT INTO scenarios 
            (scenario_id, title, industry, default_revenue, default_size, critical_asset)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            scenario_id,
            title,
            details["industry"],
            details["annual_revenue"],
            details["employee_count"],
            details["critical_asset"]
        )

        try:
            db.insert_or_update(query_insert, params)
            logger.info(f"Successfully inserted scenario: '{title}'")
        except Exception as e:
            logger.error(f"Failed to insert scenario '{title}': {e}")


def seed_learning_topics(db: DatabaseManager) -> None:
    """
    Seeds the educational topics for the Learning Center into the database.
    Prevents duplicate entries by checking the topic title.

    Args:
        db (DatabaseManager): The initialized database manager instance.
    """
    logger.info("Seeding Learning Topics...")

    topics: List[Dict[str, str]] = [
        {
            "title": "Multi-Factor Authentication",
            "category": "Access Control",
            "description": "A security system that requires more than one method of authentication from independent categories of credentials to verify the user's identity for a login or other transaction.",
            "importance": "Blocks 99% of automated credential stuffing attacks and protects accounts even if a password is breached."
        },
        {
            "title": "Firewalls",
            "category": "Network Security",
            "description": "A network security device that monitors and filters incoming and outgoing network traffic based on an organization's previously established security policies.",
            "importance": "Acts as the first line of defense, separating your secure internal network from untrusted external networks like the Internet."
        },
        {
            "title": "Endpoint Protection",
            "category": "Device Security",
            "description": "Solutions like EDR (Endpoint Detection and Response) that monitor end-user devices (desktops, laptops, mobile devices) to detect and respond to cyber threats.",
            "importance": "Catches sophisticated malware and ransomware that bypass traditional perimeter defenses."
        },
        {
            "title": "Patch Management",
            "category": "Vulnerability Management",
            "description": "The process of distributing and applying updates to software, identifying, acquiring, testing, and installing patches.",
            "importance": "Closes known security holes and exploits before attackers can weaponize them against your infrastructure."
        },
        {
            "title": "Phishing",
            "category": "Social Engineering",
            "description": "A cybercrime in which a target is contacted by email, telephone, or text message by someone posing as a legitimate institution to lure individuals into providing sensitive data.",
            "importance": "It remains the most common initial access vector for enterprise breaches and ransomware deployments."
        },
        {
            "title": "Password Hygiene",
            "category": "Access Control",
            "description": "The practice of creating strong, complex, and unique passwords for every service, alongside the use of secure password managers.",
            "importance": "Prevents lateral movement by attackers and stops attackers from reusing a leaked password across multiple corporate systems."
        },
        {
            "title": "Cloud Security",
            "category": "Infrastructure",
            "description": "A discipline of cybersecurity dedicated to securing cloud computing systems. This includes keeping data private and safe across online infrastructure, applications, and platforms.",
            "importance": "Essential for modern remote work; misconfigured cloud buckets are a leading cause of massive data leaks."
        },
        {
            "title": "Data Backups",
            "category": "Resilience",
            "description": "The practice of copying data from a primary to a secondary location (ideally immutable and off-site) to protect it in case of disaster, accident, or malicious action.",
            "importance": "Often the sole recovery method during a ransomware attack that guarantees business continuity without paying a ransom."
        }
    ]

    for topic in topics:
        # Check if the topic already exists
        query_check = "SELECT 1 FROM learning_topics WHERE title = ?"
        exists = db.fetch_one(query_check, (topic["title"],))

        if exists:
            logger.info(f"Topic '{topic['title']}' already exists. Skipping.")
            continue

        # Insert the new topic
        topic_id = str(uuid.uuid4())
        query_insert = """
            INSERT INTO learning_topics 
            (topic_id, title, category, description, importance)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            topic_id,
            topic["title"],
            topic["category"],
            topic["description"],
            topic["importance"]
        )

        try:
            db.insert_or_update(query_insert, params)
            logger.info(f"Successfully inserted topic: '{topic['title']}'")
        except Exception as e:
            logger.error(f"Failed to insert topic '{topic['title']}': {e}")


def run_seeder() -> None:
    """
    Main function to execute all database seeding operations.
    Initializes the database schema if not present, then populates data.
    """
    try:
        db = DatabaseManager()
        # Ensure the tables exist before seeding
        db.initialize_database()

        logger.info("--- Starting Database Seed Process ---")
        seed_scenarios(db)
        seed_learning_topics(db)
        logger.info("--- Database Seed Process Completed Successfully ---")
    except Exception as e:
        logger.error(f"Seed process failed: {e}")


if __name__ == "__main__":
    run_seeder()