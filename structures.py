class Stack:
    def __init__(self, maxSize):
        self.stack = []
        self.maxSize = maxSize

    def push(self, value):
        self.stack.append(value)
        if self.isFull():
            raise Exception("Stack is full")

    def pop(self):
        if not (self.isEmpty()):
            poppedItem = self.stack[-1]
            self.stack = self.stack[:-1]
            return poppedItem
        else:
            raise Exception("Stack is empty, cannot pop")

    def empty(self):
        self.stack = []

    def peek(self):
        if not (self.isEmpty()):
            return self.stack[-1]
        else:
            raise Exception("Stack is empty, cannot peek")

    def isEmpty(self):
        if len(self.stack) == 0:
            return True

    def isFull(self):
        if len(self.stack) == self.maxSize:
            return True


class Queue:
    def __init__(self, maxSize):
        self.queue = []
        self.maxSize = maxSize

    def enqueue(self, item):
        if not self.isFull():
            self.queue.append(item)
        else:
            raise Exception("Queue is full")

    def dequeue(self):
        if not self.isEmpty():
            removedItem = self.queue[0]
            self.queue = self.queue[1:]
            return removedItem
        else:
            raise Exception("Queue is empty, cannot remove item")

    def peek(self):
        if not self.isEmpty():
            return self.queue[0]
        else:
            raise Exception("Queue is empty, cannot peek")

    def isEmpty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def isFull(self):
        if len(self.queue) == self.maxSize:
            return True
        else:
            return False

