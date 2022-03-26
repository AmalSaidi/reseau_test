import socket
import threading

host = '127.0.0.1'
port = 55571

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []


def nickname_existing():
    if nickname in nicknames:
        print('nickname already exists')

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            if(message=="hi"):
                print("welcomeee !")
        except:
            index = clients.index(client)
            cliens.remove(client)
            client.close()
            nickname = nickname[index]
            broadcast(f'{nickname} left the chat !'.encode('ascii'))                                                                                        
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Conncted with {str(address)}')

        #client.send('NICk'.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of the client is {nickname} !')
        broadcast(f'{nickname} joined the chat! '.encode('ascii'))
        print(f'{nickname}')

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("server is listening ...")
receive()
nickname_existing()