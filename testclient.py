import socket

# Define server address and port
SERVER_HOST = '192.168.10.11'
SERVER_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Send data to the server
client_socket.sendall("Hello from the client!".encode())

# Receive response from the server
response = client_socket.recv(1024).decode()
print("Server response:", response)

# Close the connection
client_socket.close()
