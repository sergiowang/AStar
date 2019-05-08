import geopy.distance

class Astar(object):
    """
    Implement of A* algorithm from 
    https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    def __init__(self, graph, startNodeID, endNodeID):
        self.graph, self.startNodeID, self.endNodeID = graph, startNodeID, endNodeID
        self.startNode = [Node for Node in self.graph.network.keys() if Node.ID == startNodeID][0]
        self.endNode = [Node for Node in self.graph.network.keys() if Node.ID == endNodeID][0]
        self.openSet = []
        self.closeSet = []

    @staticmethod
    def heuristic(Node1, Node2):
        return geopy.distance.vincenty(Node1, Node2).m

    def find_current(self):
        """
        Find and remove the node with the lowest fScore from the openset
        """
        minfScore = self.openSet[0]
        minIndex = 0
        for i, Node in enumerate(self.openSet):
            fScore = Node.fScore
            if fScore < minfScore:
                minfScore = fScore
                minIndex = i
        # get and remove
        return self.openSet.pop(minIndex)

    def search(self):
        self.openSet.append(self.startNode)
        self.startNode.gScore = 0
        self.startNode.fScore = self.heuristic(self.startNode.coor, self.endNode.coor)
        while self.openSet:
            currentNode = self.find_current()
            if currentNode.ID == self.endNode:
                return self.trace_back(currentNode)
            self.closeSet.append(currentNode)
            for neighbour in self.graph.network[currentNode]:
                # neighbour node object and distance from current node to this neighbour
                neighbourNode, dis = neighbour
                if neighbour in self.closeSet:
                    continue
                # tentative gScore for this neighbour
                tentative_gScore = currentNode.gScore + dis
                if neighbour not in self.openSet:
                    self.openSet.append(neighbour)
                elif tentative_gScore >= neighbour.gScore:
                    continue
                neighbourNode.parent = currentNode
                neighbour.gScore = tentative_gScore
                neighbour.fScore = neighbour.gScore + self.heuristic(neighbourNode.coor, self.endNode.coor)
        return 'No path between node {} and node {}'.format(self.startNode, self.endNode)

    def trace_back(self, LastNode):
        path = [LastNode]
        while LastNode.parent:
            path.append(LastNode.parent)
        return list(reversed(path))
