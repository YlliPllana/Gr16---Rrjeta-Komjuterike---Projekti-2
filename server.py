import socket
import time
import os
import subprocess

SERVER_IP = 'localhost'
SERVER_PORT = 12345
MAX_CONNECTIONS = 5
QUEUE_SIZE = 10
TIMEOUT = 600
SERVER_FILES_DIR = r"C:\Users\Rinaa\PycharmProjects\Gr16-Rrjeta-Komjuterike-Projekti-2"


FULL_ACCESS = 'FULL'
READ_ONLY = 'READ'

clients = {}

def handle_client(conn, addr, privilege):
    conn.settimeout(TIMEOUT)
    print(f"[NEW CONNECTION] {addr} connected with privilege: {privilege}")

    try:
        while True:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break

            print(f"[{addr}] {msg}")
            with open("server_logs.txt", "a") as log_file:
                log_file.write(f"{time.ctime()} - {addr} - {msg}\n")


            if privilege == FULL_ACCESS:
                if msg.startswith("GET FILES"):
                    files = os.listdir(SERVER_FILES_DIR)
                    file_list = "\n".join(files) if files else "No files available"
                    conn.send(file_list.encode('utf-8'))
                elif msg.startswith("READ FILE "):
                    filename = msg.split(" ", 2)[2]
                    file_path = os.path.join(SERVER_FILES_DIR, filename)
                    if os.path.isfile(file_path):
                        with open(file_path, 'r') as file:
                            conn.send(file.read().encode('utf-8'))
                    else:
                        conn.send(f"File '{filename}' not found.".encode('utf-8'))
                elif msg.startswith("EXEC "):
                    try:
                        command = msg.split(" ", 1)[1]
                        output = subprocess.check_output(command, shell=True)
                        conn.send(output)
                    except Exception as e:
                        conn.send(f"Command failed: {str(e)}".encode('utf-8'))
                else:
                    conn.send("Unknown command.".encode('utf-8'))
            else:
                if msg == "GET FILES":
                    conn.send("Limited access: No file details available.".encode('utf-8'))
                else:
                    conn.send("Read-only access".encode('utf-8'))
    except socket.timeout:
        print(f"[TIMEOUT] {addr} timed out.")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")
        del clients[addr]