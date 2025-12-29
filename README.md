# Distributed Logging System

## Project Overview

This project implements a **Distributed Logging System** where multiple clients send log messages to a central server, and logs can be viewed in a GUI interface. It demonstrates **socket-based communication**, **threaded server handling**, **singleton design pattern**, and **database integration**.

---

## Features

* **LogMessage Class:** Represents log entries with `level`, `message`, `source`, and `timestamp`.
* **Socket-based Logging:** Clients send logs to a central server using TCP sockets.
* **Threaded Server:** The server can handle multiple client connections concurrently.
* **GUI Interface:** Users can view logs in real-time, filter by log level and date.
* **Database Integration:** Logs are stored in a SQL Server database.
* **SOLID Principles:** Each class has a single responsibility.
* **Singleton Logger:** Ensures only one instance of the logger exists.

---

## Project Structure

```
Distributed-Logging-System/
│
├── gui.py              # GUI application to view logs
├── logger.py           # Singleton logger to send logs to the server
├── log_message.py      # Represents a single log entry
├── db_manager.py       # Handles database insert and fetch operations
├── server.py           # Threaded log server
├── main.py             # Starts server and GUI
├── app_simulator.py    # Simulates multiple clients sending logs
└── README.md           # Project documentation
```

---

## Requirements

* Python 3.8+
* Tkinter
* tkcalendar
* pyodbc
* SQL Server with a database named `LoggingDB` and a table `Logs`:

```sql
CREATE TABLE Logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp DATETIME DEFAULT GETDATE(),
    LogLevel VARCHAR(10),
    message TEXT,
    source VARCHAR(50)
);

```

---

## Usage

### 1. Start the Server and GUI

```bash
python main.py
```

* The server runs in a background thread.
* GUI will display logs in real-time with filters for log level and date.

### 2. Simulate Multiple Clients

```bash
python app_simulator.py
```

* Multiple mock clients (e.g., AuthService, PaymentGateway) will send random logs to the server.

### 3. Logging from Other Python Scripts

```python
from logger import Logger

logger = Logger()
logger.log("INFO", "This is a test log", "MyService")
```

---

## Class Overview

* **LogMessage:** Defines the structure of a log entry.
* **Logger:** Singleton class for sending logs to the server.
* **DBManager:** Handles all database operations (insert and fetch).
* **LogServer:** Threaded server to handle multiple clients concurrently.
* **LogViewerApp:** GUI for real-time log display and filtering.
* **MultiClientSimulator:** Simulates multiple services generating logs.

---

## Design Patterns & Principles

* **Singleton Pattern:** Ensures a single instance of Logger across the application.
* **Threading:** Server can handle multiple client connections concurrently.
* **SOLID Principles:** Each class has a clear single responsibility and separation of concerns.

---

## Future Improvements

* Add **authentication** for clients.
* Implement **log archiving and cleanup**.
* Add **advanced filtering and search** in GUI.
* Support **remote deployment
# Distributed-Logging-System
