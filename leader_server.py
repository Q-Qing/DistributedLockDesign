'''
Author: keqin
Time: 2019-06-11

Leader_server:
There is only one leader_server in a program.
The leader_server can connect with clients and follower_servers.
The leader_server assign client_id and follower_server_id to clients and follower_servers
when a new connection is created.
It also needs to response to preempt/release request of clients or follower_servers.
And it response to check request of clients.
When lock_map changes, it broadcast new lock_map to all follower_servers to ensure
the data consistency of system.
'''

from socket import *
import threading
from threading import Thread

# class Leader_Sever(Thread):
class Leader_Sever():
    def __init__(self,port):
        # super().__init__()
        self.port = port
        self.follower_servers = []
        self.clients = []
        self.connections = []
        self.lock_map = []


    def _new_client(self,c_socket):
        '''
        Creating client_id for clients connected with leader_server.
        The first client's id which connected with leader_server is 1001 and the second is 1002,
        and so on.
        :param c_socket:
        :return: client_id
        '''
        client_id = len(self.clients) + 1001
        self.clients.append({'client_id':client_id,'socket':c_socket})
        return client_id

    def _new_follower(self,c_socket):
        '''
        Creating follower_id for follower_servers. The first id is 2 and the second is 3, and so on.
        The first client's id which connected with follower_server_2 is 2001 and the second is 2002, and so on.
        :param c_socket:
        :return: follower_id
        '''
        follower_id = len(self.follower_servers) +2
        self.follower_servers.append({'follower_id':follower_id,'socket':c_socket})
        return follower_id

    def _preempt_lock(self,lock_name,client_id):
        if self.lock_map != None:
            for lock in self.lock_map:
                if lock['name'] == lock_name:
                    return {'result':False}

        self.lock_map.append({'name': lock_name, 'client': client_id})
        self._update_map(lock_name,client_id)
        return {'result':True}

    def _update_map(self,lock_name,client_id):
        print('broadcast new lock_map')
        for follower in self.follower_servers:
            c_socket = follower['socket']
            senddata = "UpdateLockmap:%s:%d"%(lock_name,int(client_id))
            c_socket.sendall(senddata.encode())

    def _release_lock(self,lock_name,client_id):
        if self.lock_map != None:
            for lock in self.lock_map:
                if lock['name'] == lock_name and lock['client'] == client_id:
                    self.lock_map.remove({"name":lock_name,"client":client_id})
                    self._remove_map(lock_name,client_id)
                    return {'result':True}
        return {'result':False}

    def _remove_map(self,lock_name,client_id):
        print("broadcast to remove lock_map")
        for follower in self.follower_servers:
            c_socket = follower['socket']
            senddata = "RemoveLockmap:%s:%d"%(lock_name,int(client_id))
            c_socket.sendall(senddata.encode())

    def _responce_msg(self,c_socket):
        while True:
            data = c_socket.recv(1024).decode('utf-8')
            # print(data)
            if not data:
                continue

            if data == 'NewClient':
                client_id = self._new_client(c_socket)
                c_socket.sendall(("ClientId:%d"%(client_id)).encode())
                continue

            if data == 'NewFollower':
                follower_id = self._new_follower(c_socket)
                c_socket.sendall(("FollowerId:%d"%(follower_id)).encode())
                continue

            msg = data.split(":")
            if msg[0] == 'PreemptLock':
                res = self._preempt_lock(msg[1], msg[2])
                if res['result']:
                    c_socket.sendall(("PreemptLock Success:%d"%(int(msg[2]))).encode())
                else:
                    c_socket.sendall(("PreemptLock Failed:%d"%(int(msg[2]))).encode())
                continue

            if msg[0] == "ReleaseLock":
                res = self._release_lock(msg[1],msg[2])
                if res['result']:
                    c_socket.sendall(("ReleaseLock Success:%d"%(int(msg[2]))).encode())
                else:
                    c_socket.sendall(("ReleaseLock Failed:%d"%(int(msg[2]))).encode())
                continue

            if msg[0] == "CheckLock":
                if self.lock_map:
                    for lock in self.lock_map:
                        if lock['name'] == msg[1]:
                            # lock_name = lock['name']
                            client_id = lock['client']
                            break
                    c_socket.sendall(("CheckLock:Lock:%d"%(int(client_id))).encode())
                else:
                    c_socket.sendall(("there is no locks in server").encode())


    def run(self):
        host = '127.0.0.1'
        port = self.port
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        print(s)

        while True:
            conn_socket, addr = s.accept()
            print("Connect from", addr)
            self.connections.append(conn_socket)
            leader_server_thread = threading.Thread(target=self._responce_msg, args=(conn_socket,))
            leader_server_thread.setDaemon(True)
            leader_server_thread.start()
            print("active threads:")
            print(threading.active_count())

l_server = Leader_Sever(9000)
l_server.run()

