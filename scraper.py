from bs4 import BeautifulSoup
import requests
import networkx as nx
import matplotlib.pyplot as plt

"""
Next Steps:
2. Parse all trades from one page
3. Parse all trades from multiple pages
4. Parse all trades on right side of trades (iterate through more trades)
5. Add support for multiple quantities

TODO:
1. Don't save item name in item object
2. Block all offer ids
"""
paintNames = {}
paintNames['0'] = ''
paintNames['1'] = 'Burnt Sienna'
paintNames['2'] = 'Lime'
paintNames['3'] = 'Titanium White'
paintNames['4'] = 'Cobalt'
paintNames['5'] = 'Crimson'
paintNames['6'] = 'Forest Green'
paintNames['7'] = 'Grey'
paintNames['8'] = 'Orange'
paintNames['9'] = 'Pink'
paintNames['10'] = 'Purple'
paintNames['11'] = 'Saffron'
paintNames['12'] = 'Sky Blue'
paintNames['13'] = 'Black'

class Item:
    def __init__(self, itemID, certification, paintID, platform, itemName = "", paintName = "", quantity=1):
        self.itemID = itemID
        self.certification = certification
        self.paintID = paintID
        self.platform = platform
        self.itemName = itemName
        self.paintName = paintName
        self.quantity = quantity

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.itemID == other.itemID and self.certification == other.certification and self.paintID == other.paintID and self.platform == other.platform
        else:
            return False

    def __hash__(self):
        return hash((self.itemID, self.certification, self.paintID, self.platform))

    def __str__(self):
        return "{} {} ({})".format(self.paintName, self.itemName, self.quantity)


# build url from params
def buildURL(filterItem = 0, filterCertification=0, filterPaint = 0, filterPlatform = 1, filterSearchType = 1):
    return 'https://rocket-league.com/trading?filterItem={}&filterCertification={}&filterPaint={}&filterPlatform={}&filterSearchType={}'.format(filterItem, filterCertification, filterPaint, filterPlatform, filterSearchType)   

# parse the item attributes from href of item
def parseHref(href):  
    attributes = href.strip('?').split('&')
    args = [attribute.split('=')[1] for attribute in attributes]
    item = Item(*args, 1)
    return item

# Convert html item to item object
def soupItemToItems(soupItems):
    items = []
    for soupItem in soupItems:
        newItem = parseHref(soupItem.get('href'))
        newItem.itemName = getItemNameFromSoup(soupItem)
        newItem.paintName = paintNames.get(newItem.paintID, '')
        newItem.quantity = getQuantityFromSoup(soupItem)
        items.append(newItem)
    return items   

def getItemNameFromSoup(soupItem):
    return soupItem.find('h2').text

def getQuantityFromSoup(soupItem):
    quantityAttempt = soupItem.find(attrs={'class': 'rlg-trade-display-item__amount is--premium'})
    if quantityAttempt:
        return quantityAttempt.text
    return 1
# Get Soup object from url
def getPage(url):
    result = requests.get(url)
    return BeautifulSoup(result.content, 'html.parser')

# Get item objects from left side of trade
def getYourItems(soup):
    yourSoupItems = soup.find(id='rlg-youritems').findAll('a')
    return soupItemToItems(yourSoupItems)

# Get item objects from right side of trade
def getTheirItems(soup):           
    theirSoupItems = soup.find(id='rlg-theiritems').findAll('a')
    return soupItemToItems(theirSoupItems)


page = getPage(buildURL(filterItem=1,filterPaint=2))
yourItems = getYourItems(page)
theirItems = getTheirItems(page)

G = nx.DiGraph()
# Only look at trades that are 1:1 and have the same amount of items
if len(yourItems) == len(theirItems):
    for i in range(len(yourItems)):
        G.add_nodes_from([theirItems[i],yourItems[i]])
        G.add_edge(theirItems[i],yourItems[i])

# nx.set_node_attributes(G, )
nx.draw(G, with_labels=True)
plt.show()

# page = getPage(buildURL(filterItem=496))
# yourSoupItems = page.find(id='rlg-youritems').findAll('a')
# for soupItem in yourSoupItems:
#     quantityAttempt = soupItem.find(attrs={'class': 'rlg-trade-display-item__amount is--premium'})
#     if quantityAttempt:
#         print(quantityAttempt.text)
