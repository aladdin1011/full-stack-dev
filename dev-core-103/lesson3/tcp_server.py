import  socket

ALLOWED_IP_RANGE = "127.0.0.1"

def check_ip_allowed(client_ip):
    return client_ip == ALLOWED_IP_RANGE

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("localhost",12345))
server_socket.listen(5)
print("Server is listening on port 12345")

while True:
    client_socket, address = server_socket.accept()
    client_ip = address[0]

    if not check_ip_allowed(client_ip):
        print(f"Connection from {client_ip} rejected.")
        client_socket.close()
        continue
    
    print(f"Connection accepted from {client_ip}")

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Received message from {client_ip}: {message}")

            if message == "Hello":
                response = "Welcome, user"
            else:
                response = "Unknown command"
            
            client_socket.send(response.encode("utf-8"))
        except Exception as e:
            print(f"Error: {e}")
            break
    print(f"Closing connection with {client_ip}")
    client_socket.close()

