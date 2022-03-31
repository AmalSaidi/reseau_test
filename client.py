

import socket
import threading


nickname = input("Choose a nickname : ")

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',9200))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "nickname?":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("an error has occured!")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        commande = message.split(" ",2)
        if commande[1] == "QUIT":
            print("quitting session")
            client.send('QUIT'.encode('ascii'))

        elif commande[1] == "LIST":
            client.send('LIST'.encode('ascii'))

        elif commande[1] == "HELP":
            client.send('HELP'.encode('ascii'))

        elif commande[1] == "EDIT":
            client.send(f'EDIT {commande[2]}'.encode('ascii'))

        elif commande[1] == "CHAT":
            client.send(f'CHAT {commande[2]}'.encode('ascii'))
        else:
            client.send(message.encode('ascii'))
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
