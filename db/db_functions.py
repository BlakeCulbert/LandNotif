from pymongo import MongoClient
from pprint import pprint

# db connection
client = MongoClient('mongodb+srv://blake:angels36@cluster0.ixv8b.mongodb.net/LandScrapeDB?retryWrites=true&w=majority')
db = client.LandScrapeDB

def insert_query(land_query):
    result = db.Query.insert_one(land_query)

def insert_regions(region):
    result = db.landParameters.insert_one(region)

# get regions from state
def region_search(state):
    regions = []
    search = db.landParameters.find({state : { '$exists' : True }})
    for i in search:
        regions = i[state]
    return regions

def query_search():
    search = list(db.Query.find({}))
    return search

def insert_land_data(land_data):
    result = db.landData.insert_one(land_data)

def land_search(state, region):
    land = []
    search = db.landData.find({'state' : state, 'region' : region })
    for i in search:
        land.append(i)
    return land
