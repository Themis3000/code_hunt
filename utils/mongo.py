import pymongo
import os

client = pymongo.MongoClient(os.environ['mongo_connection_string'])

db = client['codeHuntData']
account_data = db['accountData']
code_data = db['codeData']

