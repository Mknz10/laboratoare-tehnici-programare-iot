import socket
import sys
import time

if len(sys.argv) < 6:
    print("Utilizare: python3 node_ring.py <NUME> <MY_IP> <MY_PORT> <NEXT_IP> <NEXT_PORT> [start]")
    sys.exit(1)

NODE_NAME = sys.argv[1]
MY_HOST = sys.argv[2]
MY_PORT = int(sys.argv[3])
NEXT_HOST = sys.argv[4]
NEXT_PORT = int(sys.argv[5])
IS_STARTER = len(sys.argv) > 6 and sys.argv[6].lower() == "start"

def send_to_next(message):
    """Se conectează la următorul nod din inel și îi transmite mesajul."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((NEXT_HOST, NEXT_PORT))
                client.sendall(message.encode('utf-8'))
                print(f"[{NODE_NAME}] -> Trimis mai departe către {NEXT_HOST}:{NEXT_PORT}: '{message}'")
                break
        except ConnectionRefusedError:
            print(f"[{NODE_NAME}] Aștept ca nodul următor ({NEXT_HOST}:{NEXT_PORT}) să pornească...")
            time.sleep(2)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((MY_HOST, MY_PORT))
    server.listen(5)
    print(f"=== Nodul {NODE_NAME} ascultă pe {MY_HOST}:{MY_PORT} (Următorul: {NEXT_HOST}:{NEXT_PORT}) ===")

    if IS_STARTER:
        mesaj_initial = input(f"[{NODE_NAME}] Introdu mesajul pentru a porni inelul: ")
        traseu_initial = f"{mesaj_initial} | Traseu: {NODE_NAME}"
        send_to_next(traseu_initial)

    while True:
        conn, addr = server.accept()
        with conn:
            data = conn.recv(4096)
            if not data:
                continue

            mesaj_primit = data.decode('utf-8').strip()
            print(f"\n[{NODE_NAME}] <- Primit: '{mesaj_primit}'")

            if IS_STARTER:
                print(f"[{NODE_NAME}] Inel completat cu succes! Mesaj final: {mesaj_primit} -> {NODE_NAME}")
                break
            else:
                mesaj_actualizat = f"{mesaj_primit} -> {NODE_NAME}"
                time.sleep(1)
                send_to_next(mesaj_actualizat)
                break