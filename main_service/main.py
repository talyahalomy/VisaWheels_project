#Python code for the main service, which will be responsible for the following:
#Handeling vehicles data, and sending it to the visa service to ask for transaction


from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

#docs_url to be default when you run the app on the browser in ingress
app = FastAPI(docs_url="/")


client = MongoClient("mongodb://localhost:27017")
db_vehicles = client["vehiecls"]
collection = db_vehicles["vehiecls"]

#homepage
@app.get("/")
async def home():
    return "Hello, this is the Vehicle Management API!"

#Get all vehicles
@app.get("/vehicles", tags=["vehicles"])
async def get_all_vehicles():
    vehicle_data = []
    for doc in collection.find():
        vehicles = doc.get("vehicles", [])
        for vehicle in vehicles:
            vehicle_data.append(vehicle)
    return {"data": vehicle_data}

#Get a specific vehicle by id
@app.get("/vehicles/{vehicle_id}", tags=["vehicles"])
async def get_vehicle_by_id(vehicle_id: int):
    vehicle = collection.find_one({"vehicles.vehicle_id": vehicle_id})
    if vehicle is None:
        return {"message": "Vehicle not found"}
    
    for veh in vehicle["vehicles"]:
        if veh["vehicle_id"] == vehicle_id:
            return veh
    
    return {"message": "Vehicle not found"}


#Create a new vehicles
@app.post("/vehicles", tags=["vehicles"])
async def create_vehicle(vehicle_id :int ,manufacturer: str, model: str, year: int, color: str, vehicle_price: float):
    new_vehicle = {
        "vehicle_id": vehicle_id,
        "manufacturer": manufacturer,
        "model": model,
        "year": year,
        "color": color,
        "vehicle_price": vehicle_price
    }
    result = collection.insert_one({"vehicles": [new_vehicle]})
    return {"message": "Vehicle created successfully", "vehicle_id": str(result.inserted_id)}


#Update a vehicle
@app.put("/vehicles/{vehicle_id}", tags=["vehicles"])
async def update_vehicle(vehicle_id: int, manufacturer: str, model: str, year: int, color: str, vehicle_price: float):
    updated_vehicle = {
        "vehicle_id": vehicle_id,
        "manufacturer": manufacturer,
        "model": model,
        "year": year,
        "color": color,
        "vehicle_price": vehicle_price
    }
    result = collection.update_one(
        {"vehicles.vehicle_id": vehicle_id},
        {"$set": {"vehicles.$": updated_vehicle}}
    )
    if result.modified_count > 0:
        return {"message": "Vehicle updated successfully"}
    else:
        return {"message": "Vehicle not found"}

#Delete a vehicle
@app.delete("/vehicles/{vehicle_id}", tags=["vehicles"])
async def delete_vehicle(vehicle_id: int):
    result = collection.update_one(
        {"vehicles.vehicle_id": vehicle_id},
        {"$pull": {"vehicles": {"vehicle_id": vehicle_id}}}
    )
    if result.modified_count > 0:
        return {"message": "Vehicle deleted successfully"}
    else:
        return {"message": "Vehicle not found"}


url_visa = "http://localhost:9010/receive"  

#Buy a vehicle
@app.post("/order", tags=["order"])
async def buy_car(customer: str, card_number: str, vehicle_id: int):

    vehicle_data = collection.find_one({"vehicles.vehicle_id": vehicle_id})
    if vehicle_data is None:
        return {"message": "Vehicle not found"}

    selected_vehicle = None
    for vehicle in vehicle_data["vehicles"]:
        if vehicle["vehicle_id"] == vehicle_id:
            selected_vehicle = vehicle
            break

    if selected_vehicle is None:
        return {"message": "Vehicle not found"}

    data_to_send = {
        "customer": customer,
        "card_number": card_number,
        "amount": selected_vehicle["vehicle_price"],
        "vehicle_id": vehicle_id
    }

    print("Sending data:", data_to_send)

    res = requests.post(url=url_visa, json=data_to_send)  # Sending to visa service
    print("Response:", res.text)

    return res.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
