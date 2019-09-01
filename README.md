# Distributed Lock Design

## Problem description

This is a semester project of Big Data Processing Technologies (Graduate) Spring 2019 of SJTU.Aim at project 2, I design and complete a simple consensus system whcih consists of a leader server, some follower servers and clients. In this consensus system, each follower server has a replicated map which should be consist with the leader server. The key of map is the name of distributed lock and the value is the client ID who owns the lock. The clients can preempt, release and chech the distributed lock but there are some detaied rules. You can find the detailed [requirements](http://www.cs.sjtu.edu.cn/~wuct/bdpt/project.html) here.

## Ideas

Here I choose to use sockets to simulate the communication in distributed system. It is not real but it is easier to implement. The server and clients can communicate with each other when they bind the same socket. And multithreading is used to simulate the scenario that multi-clients communicate with one server.

## Functions of different parts
There is a flow chart of the distributed system.

The leader server is the first part that running in the system. The leader server will bind a socket and keep listenning when the system starts. The leader server will create a new thread to process the communication when a new follower server or client bind the same socket with the leader server. And the thread processing the messages between leader server and follower servers or clients will assign a unique ID to them if it is their first time to connect with the leader server.

The second part is follower server. A follower server will bind two socket ports. One is used to connect with the leader server and another is used to keep listenning for clients. When a follower server is initialized, a thread will be started to connect to leader server and get it's ID. While, the main thread is listenning. If there is a client connected with the follower, the follower server will assign a unique ID to the client and create a new thread to process the requests from this client. If the request is check the lock, the follower server will response the state of lock. However, if the client want to release or preempt the lock, the follower will retransmit the request to leader server. And the leader server will make decisions about whether to satisfy the request or not.

The last one is client. A client can bind a socket port which is same as the server and send request to the server. Here, the client can send three kinds of request, check lock, release lock and preempt lock.
