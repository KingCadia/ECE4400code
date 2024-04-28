import socket

# Define host and port
HOST = '192.168.10.11'  # Localhost
PORT = 12345        # Port to listen on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print("Server is listening on", HOST, "port", PORT)

# Accept incoming connections
client_socket, client_address = server_socket.accept()

print("Connection from", client_address)

# Receive data from the client
data = client_socket.recv(1024).decode()
print("Received:", data)

# Send a response back to the client
client_socket.sendall("Hello from the server!".encode())

# Close the connection
client_socket.close()

# Close the server socket
server_socket.close()
