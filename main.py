import threading
import tkinter as tk
from server import LogServer
from gui import LogViewerApp


def start_server():
    """
    Start the log server in a separate thread.
    """
    server = LogServer()
    server.start()


if __name__ == "__main__":
    # Start the server in a daemon thread so it closes automatically with the GUI
    threading.Thread(target=start_server, daemon=True).start()

    # Initialize the GUI application
    root = tk.Tk()
    app = LogViewerApp(root)
    root.mainloop()
