import socket
import threading
import random
import json

# Sample themes with descriptions
themes = [
    {"name": "Y2K", "description": "A futuristic late-90s aesthetic with metallics and cyber vibes."},
    {"name": "Cottagecore", "description": "Soft rural fashion, full of nature, flowers, and linen dresses."},
    {"name": "Futuristic", "description": "High-tech vibes with shiny, sleek, space-inspired looks."},
    {"name": "Kidcore", "description": "Playful and colorful, like childhood joy and cartoons."},
    {"name": "Glamorous", "description": "Elegant, sparkling, and red-carpet ready fashion."}
]

HOST = '127.0.0.1'
PORT = 65432

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        request = conn.recv(1024).decode()
        if request == "GET_THEME":
            selected = random.choice(themes)
            conn.sendall(json.dumps(selected).encode())
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start_server():
    print("[SERVER STARTED]")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
