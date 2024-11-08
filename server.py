import socket
import threading
import time
import os
from queue import Queue


SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
MAX_CONNECTIONS = 2
QUEUE_SIZE = 10
TIMEOUT = 600
SERVER_FILES_DIR = "C:\\Users\\yllju\\OneDrive\\Desktop\\RRJETA"

FULL_ACCESS = 'FULL'
READ_ONLY = 'READ'

clients = {}
connection_queue = Queue(maxsize=QUEUE_SIZE)


def handle_client(conn, addr, privilege):
    conn.settimeout(TIMEOUT)
    print(f"[NEW CONNECTION] {addr} connected with privilege: {privilege}")


    try:
        while True:
            try:
                msg = conn.recv(1024).decode('utf-8')
                if not msg:
                    break
            except (ConnectionResetError, socket.timeout):
                print(f"[DISCONNECTED] {addr} disconnected.")
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
                elif msg.startswith("EXEC"):

                        command_parts = msg.split(" ", 2)
                        if len(command_parts) >= 2:
                            if command_parts[1].upper() == "CREATE" and len(command_parts) == 3:

                                filename = command_parts[2]
                                new_file_path = os.path.join(SERVER_FILES_DIR, filename)
                                try:
                                    with open(new_file_path, 'w') as new_file:
                                        new_file.write("This is a new file created by the server.")
                                    conn.send(f"File '{filename}' created successfully.".encode('utf-8'))
                                except Exception as e:
                                    conn.send(f"Error creating file '{filename}': {str(e)}".encode('utf-8'))
                            elif command_parts[1].upper() == "LIST":

                                connected_clients = "\n".join([f"{ip} - {priv}" for ip, priv in clients.items()])
                                response = "Connected users and their privileges:\n" + (
                                    connected_clients if connected_clients else "No users connected.")
                                conn.send(response.encode('utf-8'))
                            else:
                                conn.send("Unknown EXEC command.".encode('utf-8'))
                        else:
                            conn.send("Invalid EXEC command format.".encode('utf-8'))
                elif msg.startswith("WRITE "):

                    try:
                        filename, text = msg.split(" ", 2)[1], msg.split(" ", 2)[2]
                        file_path = os.path.join(SERVER_FILES_DIR, filename)
                        with open(file_path, 'w') as file:
                            file.write(text)
                        conn.send(f"Text written to {filename}".encode('utf-8'))
                    except Exception as e:
                        conn.send(f"Error writing to file: {str(e)}".encode('utf-8'))
                else:
                    conn.send("Unknown command.".encode('utf-8'))
            else:

                if msg == "GET FILES":
                    files = os.listdir(SERVER_FILES_DIR)
                    conn.send("Limited access: No file details available.".encode('utf-8'))
                elif msg.startswith("READ FILE "):
                    filename = msg.split(" ", 2)[2]
                    file_path = os.path.join(SERVER_FILES_DIR, filename)
                    if os.path.isfile(file_path):
                        with open(file_path, 'r') as file:
                            conn.send(file.read().encode('utf-8'))
                    else:
                        conn.send(f"File '{filename}' not found.".encode('utf-8'))
                else:
                    conn.send("Read-only access".encode('utf-8'))


            if not msg.startswith(("GET FILES", "READ FILE", "EXEC", "WRITE")):
                conn.send(msg.encode('utf-8'))

    except socket.timeout:
        print(f"[TIMEOUT] {addr} timed out.")
    except (ConnectionResetError, BrokenPipeError):
        print(f"[DISCONNECTED] {addr} forcefully closed the connection.")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")
        del clients[addr]

        process_next_client_in_queue()

def process_queue():
    while True:
        conn, addr = connection_queue.get()
        if len(clients) < MAX_CONNECTIONS:
            privilege = FULL_ACCESS if len(clients) == 0 else READ_ONLY
            clients[addr] = privilege
            thread = threading.Thread(target = handle_client, args = (conn, addr, privilege)) 
            thread.start()
        else:
            conn.send("Server full, please wait in queue...".encode('utf-8'))
            connection_queue.put((conn, addr))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(MAX_CONNECTIONS)
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}") #inicializimi i serverit

    queue_thread = threading.Thread(target=process_queue, daemon=True)
    queue_thread.start() #process_queue ekzekutohet si background process

    while True:
        conn, addr = server.accept()


        if addr not in clients:
            if len(clients) >= MAX_CONNECTIONS:

                conn.send("Server full, please wait in queue...".encode('utf-8'))
                connection_queue.put((conn, addr))
                print(f"[QUEUED] Connection from {addr} added to the queue.")
            else:

                privilege = FULL_ACCESS if len(clients) == 0 else READ_ONLY
                clients[addr] = privilege
                thread = threading.Thread(target=handle_client, args=(conn, addr, privilege))
                thread.start()

                print(f"[ACTIVE CONNECTIONS] {len(clients)} out of {MAX_CONNECTIONS}")
if __name__ == "__main__":
    start_server()



