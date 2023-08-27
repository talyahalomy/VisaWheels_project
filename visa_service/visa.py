from fastapi import FastAPI, Response
import random
import json
import uvicorn

app = FastAPI()


Transaction_id = random.randint(100000, 999999)


@app.get("/")
async def homepage():
    return Response(content= "Welcome to VISA website! \nGo to /docs to make a transaction.", media_type="text/plain")


approved_visa = {}
rejected_visa = {}
all_transactions = approved_visa, rejected_visa


""" @app.post("/transaction")
async def Transaction ():
      with open("data_to_send.json", "r") as f:
                data_to_send = json.load(f)
        if final_status == "approve":
            data_to_insert = {"customer_id":data_to_send["data"]["customer_id"],
            "visa_number": data_to_send["data"]["card_number"],
            "amount": data_to_send["data"]["amount"], 
            "status": final_status,
            "Transaction_id": Transaction_id}

            with open("approved_visa.json", "w+") as f:
               json.dump(data_to_insert, f, default=str, indent=4)

        else: 
            data_to_insert = {"customer_id":data_to_send["data"]["customer_id"],
            "visa_number": data_to_send["data"]["card_number"],
            "amount": data_to_send["data"]["amount"], 
            "status": final_status}

            with open("rejected_visa.json", "w+") as f:
               json.dump(data_to_insert, f, default=str, indent=4)           

 """


status = ["approve"] * 8 + ["reject"] * 2

def decide_reuqest(status):
    return random.choice(status)



@app.post("/receive", tags=["receive"])
async def receive_post_request(data: dict):
    print("Received data:", data)  
    final_status = decide_reuqest(status)
    Transaction_id = random.randint(100000, 999999)
    received_data = data 
    received_data["status"] = final_status
    if final_status == "approve":
        approved_visa[Transaction_id] = received_data
    else:
        rejected_visa[Transaction_id] = received_data
    return received_data

       

@app.get("/get-all-transactions")
async def get_all_transactions():
    return all_transactions
         

@app.get("/get-all-rejected-transactions")
async def get_all_rejected_transactions():
    return rejected_visa

@app.get("/get-all-approved-transactions")
async def get_all_approved_transactions():
    return approved_visa


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)

