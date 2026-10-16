import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
    while True:
        message = input("Client: ")
        if not message:
            continue 
        client.sendall(message.encode("utf-8"))
        if message.lower() == "exit":
            break
        data = client.recv(4096)
        if not data:
            print("Server disconnected.")
            break
        response = data.decode("utf-8")
        print(f"Server: {response}")
        if response.lower() == "exit":
            break