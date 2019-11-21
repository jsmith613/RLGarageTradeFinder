from rocket_league_api import *
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

blacklistItems = {
544,  
1701, 
1702,
1703,
1704,
1705,
1706,
1707,
1708,
1709  
}

# trades is a list of trade objects
def addTradesToGraph(graph, trades):
    for trade in trades:
        if trade.isValid():
            for i in range(len(trade.yourItems)):
                addItemsToGraph(graph, trade.theirItems[i], trade.yourItems[i])
                if trade.theirItems[i].quantity > 1:
                    addLowerQuantities(graph, trade.theirItems[i])
                if trade.yourItems[i].quantity > 1:
                    addLowerQuantities(graph, trade.yourItems[i])
    return graph

# Adds the lower quantities of the given item
def addLowerQuantities(graph, item):
    lastItem = item
    while lastItem.quantity > 1:
        newItem = copy.copy(lastItem)
        newItem.quantity = lastItem.quantity - 1
        graph.add_node(newItem)
        graph.add_edge(lastItem, newItem)
        lastItem = newItem

# Adds 2 items to graph and an edge from 1 to 2
def addItemsToGraph(graph, item1, item2):
    graph.add_nodes_from([item1,item2])
    graph.add_edge(item1,item2)

# Initiates search for your desiredItem from yourItem
# yourItem: Item object that you own
# searchItem: Item object that you want
def startTradeSearch(yourItem, searchItem):
    visitedItems = set()
    queue = deque()
    G = nx.DiGraph()
    queue.append(yourItem)
    shouldBreak = False
    # TODO: change this to a real termination condition
    # i = 0
    # while True:
    for i in range(1):
        print("i: ", i)
        newItem = queue.pop()
        print("Searching for item: ", newItem)
        newURL = buildURL(item=newItem) 
        trades = processPage(newURL)
        addTradesToGraph(G, trades)
        for trade in trades:
            # TODO: only add items that can be traded for yourItem (maybe)
            for theirItem in trade.theirItems:
                if theirItem not in visitedItems:
                    visitedItems.add(theirItem)
                    queue.append(theirItem)
                    if nx.all_simple_paths(G, yourItem, searchItem):
                        print("Found trade path!")
                        printPaths(yourItem, searchItem, G)
                        return

def printPaths(yourItem, searchItem, graph):
    for path in nx.all_simple_paths(graph, yourItem, searchItem):
        print(path)


startTradeSearch(Item(itemID=605), Item(itemID=1779, paintID=2))
# print(buildURL(item=Item(itemID=691, paintID=9)))
# print(list(nx.shortest_simple_paths(G, Item(itemID=496), Item(itemID=691, paintID=9), weight=None)))