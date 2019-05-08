class Queue(object):
    def __init__(self):
        self.array = []
    
    def get(self):
        return self.array.pop(0)

    def push(self, value):
        self.array.append(value)
    
    def __len__(self):
        return len(self.array)

if __name__ == '__main__':
    q = Queue()
    print(q.push(5))
    print(q.push(2))
    print(q.push(3))
    print(len(q))
    print(q.push(2))
    print(q.push(0))
    print(len(q))
    print(q.get())
    print(q.get())
    print(q.get())
    print(len(q))