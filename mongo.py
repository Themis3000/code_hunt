import pymongo
import os
import time

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

visits = client["visits"]
referral_codes = visits["referral_codes"]
visits_count = visits["visits_count"]


def get_code(code):
    code_data = referral_codes.find_one({"_id": code})
    return code_data, visits_count.find_one({"_id": code_data["type"]}), visits_count.find_one({"_id": "ALL"})


def get_type(type):
    return visits_count.find_one({"_id": type})


def add_visit(code):
    code_data = referral_codes.find_one_and_update({"_id": code}, {"$inc": {"uses": 1}, "$push": {"uses_data": {"time": int(time.time())}}})
    if code_data:
        if code_data["include_in_count"]:
            if code_data["uses"] == 0:
                type_data = visits_count.find_one_and_update({"_id": code_data["type"]}, {"$inc": {"visits": 1, "unique_visits": 1}}, upsert=True)
                type_all_data = visits_count.find_one_and_update({"_id": "ALL"}, {"$inc": {"visits": 1, "unique_visits": 1}})
            else:
                type_data = visits_count.find_one_and_update({"_id": code_data["type"]}, {"$inc": {"visits": 1}}, upsert=True)
                type_all_data = visits_count.find_one_and_update({"_id": "ALL"}, {"$inc": {"visits": 1}})
            return code_data, type_data, type_all_data
        else:
            return code_data, visits_count.find_one({"_id": code_data["type"]}), visits_count.find_one({"_id": "ALL"})
    else:
        return None, None, None
