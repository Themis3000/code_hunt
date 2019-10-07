import pymongo
import os
import time
from codegen import gen_code

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

visits = client["visits"]
referral_codes = visits["referral_codes"]
visits_count = visits["visits_count"]
user_data = visits["user_data"]


def get_code(code):
    code_data = referral_codes.find_one({"_id": code})
    return code_data, visits_count.find_one({"_id": code_data["type"]}), visits_count.find_one({"_id": "ALL"})


def get_type(type):
    return visits_count.find_one({"_id": type})


def add_visit(code, user_id):
    if user_id == "undefined":
        old_user_data = add_user()
        user_id = old_user_data["_id"]
        new_user = True
    else:
        old_user_data = user_data.find_one({"_id": user_id}, {"codes." + code: True, "username": True, "public_id": True})
        new_user = False
    current_time = int(time.time())
    if not old_user_data["codes"]:
        code_data = referral_codes.find_one_and_update({"_id": code}, {"$inc": {"uses": 1}, "$push": {"uses_data": {"time": current_time, "user": old_user_data["username"], "public_id": old_user_data["public_id"]}}}, projection={"uses_data": False})
        if code_data:
            if code_data["include_in_count"]:
                if code_data["uses"] == 0:
                    visits_count.update({"_id": code_data["type"]}, {"$inc": {"visits": 1, "unique_visits": 1}})
                    visits_count.update({"_id": "ALL"}, {"$inc": {"visits": 1, "unique_visits": 1}})
                    user = user_data.find_one_and_update({"_id": user_id}, {"$inc": {"visits": 1, "unique_visits": 1}, "$set": {"codes." + code: {"time": current_time, "visit_num": 1}}}, projection={"codes." + code: True, "username": True, "public_id": True, "visits": True}, returnNewDocument=True)
                else:
                    visits_count.update({"_id": code_data["type"]}, {"$inc": {"visits": 1}})
                    visits_count.update({"_id": "ALL"}, {"$inc": {"visits": 1}})
                    user = user_data.find_one_and_update({"_id": user_id}, {"$inc": {"visits": 1}, "$set": {"codes." + code: {"time": current_time, "visit_num": code_data["uses"] + 1}}}, projection={"codes." + code: True, "username": True, "public_id": True, "visits": True}, returnNewDocument=True)
                return code_data, user, new_user
            else:
                return code_data, user_data.find_one({"_id": user_id}, {"codes." + code: True, "username": True, "public_id": True, "visits": True}), new_user
        else:
            return None, None, None
    else:
        code_data = referral_codes.find_one({"_id": code}, projection={"uses_data": False})
        if code_data:
            return code_data, user_data.find_one({"_id": user_id}, {"codes." + code: True, "username": True, "public_id": True, "visits": True}), new_user
        else:
            return None, None, None


def get_user_by_id(user):
    return user_data.find_one({"_id": user})


def add_user():
    id = gen_code()
    public_id = gen_code()
    data = {"_id": id, "public_id": public_id, "username": "guest", "codes": {}}
    user_data.insert_one(data)
    return data


def set_username(username, id):
    user_data.update_one({"_id": id}, {"$set": {"username": username}})
