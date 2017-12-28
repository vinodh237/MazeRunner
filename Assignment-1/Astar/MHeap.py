class mHeap(object):
    def __init__(self):
        self.a = 1
        self.L = []
        self.L.append(None) # add dummy node

    def buildMinHeap(self):
        maxSize = len(self.L)
        for i in range(int(maxSize/2)):
            self.minHeapify(i)
    #
    def minHeapify(self,i):
        if i < (len(self.L)-1)/2:
            l = self.leftChild(i)
            r = self.rightChild(i)
            minIndex = i
            if l!=None and self.L[l].value < self.L[minIndex].value:
                minIndex = l
            if l != None and self.L[l].value == self.L[minIndex].value and self.L[l].g > self.L[minIndex].g:
                minIndex = l

            if r != None and self.L[r].value < self.L[minIndex].value:
                minIndex = r
            if r != None and self.L[r].value == self.L[minIndex].value and self.L[r].g > self.L[minIndex].g:
                minIndex = r
            if i!= minIndex:
                self.swap(i,minIndex)
                self.minHeapify(minIndex)

    def insert(self,a):
        try:
            self.L.append(a)
            i = len(self.L)-1
            while i > 1 and self.L[i].value < self.parent(i).value:
                parent_i = self.parentIndex(i)
                self.swap(i,parent_i)
                i = parent_i
            return True
        except:
            return False

    def popMin(self):
        a = self.L[1]
        self.L[1] = self.L[-1] #replace first element with last element
        del self.L[-1]
        # heapify
        self.minHeapify(1)
        return a

    def swap(self,i,j):
        temp  = self.L[i]
        self.L[i] = self.L[j]
        self.L[j] = temp

    def parent(self, i):
        return self.L[int(i / 2)]

    def parentIndex(self,i):
        if i <= 1:
            return None
        return int(i/2)

    def leftChild(self, i):
        if 2*i > len(self.L):
            return None
        return 2 * i

    def rightChild(self, i):
        if 2 * i + 1 > len(self.L):
            return None
        return 2 * i + 1

# kk = mHeap()
