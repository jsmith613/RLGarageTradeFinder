from bs4 import BeautifulSoup
import requests
import copy

"""
Next Steps:
3. Parse all trades from multiple pages
5. Add support for multiple quantities
6. Add termination condition
7. Add URL's to edges

TODO:
2. Don't save item name in item object
3. Block all offer ids
4. Add parallelism
5. bi-directional search
"""
paintNames = {}
paintNames[0] = ''
paintNames[1] = 'Burnt Sienna'
paintNames[2] = 'Lime'
paintNames[3] = 'Titanium White'
paintNames[4] = 'Cobalt'
paintNames[5] = 'Crimson'
paintNames[6] = 'Forest Green'
paintNames[7] = 'Grey'
paintNames[8] = 'Orange'
paintNames[9] = 'Pink'
paintNames[10] = 'Purple'
paintNames[11] = 'Saffron'
paintNames[12] = 'Sky Blue'
paintNames[13] = 'Black'

class Trade:
    def __init__(self, yourItems, theirItems):
        self.yourItems = yourItems
        self.theirItems = theirItems

    def isValid(self):
        # TODO: check for valid items in seperate module
        # for item in self.yourItems:
        #     if not item.isValid(): 
        #         return False
        # for item in self.theirItems:
        #     if not item.isValid(): 
        #         return False
        return len(self.yourItems) == len(self.theirItems)

class Item:
    def __init__(self, itemID, certification=0, paintID=0, platform=1, itemName = "", paintName = "", quantity=1):
        self.itemID = itemID
        self.quantity = quantity
        self.itemName = itemName
        self.platform = platform
        if itemID == 496:
            self.initKey()
        else:
            self.certification = certification
            self.paintID = paintID
            self.paintName = paintName


    def initKey(self):
        self.certification = 0
        self.paintID = 0
        self.paintName = ""

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.itemID == other.itemID and self.certification == other.certification and self.paintID == other.paintID and self.platform == other.platform and self.quantity == other.quantity
        else:
            return False

    def __hash__(self):
        return hash((self.itemID, self.certification, self.paintID, self.platform))

    def __str__(self):
        prettyCert = "" if self.certification == 0 else self.certification
        return "{} {} ({}) {}".format(self.paintName, self.itemName, self.quantity, prettyCert)
    def __repr__(self):
        return self.__str__()

    # TODO: implement this method to get rid of offer objects
    def isValid(self):
        return True


# build url from params
def buildURL(filterItem = 0, filterCertification = 0, filterPaint = 0, filterPlatform = 1, filterSearchType = 2, pageNum = 1, item = None):
    paint = 'N' if filterPaint == 0 else filterPaint
    if item != None:
        filterItem = item.itemID
        filterCertification = item.certification
        paint = item.paintID if item.paintID != 0 else 'N'
        filterPlatform = item.platform
    return 'https://rocket-league.com/trading?filterItem={}&filterCertification={}&filterPaint={}&filterPlatform={}&filterSearchType={}&p={}'.format(filterItem, filterCertification, paint, filterPlatform, filterSearchType, pageNum)   

# parse the item attributes from href of item
def parseHref(href):  
    attributes = href.strip('?').split('&')
    args = [int(attribute.split('=')[1]) for attribute in attributes]
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
        return int(quantityAttempt.text.strip())
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

# Gets all trades and their items
def processPage(url):
    page = getPage(url)
    yourTrades = page.findAll(id='rlg-youritems')
    theirTrades = page.findAll(id='rlg-theiritems')
    trades = []
    for i in range(len(yourTrades)):
        yourSoupItems = yourTrades[i].findAll('a')
        theirSoupItems = theirTrades[i].findAll('a')
        yourItems = soupItemToItems(yourSoupItems)
        theirItems = soupItemToItems(theirSoupItems)
        trades.append(Trade(yourItems, theirItems))
    return trades



# page = getPage(buildURL(filterItem=496))
# yourTrades = page.findAll(id='rlg-youritems')
# theirTrades = page.findAll(id='rlg-theiritems')
# trades = []
# for i in range(len(yourTrades)):
#     yourSoupItems = yourTrades[i].findAll('a')
#     theirSoupItems = theirTrades[i].findAll('a')
#     yourItems = soupItemToItems(yourSoupItems)
#     theirItems = soupItemToItems(theirSoupItems)
#     trades.append([yourItems,theirItems])
# print(trades)