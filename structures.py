class EventStack:
    def __init__(self, maxSize):
        self.stack = []
        self.maxSize = maxSize

    def push(self, value):
        self.stack.append(value)
        if self.isFull():
            self.stack = self.stack[1:]

    def pop(self):
        if not (self.isEmpty()):
            poppedItem = self.stack[-1]
            self.stack = self.stack[:-1]
            return poppedItem
        else:
            raise Exception("Stack is empty, cannot pop")

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



