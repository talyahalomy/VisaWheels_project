from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
import uvicorn
# import json
import random
# from pydantic import BaseModel
# import string

# class Visa(BaseModel):
#     customer : str
#     card_number : str
#     amount : str

app = FastAPI()

# def generate_transaction_id():
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# MongoDB setup
# client = MongoClient("mongodb://localhost:27017")
client = MongoClient("mongodb://localhost:27017")
db = client["visa"]
received_data_collection = db["visa"]  # Use the existing "visa" collection
success_visa_collection = db["success"]
rejected_visa_collection = db["rejected"]



@app.post("/receive", tags=["receive"])
async def receive_post_request(data: dict):
    # Process the received data
    print(data)

    transection_id = random.randint(10000, 99999)
    statuses = ["success"] * 8 + ["failure"] * 2
    random_status = random.choice(statuses)

    if random_status == "success":
        transaction_data_good = {
            "customer_id": data["customer"],
            "card_number": data["card_number"],
            "amount": data["amount"],
            "transaction_id": transection_id,
            "status": random_status
        }
        success_visa_collection.insert_one(transaction_data_good)
        

        return {
            "message": "Transaction successful",
            "customer_id": data["customer"],
            "transaction_id": transection_id,
            "status": random_status
        }
    
    elif random_status == "failure":
        transaction_data_bad = {
            "customer_id": data["customer"],
            "card_number": data["card_number"],
            "amount": data["amount"],
            "transaction_id": transection_id,
            "status": random_status
        }
        rejected_visa_collection.insert_one(transaction_data_bad)
    
        

        return {
            "message": "Transaction failed",
            "customer_id": data["customer"],
            "transaction_id": transection_id,
            "status": random_status
        }
    
    # received_data_collection.insert_one({"data": data})

    return {"message": "Data received successfully"}

# @app.post("/Transection", tags=["Transection"])
# async def Transection():
#     received_data = received_data_collection.find_one({})["data"]
#     # received_data = received_data_collection.find_one({})

#     vehicle_id = received_data["vehicle_id"]

#     db_vehicles_client = MongoClient("mongodb://172.17.0.1:27017")
#     db_vehicles = db_vehicles_client["vehiecls"]
#     vehicle_data = db_vehicles["vehicels"].find_one({"vehicles.vehicle_id": vehicle_id})



#     vehicle_data = db_vehicles["vehicels"].find_one({"vehicles.vehicle_id": vehicle_id})
#     if vehicle_data is None:
#         return {"message": "Vehicle not found"}

#     selected_vehicle = None
#     for vehicle in vehicle_data["vehicles"]:
#         if vehicle["vehicle_id"] == vehicle_id:
#             selected_vehicle = vehicle
#             break

#     if selected_vehicle is None:
#         return {"message": "Vehicle not found"}

#     transection_id = random.randint(10000, 99999)

#     if random_status == "success":
#         transaction_data_good = {
#             "customer_id": received_data["customer"],
#             "card_number": received_data["card_number"],
#             "amount": selected_vehicle["vehicle_price"],
#             "transaction_id": transection_id,
#             "status": random_status
#         }
#         success_visa_collection.insert_one(transaction_data_good)
        
        


#         return {
#             "message": "Transaction successful",
#             "customer_id": received_data["customer"],
#             "transaction_id": transection_id,
#             "status": random_status
#         }
#     elif random_status == "failure":
#         transaction_data_bad = {
#             "customer_id": received_data["customer"],
#             "card_number": received_data["card_number"],
#             "amount": selected_vehicle["vehicle_price"],
#             "transaction_id": transection_id,
#             "status": random_status
#         }
#         rejected_visa_collection.insert_one(transaction_data_bad)
    
        

#         return {
#             "message": "Transaction failed",
#             "customer_id": received_data["customer"],
#             "transaction_id": transection_id,
#             "status": random_status
#         }


@app.get("/")
async def home():    
    return "hello" 


@app.get("/Good",tags = ["Good"])
async def get_all_good():
    my_good_json = list(success_visa_collection.find({}))
    for data in my_good_json:
        data["_id"] = str(data["_id"])
    return my_good_json

@app.get("/Bad",tags = ["Bad"])
async def get_all_bad():
    my_bad_json = list(rejected_visa_collection.find({}))
    for data in my_bad_json:
        data["_id"] = str(data["_id"])
    return my_bad_json

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9010)
