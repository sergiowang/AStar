import geopandas as gpd

class Node(object):
    def __init__(self, ID, lon, lat):
        self.ID = ID
        self.coor = lon, lat
        self.parent = None
        self.gScore, self.fScore = float('Inf'), float('Inf')
        
    def set_parent(self, parentNode):
        self.parent = parentNode

    def show_info(self):
        return 'Node ID:{}, coor:({}, {}), parent:{}'.format(self.ID, self.lon, self.lat, self.parent)

    def __repr__(self):
        return 'Node({})'.format(self.ID)



class Graph(object):
    def __init__(self, shpFile, encoding):
        self.links = gpd.read_file(shpFile, encoding = encoding)
        self.initNetwork()
        print(self.network)
        del self.links

    def initNetwork(self):
        self.network = {}
        for link in self.links.values.tolist():
            linkLength, fromNodeID, toNodeID, geometry = link[1],link[3], link[4], str(link[-1])
            openBracket, closeBracket = geometry.index('('), geometry.index(')')
            points = geometry[openBracket+1:closeBracket-1].split(', ')
            fromNodeCor, toNodeCor = points[0].split(' '), points[1].split(' ')
            fromNodeLon, fromNodeLat = fromNodeCor[0], fromNodeCor[1]
            toNodeLon, toNodeLat = toNodeCor[0], toNodeCor[1]
            fromNode, toNode = Node(fromNodeID, fromNodeLon, fromNodeLat), Node(toNodeID, toNodeLon, toNodeLat)
            try:
                self.network[fromNode].append((toNode, linkLength))
            except KeyError:
                self.network[fromNode] = [(toNode, linkLength)]
        

if __name__ == '__main__':
    g = Graph('E:\java_projects\linkmatch\sz_shp_mars\link', 'gbk')
    

