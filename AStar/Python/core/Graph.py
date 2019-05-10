import geopandas as gpd

class Node(object):
    def __init__(self, ID, lon, lat):
        self.ID = ID
        self.coor = float(lat), float(lon)
        self.parent = None
        self.gScore, self.fScore = float('Inf'), float('Inf')
        self.disToParent = None
        self.speedFromParent = None

    def show_info(self):
        return 'Node ID:{}, coor:({}, {}), parent:{}'.format(self.ID, self.lon, self.lat, self.parent)

    def __repr__(self):
        return 'Node({})'.format(self.ID)


class Graph(object):
    def __init__(self, shpFile, encoding):
        print('Reading shp file...')
        self.links = gpd.read_file(shpFile, encoding = encoding)
        self.linkNodeRelation = {}
        self.network = {}
        print('Initing network...')
        self.init_link_node_relation()
        self.init_network()
        del self.links
        print('Network init done!')

    def init_link_node_relation(self):
        """
        linkNodeRelation:{"fromNodeID_toNodeID":{"linkID":xx,"speed":xx},
                          "fromNodeID_toNodeID":{"linkID":xx,"speed":xx},
                          "fromNodeID_toNodeID":{"linkID":xx,"speed":xx},
                          ....}
        """
        for link in self.links.values.tolist():
            linkID, direction, fromNodeID, toNodeID = str(link[0]), link[2], str(link[3]), str(link[4])
            speedFromTo, speedToFrom = link[-4], link[-3]
            key1 = fromNodeID + '_' + toNodeID
            self.linkNodeRelation[key1] = {'linkID':linkID, 'speed':speedFromTo}
            if direction == 0:
                key2 = toNodeID + '_' + fromNodeID
                self.linkNodeRelation[key2] = {'linkID':linkID, 'speed':speedToFrom}


    def init_network(self):
        """
        network:{nodeID:{"node":NodeInstance, 
                         "neighbours":[(Node1, dis1), (Node2, dis2), ...]}, 
                        ...}
        """
        for link in self.links.values.tolist():
            linkID, linkLength, direction, fromNodeID, toNodeID, geometry = str(link[0]), link[1], link[2], str(link[3]), str(link[4]), str(link[-1])
            # parse from node's and to node's coors
            openBracket, closeBracket = geometry.index('('), geometry.index(')')
            points = geometry[openBracket+1:closeBracket-1].split(', ')
            fromNodeCor, toNodeCor = points[0].split(' '), points[1].split(' ')
            fromNodeLon, fromNodeLat = fromNodeCor[0], fromNodeCor[1]
            toNodeLon, toNodeLat = toNodeCor[0], toNodeCor[1]
            # init from node and to node instance
            fromNode, toNode = Node(fromNodeID, fromNodeLon, fromNodeLat), Node(toNodeID, toNodeLon, toNodeLat)
            try:
                self.network[fromNode.ID]["neighbours"].append((toNode, linkLength))
                if direction == 0:
                    self.network[toNode.ID]["neighbours"].append((fromNode, linkLength))
            except KeyError:
                self.network[fromNode.ID] = {"node":fromNode, 
                                             "neighbours":[(toNode, linkLength)]}
                if direction == 0:
                    self.network[toNode.ID] = {"node":toNode, 
                                               "neighbours":[(fromNode, linkLength)]}



if __name__ == '__main__':
    g = Graph('E:\java_projects\linkmatch\sz_shp_mars\link', 'gbk')
    

