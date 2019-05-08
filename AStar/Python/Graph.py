import geopandas as gpd

class Node(object):
    def __init__(self, ID, lon, lat):
        self.ID = ID
        self.lon = lon
        self.lat = lat
        self.parent = None

    def set_parent(self, parentNode):
        self.parent = parentNode

    def __repr__(self):
        return 'Node ID:{}, cor:({}, {}), parent:{}'.format(self.ID, self.lon, self.lat, self.parent)


class Graph(object):
    def __init__(self, shpFile, encoding):
        self.links = gpd.read_file(shpFile, encoding = encoding)
        self.initNetwork()
        print(self.graph)

    def initNetwork(self):
        self.graph = {}
        for link in self.links.values.tolist():
            linkLength, fromNodeID, toNodeID, geometry = link[1],link[3], link[4], str(link[-1])
            openBracket = geometry.index('(')
            closeBracket = geometry.index(')')
            points = geometry[openBracket+1:closeBracket-1].split(', ')
            fromNodeCor = points[0].split(' ')
            fromNodeLon, fromNodeLat = fromNodeCor[0], fromNodeCor[1]
            toNodeCor = points[1].split(' ')
            toNodeLon, toNodeLat = toNodeCor[0], toNodeCor[1]
            fromNode, toNode = Node(fromNodeID, fromNodeLon, fromNodeLat), Node(toNodeID, toNodeLon, toNodeLat)
            print('from node:{}'.format(fromNode))
            print('to node:{}'.format(toNode))
            try:
                self.graph[fromNode].append((toNode, linkLength))
                print(fromNode)
            except KeyError:
                self.graph[fromNode] = [(toNode, linkLength)]
        

if __name__ == '__main__':
    g = Graph('E:\java_projects\linkmatch\sz_shp_mars\link', 'gbk')
    

