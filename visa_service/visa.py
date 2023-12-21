# This Python for the visa service, which will be responsible for the following:
# Receiving transaction request from the main service -
# - and sending back the transaction status (success/failure)

from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
import uvicorn
import random


app = FastAPI()



# MongoDB setup

client = MongoClient("mongodb://localhost:27017")
db = client["visa"]
received_data_collection = db["visa"]  # Use the existing "visa" collection
success_visa_collection = db["success"]
rejected_visa_collection = db["rejected"]


# Receive data from the main service, and send back the transaction status
@app.post("/receive", tags=["receive"])
async def receive_post_request(data: dict):
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


    return {"message": "Data received successfully"}


app = FastAPI(docs_url="/")

#homepage
async def home():    
    return "Hello and welcome to the visa service!" 


# Get all approved transactions
@app.get("/Good",tags = ["Good"])
async def get_all_good():
    my_good_json = list(success_visa_collection.find({}))
    for data in my_good_json:
        data["_id"] = str(data["_id"])
    return my_good_json

# Get all rejected transactions
@app.get("/Bad",tags = ["Bad"])
async def get_all_bad():
    my_bad_json = list(rejected_visa_collection.find({}))
    for data in my_bad_json:
        data["_id"] = str(data["_id"])
    return my_bad_json


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9010)



