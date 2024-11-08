import socket


SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Jeni lidhur me serverin.")

    try:
        while True:

            request = input("Shkruani kerkesen ose 'EXIT' per te dale: ")
            if request.lower() == 'exit':
                break

            client_socket.send(request.encode('utf-8'))
            response = client_socket.recv(2048).decode('utf-8')
            print("Pergjigja nga serveri:", response)
    finally:
        client_socket.close()
        print("Klienti u shkëput.")


if __name__ == "__main__":
    start_client()
