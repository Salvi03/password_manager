import socket
import json
import sys
from cryptography.fernet import Fernet

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if "--add-key" not in sys.argv:
    server_ip = str(input("Inserisci l'ip del server: "))
    port = int(input("Inserisci la porta a cui vuoi connetterti: "))
else:
    print(Fernet.generate_key().decode())
    sys.exit()

if "--add" not in sys.argv and "-a" not in sys.argv:
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, port))
            client.send(json.dumps({
                "decrypt_password": True,
                "choose_password": False
            }).encode())

            print(client.recv(255).decode())

            choice = int(input("Scegli la password da prendere: "))
            key = str(input("Inserisci la chiave per decrittare la tua password: "))

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, port))

            client.send(json.dumps({
                "decrypt_password": False,
                "choose_password": True,
                "password_number": choice
            }).encode())

            if key != "":
                try:
                    print(Fernet(key.encode()).decrypt(client.recv(255)).decode())
                except Exception as e:
                    print(e)
                    sys.exit()
                # decryptor = AES.new(key, AES.MODE_CFB, 'This is an IV456')
                # print(decryptor.decrypt(client.recv(255).decode()).decode())
            else:
                print(client.recv(64).decode())
            sys.exit()
        except Exception as e:
            print(e)
            repeat = str(input("Vuoi continuare?(Y/n) "))
            client.close()
            if repeat == "n":
                break
else:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))

    password = str(input("Inserisci la tua nuova password: "))
    key = str(input("Inserisci chiave per criptare la tua password: "))
    site = str(input("A che sito è legata la tua password? "))
    username = str(input("Inserisci il tuo username: "))

    password = Fernet(key.encode()).encrypt(password.encode()).decode()
    print("First debugging")

    client.send(json.dumps({
        "add": True,
        "key": password,
        "site": site,
        "username": username
    }).encode())

    print(client.recv(255))
