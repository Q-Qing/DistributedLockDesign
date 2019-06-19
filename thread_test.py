import threading

class Thread_test():

    def thread1(self):
        for i in range(10):
            print("thread1111111111")

    def thread2(self):
        for i in range(10):
            print("thread2222222222")

    def run(self):
        print("run")
        t1 = threading.Thread(target=self.thread1, args=())
        t1.start()
        t2 = threading.Thread(target=self.thread2, args=())
        t2.start()

tt = Thread_test()
tt.run()