# Distributed Lock Design

## Problem description

This is a semester project of Big Data Processing Technologies (Graduate) Spring 2019 of SJTU.Aim at project 2, I design and complete a simple consensus system whcih consists of a leader server, some follower servers and clients. In this consensus system, each follower server has a replicated map which should be consist with the leader server. The key of map is the name of distributed lock and the value is the client ID who owns the lock. The clients can preempt, release and chech the distributed lock but there are some detaied rules. You can find the detailed [requirements](http://www.cs.sjtu.edu.cn/~wuct/bdpt/project.html) here.

## Ideas

Here I choose to use sockets to simulate the communication in distributed system. It is not real but it is easier to implement. The server and clients can communicate with each other when they bind the same socket. And multithreading is used to simulate the scenario that multi-clients communicate with one server.
