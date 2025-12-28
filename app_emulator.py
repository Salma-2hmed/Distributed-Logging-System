import threading
import random
import time
import socket
from logger import Logger
from typing import List


class MultiUserSimulator:
    """
    Simulator representing multiple users (devices) sending logs simultaneously
    using a unique mock IP address for each.
    """

    def __init__(self, user_number: int) -> None:
        self.user_number = user_number
        # Get the actual machine hostname
        self.base_hostname = socket.gethostname()

        # Generate a unique mock IP for each user to simulate multiple devices
        # IPs will start from 192.168.1.11, 192.168.1.12, etc.
        self.ip = f"192.168.1.{10 + user_number}"

        # The source string that will appear in the GUI table
        self.device_source = f"({self.ip})"

        # Connect the Logger to the local server address
        self.logger: Logger = Logger(host="127.0.0.1", port=5000)
        self.running: bool = True

    def start_simulating(self) -> None:
        """Send logs for the current user with the defined source format."""
        print(f"[Service Online] {self.device_source} is now simulating logs...")

        while self.running:
            # Randomly select a log level
            level = random.choice(["INFO", "INFO", "WARNING", "ERROR", "CRITICAL"])

            # Realistic technical log messages
            messages = {
                "INFO": ["Connection established", "Ping response: 15ms", "Resource usage: Normal"],
                "WARNING": ["Response time exceeds threshold", "CPU fan speed high"],
                "ERROR": ["Packet loss detected", "Authentication timeout"],
                "CRITICAL": ["Service failure!", "Security breach: multiple failed logins"]
            }

            msg = random.choice(messages[level])

            # Send the log with the unique source (Mock IP)
            self.logger.log(level, msg, self.device_source)

            # Random delay between messages to simulate real user activity
            time.sleep(random.uniform(2, 5))


def run_multi_user_simulation(total_users: int = 5):
    """
    Function to launch multiple users concurrently using Threads.
    """
    print(f"Starting Multi-User Simulation ({total_users} Users)")

    threads = []
    for i in range(1, total_users + 1):
        # Create a simulator instance for each user
        user_sim = MultiUserSimulator(i)
        # Start the simulator in a separate thread
        thread = threading.Thread(target=user_sim.start_simulating, daemon=True)
        threads.append(thread)
        thread.start()

    # Keep the main thread alive until KeyboardInterrupt
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Stopping all simulated users...")


if __name__ == "__main__":
    # Simulate 5 different users or devices
    run_multi_user_simulation(20)