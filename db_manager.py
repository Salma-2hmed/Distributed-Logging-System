import pyodbc
from typing import List, Any, Dict


class DBManager:
    """Database manager for inserting and fetching log entries."""

    def __init__(self, conn_str: str) -> None:
        """
        Initialize the DBManager with a connection string.

        Args:
            conn_str (str): The ODBC connection string.
        """
        self.conn_str = conn_str

    def insert_log(self, log: Dict[str, Any]) -> None:
        """
        Insert a log entry into the Logs table.

        Args:
            log (dict): Log data with keys 'level', 'message', 'source', 'timestamp'.
        """
        query = """
        INSERT INTO Logs (LogLevel, message, source, timestamp)
        VALUES (?, ?, ?, ?)
        """
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query,
                    log["level"],
                    log["message"],
                    log["source"],
                    log["timestamp"]
                )
                conn.commit()
        except pyodbc.Error as e:
            print(f"[DB Error] Failed to insert log: {e}")

    def fetch_logs(self, level: str, start: str, end: str) -> List[Any]:
        """
        Fetch logs from the Logs table based on level and date range.

        Args:
            level (str): Log level to filter (use "ALL" for no filtering).
            start (str): Start date (YYYY-MM-DD).
            end (str): End date (YYYY-MM-DD).

        Returns:
            List[Any]: List of rows fetched from the database.
        """
        query = """
        SELECT TOP 100 id, timestamp, LogLevel, message, source
        FROM Logs
        WHERE CAST(timestamp AS DATE) BETWEEN ? AND ?
        """
        params = [start, end]

        if level.upper() != "ALL":
            query += " AND LogLevel = ?"
            params.append(level)

        query += " ORDER BY id DESC"

        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"[DB Error] Failed to fetch logs: {e}")
            return []