from fastapi import FastAPI, Response
import requests
import random
import json
import uvicorn
import os
from pymongo import MongoClient
from pydantic import BaseModel



app = FastAPI()

client = MongoClient("mongodb://localhost:27017")

db = client.visa
aproved_visa_collection = db.aproved_visa
rejected_visa_collection = db.rejected_visa
received_data_collection = db.received_data


@app.get("/")
async def homepage():
    return Response(content= "Welcome to VISA website! \nGo to /docs to make a transaction.", media_type="text/plain")


@app.post("/receive", tags=["receive"])
async def receive_post_request(data: dict):
    # Process the received data
    print(data)


    transection_id = random.randint(10000, 99999)
    statuses = ["success"] * 8 + ["failure"] * 2
    random_status = random.choice(statuses)

    if random_status == "success":
        transaction_data_good = {
            "customer_id": data["customer_id"],
            "vehicle_id": data["vehicle_id"],
            "transaction_id": transection_id,
            "status": random_status
        }
        aproved_visa_collection.insert_one(transaction_data_good)
        
        


        return {
            "message": "Transaction successful",
            "customer_id": data["customer_id"],
            "transaction_id": transection_id,
            "status": random_status
        }
    
    elif random_status == "failure":
        transaction_data_bad = {
            "customer_id": data["customer_id"],
            "transaction_id": transection_id,
            "status": random_status
        }
        rejected_visa_collection.insert_one(transaction_data_bad)
    
        

        return {
            "message": "Transaction failed",
            "customer_id": data["customer_id"],
            "transaction_id": transection_id,
            "status": random_status
        }
    
    # received_data_collection.insert_one({"data": data})

    return {"message": "Data received successfully"}




######
# class ApprovedVisa(BaseModel):
#     vehicle_id: int
#     customer_id: int
#     status: str
#     transaction_id: int


# Transaction_id = random.randint(100000, 999999)
# status = ["approve"] * 8 + ["reject"] * 2

# def decide_reuqest(status):
#     return random.choice(status)



# main_target_url = "http://127.0.0.1:9001/ready-order"

# #get request from main_with_mongo and add to aproved_visa_collection
# @app.post("/transaction-request", tags=["transaction-request"])
# async def transaction_request(data):
#    aproved_visa_collection.insert_one(data)
    
    
   


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)


