from core.Astar import Astar
from core.Graph import Graph
from flask import Flask, request
import json
from flask_cors import *

app = Flask("AStar Server")
CORS(app, supports_credentials = True)

@app.route('/search/AStar/<fromNodeID>/<toNodeID>', methods = ['GET'])
def search(fromNodeID, toNodeID):
    global searchEngine
    result = searchEngine.search(fromNodeID, toNodeID)
    return json.dumps(result)

if __name__ == '__main__':
    g = Graph('E:\java_projects\linkmatch\sz_shp_mars\link', 'gbk')
    searchEngine = Astar(g)
    HOST = '10.10.14.5'
    PORT = 8899
    app.run(HOST, PORT, threaded = True, debug = True)