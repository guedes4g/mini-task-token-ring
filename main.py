# We will need the following module to generate randomized lost packets
import random
from socket import *
from threading import Thread
import time

class Listen(Thread):
    def __init__ (self, addr, nextAddr , token, id):
        Thread.__init__(self)
        self.id = id
        self.token = token
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(addr)
        self.nextAddr  = nextAddr

    def sendToken(self, address):
        self.socket.sendto(str.encode(self.token), address)
        self.token = None

    def receiveToken(self):
        message, address = self.socket.recvfrom(1024)
        self.token = message.decode()

    def readFile(self):
        f=open("./file.txt", "r")
        contents = f.read()
        f.close()
        return contents.split('\n')[0]

    def appendFile(self, msg):
        f=open("./file.txt", "a+")
        f.write(msg)
        f.close()

    def run(self):
        print(self.token, self.id)
        while True:
            time.sleep( 5 )
            if self.token != None:
                print(str(self.id) + " sending " + self.token + " to ")
                msg = self.readFile()
                self.appendFile(msg+"\n"+str(1))
                self.sendToken(self.nextAddr)

            else:
                print(str(self.id) + " Waiting")
                self.receiveToken()
            


Listen(
    id=5,
    addr = ("127.0.0.1", 12005), 
    nextAddr= ("127.0.0.1", 12000), 
    token = "123"
).start()

for i in range(5):
    Listen(
        id=i,
        addr = ("127.0.0.1", 12000 + i), 
        nextAddr= ("127.0.0.1", 12000 + i + 1), 
        token = None).start()


