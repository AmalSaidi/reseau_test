import socket
import threading

host = '127.0.0.1'
port = 55573

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
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('QUIT'):
                quitting_user = msg.decode('ascii')[5:]
                quit_user(quitting_user)
            elif msg.decode('ascii').startswith('LIST'):
                requesting_user = msg.decode('ascii')[5:]
                liste()
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat !'.encode('ascii'))                                                                                        
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('nickname?'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if nickname == 'amal':
            print("hello admin")
        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of the client is {nickname} !')
        broadcast(f'{nickname} joined the chat! '.encode('ascii'))
        print(f'{nickname}')

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()


def quit_user(nom):
    '''name_index = nicknames.index(nom)
    client_to_quit = clients[name_index]
    clients.remove(client_to_quit)
    client_to_quit.send('you quit the session'.encode('ascii'))
    client_to_quit.close()
    nicknames.remove(nom)
    broadcast(f'{nom} quit the server'.encode('ascii'))'''

def liste():
    print(nicknames)


print("server is listening ...")
receive()
nickname_existing()
