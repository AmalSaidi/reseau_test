import socket
import threading


class Server:
    def __init__(self,address,port):
        self.address=address
        self.port=port
        self.clients=dict()
        self.private=dict()
        self.request=dict()
        self.away=[]
        self.commands=["QUIT","CHAT","ABS","BACK","LIST","EDIT","REFUSE","SEND","TELL","STOP","SFIC","ACCEPT","HELP"]
        self.definitions=["logout the user","send a message publically","Changes the state of the user from abs to away"]
        #self.com = [["quit","LOGOUT THE USER"],["CHAT","blabla"]]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def server_start(self):
        self.server.bind((self.address,self.port))
        self.server.listen()


    def broadcast(self,message):
        for client in self.clients:
            client.send(message.encode())

    def handle(self,client):
        boo = True
        bof=False
        while boo:
            try:
                message = client.recv(1024).decode("ascii")
                commande = message.split(" ",2)
                commande_de_tell = message.split(" ",3)
                #print(client)
                if commande[1] == 'QUIT':
                    self.quit(client)
                    boo = false
                elif commande[1] == 'LIST':
                    self.liste_clients(client)

                elif commande[1] == 'HELP':
                    self.liste_commandes(client)

                elif commande[1] == 'EDIT':
                    self.verify_nickname(commande[2],client)
                
                elif commande_de_tell[1] == 'TELL':
                    self.tell(commande_de_tell[2],commande_de_tell[3],client)
                    


                elif commande[1] == 'CHAT':
                    msg = message.split(" ",1)
                    self.broadcast("200 : " + self.clients[client] + " : " + commande[2])

                elif commande[1] == 'STOP':
                    self.stop(commande[2],client)

                elif commande[1] == 'SEND':
                    print(f'mon tableau: {commande} et sa taille: {len(commande)}')

                    if len(commande) < 3:
                        client.send("418 ! Missing parameter".encode())
                    elif commande[2] == " ":
                        client.send("418 : Missing parameter".encode())
                    else:
                        self.send(client,commande[2])

                elif commande[1] == 'REFUSE':
                    if len(commande) < 3:
                        client.send("Missing parameter".encode())
                    elif commande[2] == '':
                        client.send("Missing parameter".encode())
                    else:
                        self.refuse(client,commande[2])


                elif commande[1] == 'CONNECT':
                    pass

                elif commande[1] == 'ABS':
                    self.absent(client)

                elif commande[1] == 'BACK':
                    message="418 : You are already online"
                    client.send(message.encode())
                    
                elif commande[1] == 'ACCEPT':
                    if len(commande) < 3:
                        client.send("Missing parameter".encode())
                    elif commande[2] == '':
                        client.send("Missing parameter".encode())
                    else:
                        self.accept(client,commande[2])


                elif commande[1] == 'SFIC':
                    self.send_file(client)

                else:
                    client.send('404 : the command was not found'.encode('ascii'))
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
            self.clients[client] = nickname
            print(f'Nickname of the client is {nickname} !')
            self.broadcast(f'{nickname} joined the chat! ')
            self.etat=True              
        
            thread = threading.Thread(target=self.handle,args=(client,))
            thread.start()

    def absent(self,client):
        self.broadcast(f'200 : {self.clients[client]} is now away')
        self.away.append(self.clients[client])
        while True:
            try:
                next_msg = client.recv(1024).decode("ascii")
                nxt = next_msg.split(" ",2)
                if nxt[1] == 'BACK':
                    self.broadcast(f'200 : {self.clients[client]} is back')
                    break
                elif nxt[1] == "ABS":
                    message="417 : You are already away"
                    client.send(message.encode())
                elif nxt[1] == "CHAT":
                    message="403 : you can't send messages"
            except:
                print("an error")

        
    def send(self,client,receiver):
        print("here")
        if receiver in self.clients.values():
            if receiver == self.clients[client]:
                message = f"{self.clients[client]} is you, you can't have a private chat with yourself"
                client.send(message.encode())
            else:
                for key, valeur in self.clients.items(): 
                    if receiver == valeur: 
                        receiver_sock = key
                        thread = threading.Thread(target=self.handle,args=(receiver_sock,))
                        thread.start()
                        message = f"{self.clients[client]} wants to have a private a chat with you.respond with ACCEPT to accept the request or REFUSE to refuse"
                        receiver_sock.send(message.encode())
                receiver_sock.send(message.encode())
                print(self.clients[client])
                print(self.clients[receiver_sock])

        else:
            print(f"408 {receiver} doesn't exist")
            message = f"408 {receiver} doesn't exist"
            client.send(message.encode())
        

    def refuse(self,client_to_respond,client_receiving_response):
        if client_receiving_response in self.clients.values():
            if client_receiving_response == self.clients[client_to_respond]:
                message = f"{self.clients[client_to_respond]} you can't use this command to yourself"
                client_to_respond.send(message.encode())
                
            else:
                message = f"200 : {self.clients[client_to_respond]} refused to have a private chat with you."
                message2 = f"200 : you refused the private chat from {client_receiving_response}"
                for key, valeur in self.clients.items(): 
                    if client_receiving_response == valeur: 
                        client_receiving_response_sock = key
                        #print(self.private)
                        #print(self.clients[client_to_respond])
                        #print(client_receiving_response)
                client_receiving_response_sock.send(message.encode())
                client_to_respond.send(message2.encode())
        else:
            print(f"408 {client_receiving_response} doesn't exist")
            message = f"408 {client_receiving_response} doesn't exist"
            client_to_respond.send(message.encode())
            

        

    def accept(self,client_to_respond,client_receiving_response):
        if client_receiving_response in self.clients.values():
            if client_receiving_response == self.clients[client_to_respond]:
                message = f"{self.clients[client_to_respond]} is you, that means you can't use this command to yourself"
                client_to_respond.send(message.encode())
                
            else:
                message = f"{self.clients[client_to_respond]} accepted to have a private chat with you."
                for key, valeur in self.clients.items(): 
                    if client_receiving_response == valeur: 
                        client_receiving_response_sock = key
                        self.private[client_to_respond] = self.clients[client_to_respond]
                        self.private[client_receiving_response_sock] = self.clients[client_receiving_response_sock]
                        #print(self.private)
                        #print(self.clients[client_to_respond])
                        #print(client_receiving_response)

                client_receiving_response_sock.send(message.encode())
        else:
            print(f"408 {client_receiving_response} doesn't exist")
            message = f"408 {client_receiving_response} doesn't exist"
            client_to_respond.send(message.encode())


    def tell(self,client_to_respond,message,client):
        if client_to_respond in self.clients.values():
            if client_to_respond in self.private.values():
                for key, valeur in self.private.items(): 
                    if client_to_respond == valeur: 
                        client_receiving_response_sock = key
                        if client_receiving_response_sock == client:
                            msg = "you cant send a message to yourself"
                            client_receiving_response_sock.send(msg.encode())
                        else:
                            msg = f"{self.private[client]} : {message}"
                            client_receiving_response_sock.send(msg.encode())
                        #client_receiving_response_sock.send(message.encode())
            elif self.clients[client] == client_to_respond:
                msg = "you cant send a message to yourself"
                client.send(msg.encode())
            else:
                msg = "you need to send a request first"
                client.send(msg.encode())
        else:
            msg = "client doesnt exist"
            client.send(msg.encode())


    def stop(self,sender,client):
        if self.clients[client] == sender:
                message = "you can't use this command to yourself"
                client.send(message.encode())
        elif sender in self.private.values() and self.clients[client] in self.private.values():
            message=f'205 : you stopped the private chat with {sender}'
            client.send(message.encode())
            del self.private[client]
            for key, valeur in self.private.items(): 
                    if sender == valeur: 
                        sender_sock = key
            del self.private[sender_sock]
        else:
            message=f'410 : There is no private chat between you and {sender}'
            client.send(message.encode())

    def connect(self,client):
        pass

    def send_file(self,client):
        message="what file do you want to send : "
        client.send(message.encode())

    def verify_nickname(self,newNick,client):
        if newNick in self.clients.values():
            message=f'409 : {newNick} is already taken'
            client.send(message.encode())
        else:       
            self.broadcast(f'200 : {self.clients[client]} is now {newNick}')
            for key in self.clients:
                if key == client:
                #if self.Connected[i]==self.clients[client]:
                    self.clients[client]=newNick
                    #print(f'verify:{self.clients}')


    def liste_commandes(self,client):
        #ex=print(*self.commands,sep=", ")
        s=" ,".join(self.commands)
        print(s)
        message=f'202 : {s}'
        client.send(message.encode())
        #print(tabulate(self.com, headers=["command","definition"]))


    def liste_clients(self,client):
        x = list(self.clients.values())
        x.sort()
        s=" ,".join(x)
        print(s)
        message=f'203 : {s}'
        client.send(message.encode())


    def quit(self,client):
        message="200 : you have been disconnected"
        client.send(message.encode())
        #self.Connected.remove(self.clients[client])
        name = self.clients[client]
        del self.clients[client]
        self.broadcast(f'200 : {name} disconnected')
        client.close()
        

'''print("server is listening ...")
serveur = Server('127.0.0.1',9381)
serveur.server_start()
serveur.receive()
'''
#port = int(input("choose a port:"))
#host = input("choose a host:")
#host = "127.0.0.1"
serveur = Server('127.0.0.1',9110)
serveur.server_start()
print("server is listening ...")
serveur.receive()
