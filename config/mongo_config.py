from flask import request
import pymongo
from urllib.parse import quote_plus
# local_url = "mongodb://localhost:27017/" 
local_url = "mongodb://cdac:user%40cdac!@13.201.47.59:27017/?authSource=csmart&authMechanism=SCRAM-SHA-256"
# local_url = quote_plus(url_) 
# local_url = "mongodb://user1:cdac012654@65.1.218.101:27017/?authSource=textdata&authMechanism=SCRAM-SHA-256"
# local_url = "mongodb://suser:sup32024@10.226.42.136:27017/?authSource=textdata&authMechanism=SCRAM-SHA-1"
# local_url = "mongodb://user1:cdac%40123@23@10.226.53.238:27017/?authSource=textdata&authMechanism=SCRAM-SHA-1"
# local_url = "mongodb://user1:cdac%40123%23@10.226.53.238:27017/?authSource=textdata&authMechanism=SCRAM-SHA-256"
# local_url="mongodb://admin:AdminMongoDB191@10.11.191.6:27017/socialData?authSource=admin&authMechanism=SCRAM-SHA-256"
client = pymongo.MongoClient(local_url)
# db = client['socialData']
# db = client['webScrapping']
# db = client['textdata']
db = client['csmart']
