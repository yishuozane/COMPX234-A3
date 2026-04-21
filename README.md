# COMPX234-A3 Tuple Space Client/Server Implementation

## 1. Project Overview
This project implements a multi-threaded server and a synchronous client using TCP sockets in Python to manage a shared "tuple space". The implementation strictly follows the `NNN CMD key value` protocol specified in the assignment brief.

## 2. Design and Implementation Steps
I approached this assignment step-by-step, as reflected in my commit history:

* **Step 1: Basic TCP Setup:** I started by creating the `server.py` and `client.py` files, allowing them to connect via basic TCP sockets using `localhost` and a specified port.
* **Step 2: Client Parsing & Protocol:** I implemented the logic in `client.py` to read the input files line-by-line. I added a constraint check (max 970 chars for key+value) and formatted the requests into the required `NNN R/G/P key value` format. The client waits for a server response before proceeding (synchronous behavior).
* **Step 3: Multi-threaded Server:** To handle concurrent clients, I imported the `threading` module in `server.py`. The main thread runs an infinite loop accepting connections and spawning a new `handle_client` thread for each incoming connection.
* **Step 4: Safe Tuple Space:** I implemented the global dictionary `tuple_space` to store the data. Crucially, I added a `threading.Lock()` (`space_lock`) to ensure thread safety. Every `READ`, `GET`, and `PUT` operation acquires this lock before modifying or reading the dictionary to prevent race conditions.
* **Step 5: Status Reporting:** I created a daemon thread (`report_status`) in the server that wakes up every 10 seconds. It briefly acquires the `space_lock` to calculate the current size of the tuple space, average lengths, and print the global statistics (total operations, errors, etc.) to the console.

## 3. How to Run

1.  **Start the Server:** Open a terminal and run the server with a port number (e.g., 51234).
    ```bash
    python server.py 51234
    ```
2.  **Start the Clients:** Open a separate terminal for each client and run them using the hostname, port, and input file.
    ```bash
    python client.py localhost 51234 client_1.txt
    ```

## 4. Testing Note
The system has been tested concurrently with multiple clients. The server correctly maintains thread safety, prevents duplicate keys on `PUT`, returns errors for missing keys on `READ`/`GET`, and accurately prints the 10-second summary.