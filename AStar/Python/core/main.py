from Graph import Graph
from Astar import Astar
import pickle


g = Graph('E:\java_projects\linkmatch\sz_shp_mars\link', 'gbk')
with open('graph.pickle', 'wb') as f:
    pickle.dump(g, f)



with open('graph.pickle', 'rb') as f:
    g = pickle.load(f)
#print(g.network['156221'])
#import collections
#collections.Counter([len(nodeInfo['neighbours']) for nodeID, nodeInfo in g.network.items()])


a = Astar(g)
result = a.search('156221', '156215')