import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import socket
import json
import threading
from datetime import datetime


class LogViewerApp:
    """
    A GUI application for viewing and filtering system logs.
    Connects to a local server to fetch log data and displays it in a structured table.
    """

    def __init__(self, root):
        """Initialize the application, styles, and UI components."""
        self.root = root
        self.root.title("LOG SYSTEM")
        self.root.geometry("1150x700")
        self.root.configure(bg="white")

        self.filter_level = tk.StringVar(value="ALL")

        self.setup_styles()
        self.create_ui()

        # Start the automatic data refresh cycle
        self.refresh_loop()

    def setup_styles(self):
        """Configure the look and feel of the Tkinter widgets."""
        style = ttk.Style()
        style.theme_use('clam')

        # Table (Treeview) styling - Light theme colors
        style.configure("Treeview",
                        background="white",
                        foreground="#333333",
                        rowheight=35,
                        fieldbackground="white",
                        borderwidth=1,
                        font=("Segoe UI", 10))

        # Selection styling (Row highlight color)
        style.map("Treeview",
                  background=[('selected', '#e7f1ff')],
                  foreground=[('selected', '#007acc')])

        # Table header styling
        style.configure("Treeview.Heading",
                        background="#f1f3f5",
                        foreground="#495057",
                        relief="flat",
                        padding=10,
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[('active', '#dee2e6')])

        # Button styling (Modern Blue Button)
        style.configure("Action.TButton",
                        foreground="white",
                        background="#007acc",
                        font=("Segoe UI", 9, "bold"),
                        padding=8,
                        borderwidth=0)
        style.map("Action.TButton", background=[('active', '#005fa3')])

    def create_ui(self):
        """Construct the user interface components."""
        # Clean Control Panel (Top Bar)
        top_bar = tk.Frame(self.root, bg="#ffffff", pady=20, padx=25,
                           highlightbackground="#dee2e6", highlightthickness=1)
        top_bar.pack(fill="x")

        # Main Title
        tk.Label(top_bar, text="LOGS", fg="#212529", bg="#ffffff",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=(0, 40))

        # Log Level Filter
        tk.Label(top_bar, text="Level:", fg="#6c757d", bg="#ffffff", font=("Segoe UI", 10)).pack(side="left", padx=5)
        level_menu = ttk.Combobox(top_bar, textvariable=self.filter_level,
                                  values=["ALL", "INFO", "WARNING", "ERROR", "CRITICAL"],
                                  width=12, state="readonly")
        level_menu.pack(side="left", padx=5)

        # Date Range Filter
        tk.Label(top_bar, text="From:", fg="#6c757d", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(20, 5))
        self.start_date = DateEntry(top_bar, width=12, background='#007acc', foreground="white", borderwidth=2)
        self.start_date.pack(side="left", padx=5)

        tk.Label(top_bar, text="To:", fg="#6c757d", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(20, 5))
        self.end_date = DateEntry(top_bar, width=12, background="#007acc", foreground="white", borderwidth=2)
        self.end_date.pack(side="left", padx=5)

        # Manual Refresh Button
        ttk.Button(top_bar, text="REFRESH DATA", style="Action.TButton",
                   command=self.manual_refresh).pack(side="right")

        # Table Container
        table_frame = tk.Frame(self.root, bg="#f8f9fa", padx=25, pady=25)
        table_frame.pack(fill="both", expand=True)

        # Inner frame for table border effect
        inner_frame = tk.Frame(table_frame, bg="white", highlightbackground="#dee2e6", highlightthickness=1)
        inner_frame.pack(fill="both", expand=True)

        # Table Definition
        cols = ("id", "time", "level", "message", "source")
        self.tree = ttk.Treeview(inner_frame, columns=cols, show="headings", style="Treeview")

        col_map = {"id": "ID", "time": "DATE & TIME", "level": "LOG LEVEL", "message": "MESSAGE", "source": "SOURCE"}
        for c in cols:
            self.tree.heading(c, text=col_map[c])
            self.tree.column(c, anchor="center" if c != "message" else "w")

        self.tree.column("id", width=60)
        self.tree.column("time", width=200)
        self.tree.column("level", width=120)
        self.tree.column("message", width=400)
        self.tree.column("source", width=150)

        # Scrollbar integration
        scrolly = ttk.Scrollbar(inner_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrolly.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrolly.pack(side="right", fill="y")

        # Bottom Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Frame(self.root, bg="#ffffff", height=30, highlightbackground="#dee2e6", highlightthickness=1)
        status_bar.pack(side="bottom", fill="x")

        tk.Label(status_bar, textvariable=self.status_var, bg="#ffffff", fg="#6c757d",
                 font=("Segoe UI", 9), padx=15).pack(side="left")

    def manual_refresh(self):
        """Triggered by button click to fetch data immediately."""
        self.status_var.set("Updating log entries...")
        threading.Thread(target=self.fetch_data_task, daemon=True).start()

    def refresh_loop(self):
        """Automatically fetch data every 2 seconds."""
        self.manual_refresh()
        self.root.after(2000, self.refresh_loop)

    def fetch_data_task(self):
        """Background task to request log data from the server via sockets."""
        try:
            request = {
                "action": "FETCH_LOGS",
                "filters": {
                    "level": self.filter_level.get(),
                    "from": self.start_date.get_date().strftime("%Y-%m-%d"),
                    "to": self.end_date.get_date().strftime("%Y-%m-%d")
                }
            }
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect(("127.0.0.1", 5000))
                s.sendall(json.dumps(request).encode())

                data = b""
                while True:
                    chunk = s.recv(8192)
                    if not chunk:
                        break
                    data += chunk

                if data:
                    response = json.loads(data.decode())
                    # Update UI on the main thread
                    self.root.after(0, self._update_table, response["data"])
        except Exception as e:
            # Handle connection errors gracefully
            self.root.after(0, lambda: self.status_var.set(f"Connection Status: Offline ({str(e)})"))

    def _update_table(self, logs):
        """Clear the table and populate it with new log entries."""
        self.tree.delete(*self.tree.get_children())
        for r in logs:
            lvl = r["level"].upper()
            self.tree.insert("", "end", values=(r["id"], r["timestamp"], lvl, r["message"], r["source"]),
                             tags=(lvl.lower(),))

        # text colors for better readability
        self.tree.tag_configure("error", foreground="#d9534f")  # Soft red
        self.tree.tag_configure("critical", foreground="white", background="#d9534f")
        self.tree.tag_configure("warning", foreground="#f0ad4e")  # Soft orange/amber
        self.tree.tag_configure("info", foreground="#5cb85c")  # Soft green

        self.status_var.set(f"Active | Last Sync: {datetime.now().strftime('%H:%M:%S')} | Entries: {len(logs)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LogViewerApp(root)
    root.mainloop()
