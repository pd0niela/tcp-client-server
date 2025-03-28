#!/usr/bin/env python3
import socket
import threading

# Configurația serverului
HOST = '127.0.0.1'  # Adresa IP a serverului (localhost - adresa locală)
PORT = 5555         # Portul pe care serverul va asculta conexiuni
MAX_CLIENTS = 10    # Numărul maxim de clienți care se pot conecta simultan

# Lista de clienți pentru a urmări conexiunile active
clients = []
clients_lock = threading.Lock()  # Blocaj pentru operațiuni thread-safe pe lista de clienți

def broadcast(message, sender_socket):
    """
    Trimite un mesaj către toți clienții, cu excepția expeditorului
    
    Parametri:
    - message: mesajul de trimis (în format bytes)
    - sender_socket: socket-ul clientului care a trimis mesajul (pentru a nu-i trimite înapoi)
    """
    with clients_lock:  # Blocăm lista de clienți pentru a evita modificări simultane din alte fire de execuție
        for client in clients:
            # Nu trimitem mesajul înapoi la expeditor
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # Dacă trimiterea eșuează, clientul probabil s-a deconectat
                    remove_client(client)

def remove_client(client_socket):
    """
    Elimină un client deconectat din lista de clienți
    
    Parametri:
    - client_socket: socket-ul clientului care trebuie eliminat
    """
    with clients_lock:  # Blocăm lista pentru operațiuni thread-safe
        if client_socket in clients:
            clients.remove(client_socket)
            print(f"Client deconectat. Conexiuni active: {len(clients)}")

def handle_client(client_socket, client_address):
    """
    Gestionează conexiunea individuală a unui client
    
    Această funcție rulează într-un fir separat pentru fiecare client conectat
    
    Parametri:
    - client_socket: socket-ul pentru comunicarea cu clientul
    - client_address: adresa clientului (IP, port)
    """
    print(f"Conexiune nouă de la {client_address}")
    
    # Adăugăm noul client în lista noastră
    with clients_lock:
        clients.append(client_socket)
    
    # Trimitem un mesaj de bun venit clientului
    welcome_msg = "Bun venit la serverul de chat! Tastați 'quit' pentru a ieși.".encode('utf-8')
    client_socket.send(welcome_msg)
    
    # Notificăm ceilalți clienți despre noua conexiune
    join_message = f">>> Utilizatorul de la {client_address[0]}:{client_address[1]} s-a alăturat conversației".encode('utf-8')
    broadcast(join_message, client_socket)
    
    try:
        while True:
            # Primim mesaj de la client
            message = client_socket.recv(1024)
            
            # Dacă clientul s-a deconectat sau a trimis 'quit'
            if not message or message.decode('utf-8').strip().lower() == 'quit':
                break
                
            # Formatăm și difuzăm mesajul către toți ceilalți clienți
            formatted_msg = f"[{client_address[0]}:{client_address[1]}]: {message.decode('utf-8')}".encode('utf-8')
            print(formatted_msg.decode('utf-8'))
            broadcast(formatted_msg, client_socket)
                
    except Exception as e:
        print(f"Eroare la gestionarea clientului {client_address}: {e}")
    
    # Curățăm când clientul se deconectează
    client_socket.close()
    remove_client(client_socket)
    
    # Notificăm ceilalți clienți despre deconectare
    leave_message = f">>> Utilizatorul de la {client_address[0]}:{client_address[1]} a părăsit conversația".encode('utf-8')
    broadcast(leave_message, client_socket)

def start_server():
    """
    Pornește serverul de chat
    
    Această funcție este responsabilă de:
    - Crearea socket-ului TCP
    - Configurarea și inițierea serverului
    - Acceptarea noilor conexiuni
    - Crearea firelor de execuție pentru gestionarea clienților
    """
    # Creăm un socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permitem reutilizarea adresei (util la repornirea serverului)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Asociem socket-ul cu adresa și portul
        server_socket.bind((HOST, PORT))
        
        # Începem să ascultăm conexiuni
        server_socket.listen(MAX_CLIENTS)
        print(f"Serverul a pornit pe {HOST}:{PORT}")
        
        while True:
            # Acceptăm o nouă conexiune
            client_socket, client_address = server_socket.accept()
            
            # Creăm un nou fir de execuție pentru a gestiona clientul
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True  # Firul se va încheia când programul principal se termină
            client_thread.start()
            
            print(f"Conexiuni active: {len(clients)}")
            
    except KeyboardInterrupt:
        print("Serverul se închide...")
    except Exception as e:
        print(f"Eroare: {e}")
    finally:
        # Închidem toate conexiunile clienților
        with clients_lock:
            for client in clients:
                client.close()
        # Închidem socket-ul serverului
        server_socket.close()
        print("Serverul a fost închis")

if __name__ == "__main__":
    start_server()