import socket
import threading


class Server:
    def __init__(self,address,port):
        self.address=address
        self.port=port
        self.clients=dict()
        self.commands="QUIT, CHAT, ABS, BACK , LIST , EDIT , REFUSE , SEND , TELL , STOP , SFIC ,ACCEPT,HELP"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def server_start(self):
        self.server.bind((self.address,self.port))
        self.server.listen()


    def broadcast(self,message):
        for client in self.clients:
            client.send(message.encode())

    def handle(self,client):
        boo = True
        while boo:
            try:
                message = client.recv(1024).decode("ascii")
                commande = message.split(" ")
                #print(client)
                if commande[0] == 'QUIT':
                    print("oof")
                    #client.close()
                    #boo = False
                elif commande[0] == 'LIST':
                    pass

                elif commande[0] == 'HELP':
                    self.liste(client)
                    #self.toString()
                    #requesting_user = message.decode('ascii')
                    #commands_list(requesting_user)
                elif commande[0] == 'EDIT':
                    self.verify_nickname(commande[1],client)
                elif commande[0] == 'CHAT':
                    msg = message.split(" ",1)
                    self.broadcast(self.clients[client] + " : " + msg[1])
                else:
                    client.send('the command was not found'.encode('ascii'))
            except:
                client.close()
                nickname = self.clients[client]
                self.broadcast(f'{nickname} left the chat !')                                                                                        
                del self.clients[client]
                break


    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')
            client.send('nickname?'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            print(nickname)
            self.clients[client] = nickname
            print(f'Nickname of the client is {nickname} !')
            self.broadcast(f'{nickname} joined the chat! ')
            print(f'{nickname}')
            thread = threading.Thread(target=self.handle,args=(client,))
            thread.start()

    def verify_nickname(self,newNick,client):
        if newNick in self.clients.values():
            message=f'{newNick} is already taken'
            client.send(message.encode())
        else:
            self.broadcast(f'{self.clients[client]} is now {newNick}')
            self.clients[client]=newNick




    def liste(self,client):
        #ex=print(*self.commands,sep=", ")
        message=f'{self.commands}'
        client.send(message.encode())




    def commands_list(sock):
        while true:
            mess=sock.recv(1024)
            if mess.decode()=="":
                break
            sock.send(mess.upper())

print("server is listening ...")
serveur = Server('127.0.0.1',9200)
serveur.server_start()
serveur.receive()
serveur.nickname_existing()
