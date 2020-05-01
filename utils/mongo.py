import pymongo
import os

client = pymongo.MongoClient(os.environ['mongo_connection_string'])

db = client['codeHuntData']

collections = db.list_collection_names()

if 'account_data' not in collections:
    pass  # init things like indexs

if 'codeData' not in collections:
    pass  # init things like indexs

account_data = db['accountData']
code_data = db['codeData']
