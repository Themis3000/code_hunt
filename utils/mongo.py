import pymongo
import os
import time
from utils.codegen import gen_code

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

visits = client["visits"]
referral_codes = visits["referral_codes"]
visits_count = visits["visits_count"]
user_data = visits["user_data"]


def get_type_data(type):
    return visits_count.find_one({"_id": type})


def add_visit(code, user_id):
    if user_id == "undefined":
        old_user_data = add_user()
        user_id = old_user_data["_id"]
        new_user = True
    else:
        old_user_data = user_data.find_one({"_id": user_id}, {"codes." + code: True, "username": True, "public_id": True, "visits_counts.ALL": True})
        new_user = False
    current_time = int(time.time())
    if not old_user_data["codes"]:
        code_data = referral_codes.find_one_and_update({"_id": code}, {"$inc": {"uses": 1}, "$push": {"uses_data": {"time": current_time, "user": old_user_data["username"], "public_id": old_user_data["public_id"]}}}, projection={"uses_data": False})
        if code_data:
            if code_data["include_in_count"]:
                if code_data["uses"] == 0:
                    type_data = visits_count.find_one_and_update({"_id": code_data["type"]}, {"$inc": {"visits": 1, "unique_visits": 1}})
                    visits_count.update({"_id": "ALL"}, {"$inc": {"visits": 1, "unique_visits": 1}})
                    user = user_data.find_one_and_update({"_id": user_id}, {"$inc": {"visits_counts.ALL.visits": 1, "visits_counts.ALL.unique_visits": 1, "visits_counts." + code_data["type"] + ".visits": 1, "visits_counts." + code_data["type"] + ".unique_visits": 1}, "$set": {"codes." + code: {"time": current_time, "visit_num": 1, "type": code_data["type"], "public_id": code_data["public_id"]}}}, projection={"codes." + code: True, "username": True, "public_id": True, "visits": True, "visits_counts.ALL": True}, returnNewDocument=True)
                else:
                    type_data = visits_count.find_one_and_update({"_id": code_data["type"]}, {"$inc": {"visits": 1}})
                    visits_count.update({"_id": "ALL"}, {"$inc": {"visits": 1}})
                    user = user_data.find_one_and_update({"_id": user_id}, {"$inc": {"visits_counts.ALL.visits": 1, "visits_counts." + code_data["type"] + ".visits": 1}, "$set": {"codes." + code: {"time": current_time, "visit_num": code_data["uses"] + 1, "type": code_data["type"], "public_id": code_data["public_id"]}}}, projection={"codes." + code: True, "username": True, "public_id": True, "visits": True, "visits_counts.ALL": True}, returnNewDocument=True)
                return code_data, user, type_data, new_user
            else:
                return code_data, user_data.find_one({"_id": user_id}, {"codes." + code: True, "username": True, "public_id": True, "visits_counts.ALL": True}), visits_count.find_one({"_id": code_data["type"]}), new_user
        else:
            return None, None, None, None
    else:
        code_data = referral_codes.find_one({"_id": code}, projection={"uses_data": False})
        if code_data:
            return code_data, user_data.find_one({"_id": user_id}, {"codes." + code: True, "username": True, "public_id": True, "visits_counts.ALL": True}), visits_count.find_one({"_id": code_data["type"]}), new_user
        else:
            return None, None, None, None


def get_user_by_public_id(public_id):
    return user_data.find_one({"public_id": public_id})


def get_code_data_by_public_id(public_code_id):
    return referral_codes.find_one({"public_id": public_code_id})


def add_user():
    id = gen_code()
    public_id = gen_code()
    data = {"_id": id, "public_id": public_id, "join_date": int(time.time()), "visits_counts": {}, "username": "guest", "codes": {}}
    user_data.insert_one(data)
    return data


def set_username(username, id):
    user_data.update_one({"_id": id}, {"$set": {"username": username}})


def get_top(type, amount):
    return user_data.find(projection={"public_id": True, "visits_counts." + type + ".visits": True, "username": True}).sort("visits_counts." + type + ".visits", pymongo.DESCENDING).limit(amount)


def create_codes(type, amount):
    codes_data = []
    type_data = visits_count.find_one({"_id": type}, projection={"created_amount": True, "_id": False})
    if type_data:
        created_amount = type_data["created_amount"]
    else:
        visits_count.insert_one({"_id": type, "visits": 0, "unique_visits": 0, "created_amount": 0})
        created_amount = 0
    all_created_amount = visits_count.find_one({"_id": "ALL"}, projection={"created_amount": True, "_id": False})["created_amount"]
    for i in range(amount):
        created_amount += 1
        all_created_amount += 1
        codes_data.append({"_id": gen_code(), "public_id": gen_code(), "created_date": int(time.time()), "created_number": created_amount, "all_created_number": all_created_amount, "type": type, "include_in_count": True, "uses": 0, "uses_data": []})
    visits_count.update_one({"_id": type}, {"$inc": {"created_amount": amount}})
    visits_count.update_one({"_id": "ALL"}, {"$inc": {"created_amount": amount}})
    referral_codes.insert_many(codes_data)
    return codes_data
