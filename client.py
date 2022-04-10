
import socket
import threading


class Client():
    def __init__(self,nickname,address,port):
        self.nickname = nickname
        self.address = address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """nickname = input("Choose a nickname : ")
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1',9184))
    """
    def connect(self):
        self.client.connect((self.address,self.port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == "nickname?":
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("an error has occured!")
                self.client.close()
                break


    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('ascii'))
            

nickname = input("choose a nickname:")
client = Client(nickname,"127.0.0.1",9110)

client.connect()
receive_thread = threading.Thread(target=client.receive)
receive_thread.start()

write_thread = threading.Thread(target=client.write)
write_thread.start()
