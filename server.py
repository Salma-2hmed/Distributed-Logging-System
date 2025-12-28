import socket
import threading
import json
from db_manager import DBManager


class LogServer:
    """A multi-threaded logging server for log insertion and retrieval."""

    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        # SQL Server connection string using ODBC Driver 17
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=LoggingDB;"
            "Trusted_Connection=yes;"
        )
        # Initialize Database Manager
        self.db = DBManager(self.conn_str)
        # Initialize TCP/IP Socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of the port after server restart
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        """Bind the socket and start listening for incoming client connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server running and protected on {self.host}:{self.port}...")

        while True:
            # Accept new client connection
            client_socket, _ = self.server_socket.accept()
            # Start a new thread for each client to enable concurrency
            threading.Thread(
                target=self.handle_client,
                args=(client_socket,),
                daemon=True
            ).start()

    def handle_client(self, client_socket):
        """Handle incoming requests from a specific client."""
        with client_socket:
            try:
                # Retrieve the full data payload from the socket
                data = self.receive_full_data(client_socket)
                if not data:
                    return

                # Parse JSON request
                request = json.loads(data.decode())
                action = request.get("action")

                # Branch logic based on the requested action
                if action == "LOG":
                    # Insert a new log entry into the database
                    self.db.insert_log(request.get("data"))

                elif action == "FETCH_LOGS":
                    # Retrieve logs based on provided filters (level, date range)
                    filters = request.get("filters", {})
                    rows = self.db.fetch_logs(
                        filters.get("level"),
                        filters.get("from"),
                        filters.get("to")
                    )

                    # Construct the JSON response structure
                    response = {
                        "status": "OK",
                        "data": [
                            {
                                "id": row[0],
                                "timestamp": str(row[1]),
                                "level": row[2],
                                "message": row[3],
                                "source": row[4],
                            }
                            for row in rows
                        ],
                    }
                    # Send response back to the client
                    client_socket.sendall(json.dumps(response).encode())

            except Exception as e:
                print(f"Server Error during client handling: {e}")

    def receive_full_data(self, sock, buffer_size=4096):
        """Receive all data from the client socket until the transmission is complete."""
        data = b""
        while True:
            chunk = sock.recv(buffer_size)
            if not chunk:
                break
            data += chunk
            # If the chunk is smaller than buffer, it's likely the end of the message
            if len(chunk) < buffer_size:
                break
        return data


if __name__ == "__main__":
    # Instantiate and start the server
    server = LogServer()
    server.start()
