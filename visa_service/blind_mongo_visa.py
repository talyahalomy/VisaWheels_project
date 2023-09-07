from fastapi import FastAPI, Response, HTTPException
import requests
import random
import uvicorn
import os
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# Initialize MongoDB client and collection for approved_visa
client = MongoClient("mongodb://localhost:27017")

db = client.visa
approved_visa_collection = db.approved_visa



class VisaTransactionModel(BaseModel):
    customer_id: str
    card_number: str
    vehicle_id: str
    amount: str
    status: str
    transaction_id: str

def decide_request(status):
    return random.choice(status)

@app.post("/receive", tags=["receive"])
async def receive_post_request(data: VisaTransactionModel):
    # Assuming VisaTransactionModel matches your incoming data
    print("Received data:", data.dict())

    final_status = decide_request(status)
    transaction_id = random.randint(100000, 999999)

    data.status = final_status
    data.transaction_id = str(transaction_id)

    # Save the received data to MongoDB collection
    approved_visa_collection.insert_one(data.dict())

    if final_status == "approve":
        # Handle approved transactions as needed
        pass
    else:
        # Handle rejected transactions as needed
        pass

    return data.dict()

@app.get("/get-approved-visa-transactions")
async def get_approved_visa_transactions():
    # Retrieve all approved visa transactions from MongoDB
    transactions = list(approved_visa_collection.find())
    return transactions

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
