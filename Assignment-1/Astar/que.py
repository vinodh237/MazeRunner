
class queue(object):
    def __init__(self):
        self.L = []

    def enque(self,a):
        try:
            self.L.append(a)
            return True
        except:
            print("error in enque")
            return False

    def deque(self):
        if len(self.L) > 0:
            a = self.L[0]
            self.L = self.L[1:]
            return a
        else:
            return None