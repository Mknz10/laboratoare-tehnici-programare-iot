import socket

HOST = "0.0.0.0"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Server Echo ascultă pe {HOST}:{PORT}...")
    
    conn, addr = server.accept()
    with conn:
        print(f"[+] Client conectat: {addr}")
        while True:
            data = conn.recv(4096)
            if not data:
                print("[-] Client deconectat.")
                break
            
            mesaj = data.decode("utf-8").strip()
            print(f"Primit de la client: {mesaj}")
            
            # Trimitem exact aceleași date înapoi (Echo)
            conn.sendall(data)
            
            if mesaj.lower() == "exit":
                print("[-] Clientul a cerut închiderea conexiunii.")
                break