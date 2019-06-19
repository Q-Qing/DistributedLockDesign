'''
Author: keqin
Time: 2019-06-11

Follower_server:
There can be many follower_servers in a program.
The follower_server can connect with clients and leader_servers.
The follower_server assign client_id to clients when a new connection is created.
It forwards preempt/release request of clients to leader_servers and forwards the response of leader_server to clients.
And it responses to check request of clients.
When lock_map changes, it change its local lock_map according to leader_server's message.
'''
from socket import *
import threading
from threading import Thread

# class Follower_Server(Thread):
class Follower_Server():

    def __init__(self,selfport,leaderport):
        super().__init__()
        self.selfport = selfport
        self.leaderport = leaderport
        self.lock_map = []
        self.clients = []
        self.connections = []
        self.followerid = None

    def _connect_with_leaderserver(self,host,port):
        print("start to connect with leader_server")
        leader_socket = socket(AF_INET,SOCK_STREAM)
        leader_socket.connect((host, port))
        senddata = "NewFollower"
        leader_socket.sendall(senddata.encode())
        print("follower send data")
        data = leader_socket.recv(1024).decode('utf-8')
        msg = data.split(":")
        if msg[0] == "FollowerId":
            FollowerId = int(msg[1])
            self.followerid = FollowerId
        return leader_socket, FollowerId

    def _forward_down(self,leader_socket):
        '''
        forward messsage of leader_server to clients
        :return:
        '''
        while True:
            data = leader_socket.recv(1024)
            if not data:
                continue
            msg = data.split(":")

            if msg[0] == 'UpdateLockmap':
                self.lock_map.append({'name':msg[1],'client':msg[2]})
                continue
            if msg[0] == 'RemoveLockmap':
                self.lock_map.remove({'name':msg[1],'client':msg[2]})
            if msg[0] == 'PreemptLock Success' or msg[0] == 'PreemptLock Failed' or msg[0] == 'ReleaseLock Success' or msg[0] == 'ReleaseLock Failed':
                client_id = msg[1]
                for client in self.clients:
                    if client['id'] == int(client_id):
                        client['socket'].sendall(msg[0])

    def _new_client(self,c_socket):
        client_id = self.followerid*1000 + len(self.clients) + 1
        self.clients.append({'client_id':client_id,'socket':c_socket})
        return client_id

    def _forward_up(self,leader_socket,c_socket):
        while True:
            data = c_socket.recv(1024)
            if not data:
                continue
            if data == 'NewClient':
                client_id = self._new_client(c_socket)
                c_socket.sendall("ClientId:%d"%(client_id))
                continue

            msg = data.split(":")
            if msg[0] == "PreemptLock":
                leader_socket.sendall("PreemptLock:%s:%d"%(msg[1], msg[2]))
                continue

            if msg[0] == "ReleaseLock":
                leader_socket.sendall("ReleaseLock:%s:%d"%(msg[1], msg[2]))
                continue

            if msg[0] == "CheckLock":
                if self.lock_map == None:
                    lock_name = None
                    client_id = None
                else:
                    for lock in self.lock_map:
                        if lock['name'] == msg[1]:
                            lock_name = lock['name']
                            client_id = lock['client']
                c_socket.sendall("CheckLock:%s:%d"%(lock_name, client_id))



    def run(self):
        host = '127.0.0.1'

        # connect to leader_server
        leader_socket, follower_id = self._connect_with_leaderserver(host,self.leaderport)
        print("leader socket and follower_id")
        print(leader_socket,follower_id)
        forward_down = threading.Thread(self._forward_down(leader_socket))
        forward_down.setDaemon(True)
        forward_down.start()

        # bind self socket
        s = socket(AF_INET,SOCK_STREAM)
        s.bind((host,self.selfport))
        s.listen(3)
        print(s, "listening##########################")

        while True:
            c_soc, addr = s.accept()
            print("connect with ",addr)
            forward_up = threading.Thread(self._forward_up(leader_socket,c_soc))
            forward_up.setDaemon(True)
            forward_up.start()

f_server = Follower_Server(9001,9000)
f_server.run()