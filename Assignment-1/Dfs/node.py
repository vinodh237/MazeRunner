class Node:

# Define each node to contain its x and y coordinates and the parent node visited before reaching this node
    def __init__(self, x, y, parent):
        """
        :param x: The X-coordinate of the node
        :param y: The y-coordinate of the node
        :param parent: The node before arriving at this node
        """
        self.x = x
        self.y = y
        self.parent = parent