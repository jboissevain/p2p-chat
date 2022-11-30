import tkinter as tk
from tkinter import ttk

class TopFrame(ttk.Frame):
    def __init__(self,container, controller):
        super().__init__(container)
        self.controller = controller

        options = {'padx': 5, 'pady':5, 'side':tk.LEFT}

        self.IPlabel = ttk.Label(self, text='IP Address')
        self.IPlabel.pack(**options)

        self.IPInput = ttk.Entry(self)
        self.IPInput.pack(**options)

        self.nickLabel = ttk.Label(self, text = 'Nickname')
        self.nickLabel.pack(**options)

        self.nickInput = ttk.Entry(self)
        self.nickInput.pack(**options)

        self.portLabel = ttk.Label(self,text='Port')
        self.portLabel.pack(**options)

        self.portInput = ttk.Entry(self)
        self.portInput.pack(**options)

        self.connectButton = ttk.Button(self, text='Connect to chat', command=lambda: controller.connect([self.IPInput.get(), self.portInput.get()]))
        self.connectButton.pack(**options)

        self.pack(side=tk.TOP)

class InfoFrame(ttk.Frame):
     def __init__(self,container, controller):
        super().__init__(container)
        self.controller= controller

        options = {'padx': 5, 'pady':5, 'side':tk.TOP}
        self.connectedVar = tk.StringVar(self, 'Connected: False')
        self.IPLabel = ttk.Label(self, textvariable=self.connectedVar)
        self.IPLabel.pack(**options)

        self.serverPortLabel = ttk.Label(self, text='Server port to use')
        self.serverPortLabel.pack(padx = 5, side=tk.TOP)
        self.serverPortEntry = ttk.Entry(self)
        self.serverPortEntry.pack(padx = 5,side=tk.TOP)

        self.startServerButton = ttk.Button(self, text='start server', command=lambda: controller.startServer(self.serverPortEntry.get()))
        self.startServerButton.pack(**options)

        self.exitButton = ttk.Button(self, text='Stop Server', command=lambda: controller.stopServer())

        self.pack(side=tk.LEFT)

class ChatFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)

        options = {'padx': 5, 'pady':5, 'side':tk.BOTTOM}

        self.chatBox = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED)
        self.chatBox.pack(**options)

        self.pack(side=tk.RIGHT)
    
    def addMessage(self, message, sender):
        self.chatBox.config(state=tk.NORMAL)
        self.chatBox.insert(tk.END,sender+': '+ message+'\n\n')
        self.chatBox.config(state=tk.DISABLED)

class MessageFrame(ttk.Frame):
    def __init__(self,container, controller):
        super().__init__(container)

        self.controller = controller

        options = {'padx': 5, 'pady':5, 'side':tk.BOTTOM}

        self.messageBox = ttk.Entry(self, width=100)
        self.messageBox.pack(side = tk.LEFT)

        self.sendButton = ttk.Button(self, 
                                    text='Send',
                                    command=lambda: controller.sendMessage(self.messageBox.get()))
        self.sendButton.pack(padx = 5, pady = 5, side= tk.RIGHT)

        self.pack(**options)


class App(tk.Tk):
    def __init__(self, chatApp):
        super().__init__()

        self.chatApp = chatApp

        self.title('p2p-chat')
        self.geometry('800x400')

        self.topFrame = TopFrame(self, self)
        self.messageFrame = MessageFrame(self, self)
        self.chatFrame = ChatFrame(self)
        self.infoFrame = InfoFrame(self,self)

    def sendMessage(self, message):
        self.chatApp.sendMessage(message)
        self.chatFrame.addMessage(message, self.topFrame.nickInput.get())

    def connect(self, args):
        if(self.chatApp.connect(args)):
            self.infoFrame.connectedVar.set('Connected: True')

    def printMessage(self, message, sender):
        self.chatFrame.addMessage(message, sender)

    def startServer(self, port):
        self.chatApp.startServer(port)
    
    def stopServer(self):
        self.chatApp.stopServer()

    def log(self, message):
        self.chatFrame.addMessage(message, 'System Log')
    
    def getNick(self):
        return self.topFrame.nickInput.get()