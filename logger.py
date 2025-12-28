import socket
import json
from log_message import LogMessage


class Logger:
    """
    Singleton Logger class to handle sending log messages to a central server.
    Captures hostname and IP address automatically.
    """
    _instance = None

    def __new__(cls, host="127.0.0.1", port=5000):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.host = host
            cls._instance.port = port

            # Fetch hostname and IP address once during initialization
            cls._instance.hostname = socket.gethostname()
            cls._instance.ip_address = socket.gethostbyname(cls._instance.hostname)
        return cls._instance

    def log(self, level: str, message: str, source: str = None) -> None:
        """
        Sends a log message to the server.
        If no source is provided, it defaults to the machine's hostname and IP.
        """
        # Default source to Hostname (IP) if not manually specified
        if source is None:
            source = f"{self.hostname} ({self.ip_address})"

        log_msg = LogMessage(level, message, source)
        payload = {
            "action": "LOG",
            "data": log_msg.to_dict()
        }

        try:
            # Create a TCP socket and connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                # Encode and send the JSON payload
                sock.sendall(json.dumps(payload).encode("utf-8"))
        except ConnectionRefusedError:
            print(f"[Logger Error] Connection refused: Is the server running at {self.host}:{self.port}?")
        except Exception as e:
            print(f"[Logger Error] {e}")