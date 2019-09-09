from math import sqrt

class Node:
    def __init__(self, parent= None, position = None):
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0
    
    @staticmethod
    def Euclidian(start,end):
        distance = sqrt((end.position[0] - start.position[0]) ** 2 + (end.position[1] - start.position[1]) ** 2)
        return distance

    @staticmethod
    def Manhattan(start,end):
        distance = abs(start.position[0] - end.position[0]) + abs(start.position[1] - end.position[1])
        return distance

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self,other):
        return self.f < other.f