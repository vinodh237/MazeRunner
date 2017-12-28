class queue:
    def __init__(self):
        self.L = []
# adds an element to the back of the Queue
    def enque(self,a):
        """
        :param a:
        :return: True if element was successfully added else False
        """
        try:
            self.L.append(a)
            return True
        except:
            print("error in enque")
            return False

    def deque(self):
        """
        :return: an element from the front of the Queue
        """
        if len(self.L) > 0:
            a = self.L[0]
            self.L = self.L[1:]
            return a
        else:
            return None

    def top(self):
        """
        :return: the front element of Queue
        """
        if len(self.L) > 0:
            a = self.L[0]
            return a
        else:
            return None

    def size(self):
        """

        :return: the size of the Queue
        """
        return len(self.L)
