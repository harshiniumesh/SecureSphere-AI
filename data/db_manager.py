"""
db_manager.py
Production-quality SQLite database manager for SecureSphere AI.
Handles connection pooling, safe query execution, and schema initialization.
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Any
from contextlib import contextmanager

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
logger = logging.getLogger("SecureSphereDB")
logger.setLevel(logging.INFO)

# Prevent adding multiple handlers if the module is reloaded
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class DatabaseManager:
    """
    Manages SQLite database connections and executes queries safely.
    """

    def __init__(self, db_path: str = "data/securesphere.db"):
        """
        Initializes the DatabaseManager.

        Args:
            db_path (str): The file path to the SQLite database.
        """
        self.db_path = Path(db_path)
        # Ensure the directory exists before attempting to connect
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """
        Context manager for safely acquiring and releasing a database connection.
        Enables dictionary-like access to rows via sqlite3.Row.

        Yields:
            sqlite3.Connection: An active SQLite database connection.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            # Allow rows to be accessed by column name (like dictionaries)
            conn.row_factory = sqlite3.Row
            # Enforce foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def initialize_database(self, schema_path: str = "data/schema.sql") -> None:
        """
        Reads the schema.sql file and executes it to initialize the database tables.

        Args:
            schema_path (str): The file path to the SQL schema file.
        """
        schema_file = Path(schema_path)
        if not schema_file.exists():
            logger.error(f"Schema file not found at: {schema_path}")
            raise FileNotFoundError(f"Schema file not found at: {schema_path}")

        logger.info(f"Initializing database with schema from {schema_path}...")
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_script = f.read()

            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executescript(schema_script)
                conn.commit()
            logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database schema: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during initialization: {e}")
            raise

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """
        Safely executes a single query (e.g., CREATE, DROP, DELETE) without returning data.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameterized values to prevent SQL injection.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e} | Query: {query}")
            raise

    def insert_or_update(self, query: str, params: Tuple[Any, ...] = ()) -> Optional[int]:
        """
        Safely executes an INSERT or UPDATE query and returns the last row ID.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameterized values to prevent SQL injection.

        Returns:
            Optional[int]: The ID of the last inserted row, or None if failed.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error in insert/update: {e} | Query: {query}")
            raise

    def fetch_one(self, query: str, params: Tuple[Any, ...] = ()) -> Optional[sqlite3.Row]:
        """
        Executes a SELECT query and returns a single row.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameterized values to prevent SQL injection.

        Returns:
            Optional[sqlite3.Row]: The retrieved row, or None if no result.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"Error in fetch_one: {e} | Query: {query}")
            raise

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        """
        Executes a SELECT query and returns all matching rows.

        Args:
            query (str): The SQL query string.
            params (tuple): Parameterized values to prevent SQL injection.

        Returns:
            List[sqlite3.Row]: A list of retrieved rows.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error in fetch_all: {e} | Query: {query}")
            raise