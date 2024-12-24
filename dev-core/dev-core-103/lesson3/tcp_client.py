import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(("localhost",12345))

try:
    messages = ["Hello","How are you?","Hello","Goodbye"]

    for msg in messages:
        client_socket.send(msg.encode("utf-8"))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

finally:
    client_socket.close()