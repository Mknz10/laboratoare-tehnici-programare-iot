import socket
import selectors

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"[+] Client conectat: {addr}")
    conn.setblocking(False)  # Socket non-blocant
    sel.register(conn, selectors.EVENT_READ, data=read_wrapper)

def read_wrapper(conn):
    try:
        data = conn.recv(1024)
    except ConnectionResetError:
        data = None

    if data:
        mesaj = data.decode('utf-8').strip()
        print(f"Primit: {mesaj}")
        conn.sendall(data)  # Echo înapoi la client
        if mesaj.lower() == "exit":
            print("[-] Client deconectat (exit)")
            sel.unregister(conn)
            conn.close()
    else:
        print("[-] Client deconectat")
        sel.unregister(conn)
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 5000))
server.listen()
server.setblocking(False)

sel.register(server, selectors.EVENT_READ, data=accept_wrapper)
print("Serverul cu selectors rulează pe 127.0.0.1:5000...")

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
except KeyboardInterrupt:
    print("\nServer oprit.")
finally:
    sel.close()