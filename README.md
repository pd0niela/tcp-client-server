# TCP client-server
Această aplicație permite comunicarea între mai mulți utilizatori printr-un server central folosind sockets TCP.

## Structura proiectului
Proiectul conține două fișiere principale:
server.py - Scriptul serverului care gestionează conexiunile și mesajele
client.py - Scriptul clientului care permite utilizatorilor să se conecteze și să comunice

# Instalare
Nu sunt necesare biblioteci externe. Aplicația folosește doar biblioteci standard Python.

# Utilizare
Pornirea serverului
Deschideți un terminal și navigați la directorul unde se află fișierul server.py

python server.py

Serverul va porni și va afișa un mesaj confirmând că ascultă pe adresa IP și portul specificate
Pornirea clientului
Deschideți un alt terminal și navigați la directorul unde se află fișierul client.py

python client.py

Pentru a permite conectarea mai multor clienți la server, trebuie să rulezi client.py în terminale diferite. 
Clientul se va conecta la server automat
După conectare, puteți începe să scrieți mesaje

quit - pentru a ieși din aplicație
