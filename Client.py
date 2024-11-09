import socket


SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Jeni lidhur me serverin.")
    except ConnectionRefusedError:
        print("Nuk u arrit lidhja me serverin. Ju lutemi kontrolloni që serveri është në punë.")
        return

    try:
        while True:

            request = input("Shkruani kërkesën ose 'EXIT' për të dalë: ")
            if request.lower() == 'exit':
                break

            client_socket.send(request.encode('utf-8'))


            try:
                response = client_socket.recv(2048).decode('utf-8')
                print("Përgjigja nga serveri:", response)
            except ConnectionAbortedError:
                print("Serveri refuzoi kërkesën")
                break
            except socket.error as e:
                print(f"Ndodhi një gabim gjatë leximit të përgjigjes: {e}")
                break
    finally:
        client_socket.close()
        print("Klienti u shkëput.")


if __name__ == "__main__":
    start_client()
