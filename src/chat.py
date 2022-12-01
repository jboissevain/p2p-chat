import socket
import threading
import chatGUI
import elGamal

FORMAT = 'utf-8'


class Server(threading.Thread):
    def __init__(self, chatApp):
        super().__init__()

        self.chatApp = chatApp
        self.port = self.chatApp.port
        self.host = ''
        self.hasConnection = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.chatApp.log('server started, listening on port ' + str(self.port))

    def run(self):
        conn, addr = self.socket.accept()
        init = conn.recv(1024)
        self.hasConnection = True

        self.handleConnection(init)

        while True:
            data = conn.recv(4096)
            if not data:
                self.chatApp.log('empty message')
                break

            decrypted = self.chatApp.encryption.decrypt(data.decode(FORMAT))
            self.chatApp.printMessage(decrypted.decode(FORMAT))
    
    def handleConnection(self, init):
        if not init:
            self.chatApp.peer = 'none'
            self.chatApp.peerPort = 'none'
            self.chatApp.peerHost = 'none'
        else:
            init = init.decode(FORMAT)
            init = init.split(' ')
            self.chatApp.peer = init[1]
            self.chatApp.peerHost = init[2]
            self.chatApp.peerPort = init[3]
            self.chatApp.setPeerKey([int(init[4]), int(init[5]), int(init[6])])
        
        self.chatApp.connectBack()

    def stop(self):
        if self.hasConnection:
            self.socket.close()
        exit(1)
        



class Client(threading.Thread):
    def __init__(self, chatApp):
        super().__init__()
        self.chatApp = chatApp
        self.isConnected = False

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatApp.log('client started')
        self.sock.settimeout(6)

    def send(self, message):
        if message != '':
            try:
                encrypted = self.chatApp.encryption.encrypt(message)
                self.sock.send(encrypted.encode(FORMAT))
                return True
            except socket.error as error:
                self.chatApp.log('failed to send')
                self.chatApp.log(error)
                self.isConnected = False
                return False

    def connect(self, args):
        #Peer hostname and port
        host = args[0]
        port = int(args[1])

        try:
            self.sock.connect((host,port))
        except socket.error:
            self.chatApp.log('failed connecting to peer')
            return False

        key = self.chatApp.getPublicKey()
        #send initial connection info
        self.sock.send('init {0} {1} {2} {3} {4} {5}'.format(self.chatApp.getNick(), socket.gethostname(), self.chatApp.port, key[0], key[1], key[2]).encode(FORMAT))
        self.chatApp.log('connected to peer')
        self.isConnected = True
        self.chatApp.log('Chosen prime: ' + str(key[2]))
        self.chatApp.log('Chosen alpha: ' + str(key[1]))
        self.chatApp.log('Chosen Public key Beta: ' + str(key[0]))
    
    def stop(self):
        self.sock.close()
        self.sock = None
        exit(1)

class ChatApp():
    def __init__(self):
        super().__init__()
        self.encryption = elGamal.ElGamal(self)
        self.gui = chatGUI.App(self)

        self.port = 3334 # Port the server runs on
        self.nick = "" # User's nickname
        self.peer = "" # Peer nickname
        self.peerHost = "0" # Hostname of peer
        self.peerPort = "0" # Port of peer
        
        self.run()
        self.gui.mainloop()


    def run(self):
        print('starting client')
        self.log('starting client')
        self.client = Client(self)
        self.client.start()

    def startServer(self,port):
        self.port = int(port)
        self.server = Server(self)
        self.server.daemon = True
        self.server.start()

    def stopServer(self):
        self.server.stop()
    
    def log(self, message):
        self.gui.log(message)

    def printMessage(self, message):
        self.gui.printMessage(message, self.peer)
    
    def sendMessage(self, message):
        self.client.send(message)

    def connectBack(self):
        if self.server.hasConnection and not self.client.isConnected:
            self.client.connect([self.peerHost, int(self.peerPort)])
        else:
            return False
    
    def connect(self, args):
        self.client.connect(args)

    def getNick(self):
        return self.gui.getNick()
    
    def getPublicKey(self):
        return self.encryption.getPublicKey()

    def setPeerKey(self, key):
        self.encryption.setPeerKey(key)

if __name__ == "__main__":
    chatApp = ChatApp().run()