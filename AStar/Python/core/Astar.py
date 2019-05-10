import geopy.distance

class Astar(object):
    """
    Implement of A* algorithm from 
    https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    def __init__(self, graph):
        self.graph = graph
        self.openSet = []
        self.closeSet = []

    def reset(self):
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

    def search(self, startNodeID, endNodeID):
        startNode = self.graph.network[startNodeID]
        endNode = self.graph.network[endNodeID]
        print('Start searching...')
        self.openSet.append(startNode['node'])
        startNode['node'].gScore = 0
        startNode['node'].fScore = self.heuristic(startNode['node'].coor, endNode['node'].coor)
        #step = 1
        while self.openSet:
            #print(step, ':', self.openSet)
            currentNode = self.find_current()
            if currentNode.ID == endNodeID:
                print('Search done!')
                self.reset()
                return self.trace_back(currentNode)
            self.closeSet.append(currentNode)
            try:
                neighbours = self.graph.network[currentNode.ID]["neighbours"]
                #print('{}\' neighbours:{}'.format(currentNode.ID, neighbours))
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
                neighbourNode.parent, neighbourNode.disToParent = currentNode, dis
                neighbourNode.gScore = tentative_gScore
                neighbourNode.fScore = neighbourNode.gScore + self.heuristic(neighbourNode.coor, endNode['node'].coor)
            #step += 1
        print('Search done, path not found!')
        self.reset()
        return 'No path between node {} and node {}'.format(startNode['node'], endNode['node'])

    def trace_back(self, PrevNode):
        print('Trace back path...')
        pathNode = [int(PrevNode.ID)]
        nodePair = PrevNode.parent.ID + '_' + PrevNode.ID
        LinkID, nodePairSpeed = self.graph.linkNodeRelation[nodePair].values()
        pathLink = [int(LinkID)]
        pathSpeed = [nodePairSpeed]
        pathDis = [PrevNode.disToParent]
        while PrevNode.parent:
            PrevNode = PrevNode.parent
            pathNode.append(int(PrevNode.ID))
            if PrevNode.parent is not None:
                nodePair = PrevNode.parent.ID + '_' + PrevNode.ID
                linkID, nodePairSpeed = self.graph.linkNodeRelation[nodePair].values()
                pathSpeed.append(nodePairSpeed)
                pathLink.append(int(linkID))
                pathDis.append(PrevNode.disToParent)
        print('Trace done!')
        return {'pathNode':list(reversed(pathNode)), 
                'pathLink':list(reversed(pathLink)), 
                'pathDis':list(reversed(pathDis)), 
                'pathSpeed':list(reversed(pathSpeed))}


