#!/usr/bin/env python3
import socket
import threading
import sys

# Detaliile conexiunii la server
HOST = '127.0.0.1'  # Adresa IP a serverului (localhost - adresa locală)
PORT = 5555         # Portul serverului pentru comunicare

def receive_messages(client_socket):
    """
    Funcție care primește continuu mesaje de la server și le afișează utilizatorului
    
    Această funcție rulează într-un fir de execuție separat și este responsabilă pentru:
    - Primirea mesajelor de la server
    - Afișarea mesajelor primite
    - Gestionarea deconectărilor sau erorilor de comunicare
    """
    try:
        while True:
            # Primim mesajul de la server (maxim 1024 bytes)
            message = client_socket.recv(1024)
            
            # Dacă nu primim niciun mesaj, înseamnă că serverul s-a deconectat
            if not message:
                print("Conexiunea cu serverul a fost pierdută")
                break
                
            # Afișăm mesajul primit (decoding din bytes în text)
            print(message.decode('utf-8'))
    except Exception as e:
        # Afișăm orice eroare apărută în timpul primirii mesajelor
        print(f"Eroare la primirea mesajelor: {e}")
    finally:
        # Închidem socket-ul în caz de eroare sau deconectare
        client_socket.close()
        print("Deconectat de la server")
        sys.exit(0)  # Ieșim din program

def start_client():
    """
    Funcția principală care inițiază și gestionează clientul de chat
    
    Această funcție este responsabilă pentru:
    - Crearea conexiunii cu serverul
    - Inițierea firului de execuție pentru primirea mesajelor
    - Gestionarea introducerii și trimiterii mesajelor de la utilizator
    - Gestionarea deconectărilor și erorilor
    """
    try:
        # Creăm un socket TCP (SOCK_STREAM) pentru comunicare
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectare la server
        print(f"Se conectează la serverul {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Conectat la server")
        
        # Inițiem firul de execuție pentru primirea mesajelor
        # Acest fir va rula în paralel cu firul principal
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True  # Firul se va încheia când programul principal se termină
        receive_thread.start()
        
        # Bucla principală pentru trimiterea mesajelor
        while True:
            # Așteptăm introducerea unui mesaj de la utilizator
            message = input()
            
            # Trimitem mesajul la server (encoding din text în bytes)
            client_socket.send(message.encode('utf-8'))
            
            # Dacă utilizatorul tastează 'quit', ieșim din buclă
            if message.strip().lower() == 'quit':
                break
    except ConnectionRefusedError:
        # Eroare specifică când serverul nu acceptă conexiunea
        print("Nu s-a putut conecta la server. Asigurați-vă că serverul este pornit.")
    except KeyboardInterrupt:
        # Capturăm întreruperea de la tastatură (Ctrl+C)
        print("Clientul se închide...")
    except Exception as e:
        # Capturăm orice altă eroare
        print(f"Eroare: {e}")
    finally:
        # Închidem întotdeauna socket-ul, indiferent de situație
        client_socket.close()
        print("Deconectat de la server")

# Punct de intrare în program
# Verificăm dacă scriptul este rulat direct (nu importat ca modul)
if __name__ == "__main__":
    start_client()