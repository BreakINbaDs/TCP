from collections import deque
from threading import Thread
import threading
#temporary class of queue b
class Queue:
    def __init__(self):
        self.lock = threading.Lock()
        self.q_user1 = deque([])
        self.q_user2 = deque([])
        self.q_user3 = deque([])

    def add_user1(self, input):
        try:
            self.lock.acquire()
            self.q_user1.append(input)
        finally:
            self.lock.release()
            return self.q_user1


    def add_user2(self, input):
        try:
            self.lock.acquire()
            self.q_user2.append(input)
        finally:
            self.lock.release()
            return self.q_user2

    def add_user3(self, input):
        try:
            self.lock.acquire()
            self.q_user3.append(input)
        finally:
            self.lock.release()
            return self.q_user3

    def take1(self):
        return self.q_user1.popleft()

    def take2(self):
        return self.q_user2.popleft()

    def take3(self):
        return self.q_user3.popleft()

#queue=Queue()
#queue.add('3,6,c')
#queue.add('5,6,c')
#queue.add('4,1,c')
#queue.add('3,4,c')
#print queue.q
#print queue.take()
#print queue.q

