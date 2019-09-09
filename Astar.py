import heapq
from tb1util.Enums import GridItemType
from Node import Node



""" 
    scenario: bidimensional list
    start,target: tuples (x,y)
    heuristic: function(start,end)
"""
def astar(scenario,start,target,heuristic):
    startNode = Node(None, start)
    targetNode = Node(None, target)
    opened = []
    closed = []
    n = len(scenario)
    #heapq works with tuples, in this case we add f() to sort this list in heap
    heapq.heappush(opened,startNode)

    evaluated = []

    while len(opened) > 0:
        #heappop returns the smallest Node by f() value
        currentNode = heapq.heappop(opened)

        if currentNode == targetNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1],evaluated
        
        successors = []
        #Get all successors of current node
        for movement in [(0,-1),(0,1),(-1,0),(1,0)]:
            #Get coords after movement
            coordX = currentNode.position[0] + movement[0]
            coordY = currentNode.position[1] + movement[1]

            #Validate if doesn't collide with map
            if coordX > n - 1 or coordX < 0 \
                or coordY > (n - 1) or coordY < 0:
                continue
            #make sure the next position is enabled
            if scenario[coordX][coordY] != GridItemType.ROAD and scenario[coordX][coordY] != GridItemType.SEMAPH_GREEN \
                and scenario[coordX][coordY] != GridItemType.TARGET:
                continue

            evaluated.append((coordX,coordY))

            #Append the new node to successors
            newNode = Node(currentNode,(coordX,coordY))
            successors.append(newNode)

        for s in successors:
            for c in closed:
                if s == c:
                    continue
            s.g = currentNode.g + 1
            s.h = heuristic(s,targetNode)
            s.f = s.g + s.h
            heapq.heappush(opened,s)