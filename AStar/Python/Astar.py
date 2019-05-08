import geopy.distance

class Astar(object):
    """
    Implement of A* algorithm from 
    https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    def __init__(graph, startNode, endNode, heuristic = straightDistance):
        self.graph, self.start, self.end = graph, start, end
        self.openSet = [startNode]
        self.closeSet = []
        self.heuristic = heuristic

    @staticmethod
    def straight_distance_between(Node1, Node2):
        return geopy.distance.vincenty(Node1, Node2).m

    def seach(self):
        pass

    def trace_back(self):
        pass
