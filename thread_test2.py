from threading import Thread
from time import sleep

def thread1():
    for i in range(10):
        print("thread1111111111")
        sleep(1)


def thread2():
    for j in range(10):
        print("thread2222222222")
        sleep(1)

print("run")
t1 = Thread(target=thread1,args=())
t2 = Thread(target=thread2,args=())
t1.start()
t2.start()

