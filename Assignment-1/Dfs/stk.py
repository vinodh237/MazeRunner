class Stk(object):
    def __init__(self):
        self.L = []

    def push(self, a):
        # type: (object) -> object
        """

        :rtype: object
        """
        try:
            self.L.append(a)
            return True
        except:
            print("error in push")
            return False

    def pop(self):
        if len(self.L) == 0:
            return None
        else:
            a = self.L[-1]
            self.L = self.L[:-1]
            return a
