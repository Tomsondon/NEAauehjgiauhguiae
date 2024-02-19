class Stack:
    def __init__(self, maxSize):
        self.__stack = []
        self.__maxSize = maxSize

    def push(self, value):
        self.__stack.append(value)
        if self.isFull():
            raise Exception("Stack is full")

    def pop(self):
        if not (self.isEmpty()):
            poppedItem = self.__stack[-1]
            self.__stack = self.__stack[:-1]
            return poppedItem
        else:
            raise Exception("Stack is empty, cannot pop")

    def empty(self):
        self.__stack = []

    def peek(self):
        if not (self.isEmpty()):
            return self.__stack[-1]
        else:
            raise Exception("Stack is empty, cannot peek")

    def isEmpty(self):
        if len(self.__stack) == 0:
            return True

    def isFull(self):
        if len(self.__stack) == self.__maxSize:
            return True


class Queue:
    def __init__(self, maxSize):
        self.__queue = []
        self.__maxSize = maxSize

    def enqueue(self, item):
        if not self.isFull():
            self.__queue.append(item)
        else:
            raise Exception("Queue is full")

    def dequeue(self):
        if not self.isEmpty():
            removedItem = self.__queue[0]
            self.__queue = self.__queue[1:]
            return removedItem
        else:
            raise Exception("Queue is empty, cannot remove item")

    def peek(self):
        if not self.isEmpty():
            return self.__queue[0]
        else:
            raise Exception("Queue is empty, cannot peek")

    def isEmpty(self):
        if len(self.__queue) == 0:
            return True
        else:
            return False

    def isFull(self):
        if len(self.__queue) == self.__maxSize:
            return True
        else:
            return False
