import geopy.distance

class Astar(object):
    """
    Implement of A* algorithm from 
    https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    def __init__(self, graph, startNodeID, endNodeID):
        self.graph, self.startNodeID, self.endNodeID = graph, startNodeID, endNodeID
        self.startNode = self.graph.network[startNodeID]
        self.endNode = self.graph.network[endNodeID]
        self.openSet = []
        self.closeSet = []

    @staticmethod
    def heuristic(Node1, Node2):
        return float(geopy.distance.vincenty(Node1, Node2).m)

    def find_current(self):
        """
        Find and remove the node with the lowest fScore from the openset
        """
        minfScore = self.openSet[0].fScore
        minIndex = 0
        for i, Node in enumerate(self.openSet):
            fScore = Node.fScore
            if fScore < minfScore:
                minfScore = fScore
                minIndex = i
        # get and remove
        return self.openSet.pop(minIndex)

    def search(self):
        print('Start searching...')
        self.openSet.append(self.startNode['node'])
        self.startNode['node'].gScore = 0
        self.startNode['node'].fScore = self.heuristic(self.startNode['node'].coor, self.endNode['node'].coor)
        #step = 1
        while self.openSet:
            #print(step, ':', self.openSet)
            currentNode = self.find_current()
            if currentNode.ID == self.endNode['node'].ID:
                return self.trace_back(currentNode)
            self.closeSet.append(currentNode)
            try:
                neighbours = self.graph.network[currentNode.ID]["neighbours"]
                print('{}\' neighbours:{}'.format(currentNode.ID, neighbours))
            except KeyError:
                # dead end node with no neighbours
                continue
            #print('NEIGHBOURS:{}'.format(neighbours))
            for neighbour in neighbours:
                # neighbour node object and distance from current node to this neighbour
                neighbourNode, dis = neighbour
                if neighbourNode in self.closeSet:
                    continue
                # tentative gScore for this neighbour node
                tentative_gScore = currentNode.gScore + dis
                if neighbourNode not in self.openSet:
                    self.openSet.append(neighbourNode)
                elif tentative_gScore >= neighbourNode.gScore:
                    continue
                neighbourNode.parent = currentNode
                neighbourNode.gScore = tentative_gScore
                neighbourNode.fScore = neighbourNode.gScore + self.heuristic(neighbourNode.coor, self.endNode['node'].coor)
            #step += 1
        return 'No path between node {} and node {}'.format(self.startNode['node'], self.endNode['node'])

    def trace_back(self, LastNode):
        path = [LastNode]
        while LastNode.parent:
            path.append(LastNode.parent)
            LastNode = LastNode.parent
        return list(reversed(path))


