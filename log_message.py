from datetime import datetime
from typing import Dict


class LogMessage:
    """Represents a log message with level, source, and timestamp."""

    def __init__(self, level: str, message: str, source: str) -> None:
        """
        Initialize a log message.

        Args:
            level (str): Log level (e.g., INFO, ERROR).
            message (str): Log message content.
            source (str): Source of the log message.
        """
        self.level: str = level.upper()
        self.message: str = message
        self.source: str = source
        self.timestamp: datetime = datetime.now()

    def to_dict(self) -> Dict[str, str]:
        """
        Convert the log message to a dictionary suitable for JSON or DB insertion.

        Returns:
            dict: Log message data.
        """
        return {
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }