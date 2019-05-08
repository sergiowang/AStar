import geopandas as gpd

class Node(object):
    def __init__(self, ID):
        self.ID = ID
    
    def set_parent(self, parentNode):
        self.parent = parentNode

    def __repr__(self):
        return 'Node ID:{}, parent:{}'.format(self.ID, self.parent)


class Graph(object):
    def __init__(self, shpFile, encoding):
        self.links = gpd.read_file(shpFile, encoding = encoding)
        self.initNetwork()
        #print(self.graph)

    def initNetwork(self):
        self.graph = {}
        for link in self.links.values.tolist():
            linkLength, fromNode, toNode = link[1], Node(link[3]), Node(link[4])
            try:
                self.graph[fromNode].append((toNode, linkLength))
                print(fromNode)
            except KeyError:
                self.graph[fromNode] = [(toNode, linkLength)]
        

if __name__ == '__main__':
    g = Graph('E:\java_projects\linkmatch\sz_shp_mars\link', 'gbk')
    

