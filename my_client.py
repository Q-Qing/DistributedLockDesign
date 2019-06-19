"""
my_client:
Connecting with leader_server or follower_server.
A client can preempt lock, release lock and check lock.
And the server will response these three actions
"""
from tkinter import *
from socket import *
import datetime
import threading

class My_Client():

    def __init__(self, server_port):
        self.port = server_port
        self.client_id = None
        self.socket = None

    def _connect_with_server(self, hostname, server_port):
        print("start to connect with server")
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.connect((hostname, server_port))
        self.socket = server_socket
        senddata = "NewClient"
        server_socket.sendall(senddata.encode())
        print("client send data")
        data = server_socket.recv(1024).decode('utf-8')
        msg = data.split(":")
        if msg[0] == "ClientId":
            self.client_id = msg[1]
        return server_socket, self.client_id

    def preemptlock(self):
        # send data form: "PreemptLock:Lock:client_id"
        send_data = "PreemptLock:Lock:"+self.client_id
        self.socket.sendall(send_data.encode())
        time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(time1," preemptlock")
        listbox.insert(END,time1)
        listbox.insert(END, "Preempt Lock")
        data = self.socket.recv(1024).decode('utf-8')
        time2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        listbox.insert(END, time2)
        listbox.insert(END, data)
        print(time2," response to preemptlock", data)

    def releaselock(self):
        # send data form: "ReleaseLock:Lock:client_id"
        send_data = "ReleaseLock:Lock:"+self.client_id
        self.socket.sendall(send_data.encode())
        time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(time1," releaselock")
        listbox.insert(END,time1)
        listbox.insert(END, "Release Lock")
        data = self.socket.recv(1024).decode('utf-8')
        time2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        listbox.insert(END, time2)
        listbox.insert(END, data)
        print(time2," response to releaselock", data)

    def checklock(self):
        # send data form: "CheckLock:Lock:client_id"
        send_data = "CheckLock:Lock:"+self.client_id
        self.socket.sendall(send_data.encode())
        time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(time1," checklock")
        listbox.insert(END,time1)
        listbox.insert(END, "Check Lock")
        data = self.socket.recv(1024).decode('utf-8')
        time2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        listbox.insert(END, time2)
        listbox.insert(END, data)
        print(time2," response to checklock", data)


    def create_gui(self):
        root = Tk()
        root.title('client')
        root.geometry('400x300')
        global listbox
        listbox = Listbox(root,width=250)
        listbox.pack()
        preempt_button = Button(root, text='Preempt Lock', command=self.preemptlock)
        preempt_button.pack()
        release_button = Button(root, text='Release Lock', command=self.releaselock)
        release_button.pack()
        check_button = Button(root, text='Check Lock', command=self.checklock)
        check_button.pack()
        root.mainloop()

    def run(self):
        hostname = '127.0.0.1'
        port = self.port
        server_socket, client_id = self._connect_with_server(hostname,port)
        print("server socket:", server_socket)
        print("client_id:", client_id)
        self.create_gui()


client = My_Client(9000)
client.run()


