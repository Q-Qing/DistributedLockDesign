import threading
from time import sleep

def thread1():
    for i in range(10):
        print("thread1111111111")
        sleep(1)


def thread2():
    for i in range(10):
        print("thread2222222222")
        sleep(1)

print("run")
t1 = threading.Thread(target=thread1())
t1.start()
t2 = threading.Thread(target=thread2())
t2.start()
