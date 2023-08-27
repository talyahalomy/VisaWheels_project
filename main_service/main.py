from fastapi import FastAPI, Response
import json
import requests 
import uvicorn


# with open("vehicles.json", "r") as f:
#          my_vehicles = json.load(f)

my_vehicles = {
    "829102":{ "manufactor": "Mitsubishi"
    ,"model": "Lancer Evolution"
    ,"year": 2008
    ,"color": "Red",
    "vehicle_id": 829102,
    "price": 170000
    },"778214":{ "manufactor": "Peugeot"
    ,"model": "106"
    ,"year": 1999
    ,"color": "White",
    "vehicle_id": 778214,
    "price": 45000
    }}

customers = {
       
    "82719239": { 

    "customer_id": 82719239,
    "name": "Steve Jobs",
    "address": "Colorado, South Park",
    "phone": "8102310777"

},

"78812932":{

        "customer_id": 78812932,
        "name": "Steve Jobs",
        "address": "Colorado, South Park",
        "phone": "8102310223" },   
"80942932":{

        "customer_id": 80942932,
        "name": "Steve Jobs",
        "address": "Colorado, South Park",
        "phone": "9528101231"  }
    
}


app = FastAPI()

@app.get("/", tags=["Homepage"])
async def homepage():
        return Response(content= "Hello and welcome to our vehicle website! \nGo to /docs to see all our functions.", media_type="text/plain")

#GET used for viewwing specific vehicle:
@app.get("/get-vehicle", tags=["Vehicle"])
async def vehicle(vehicle_id: str ):
        if vehicle_id not in my_vehicles:
                return {"Error": "Vehicle ID not found"}
        return my_vehicles[vehicle_id]

#GET used for viewing all vehicles:
@app.get("/get-all-vehicles", tags=["Vehicle"])
async def vehicle():
        return my_vehicles


@app.put("/update-vehicle", tags=["Vehicle"])
#PUT used for updating existing vehicle details:
async def update_vehicle(vehicle_id: str, manufactor: str, model: str, year: int, color: str):
        if vehicle_id not in my_vehicles:
                return {"Error": "Vehicle ID not found"}      
        my_vehicles[vehicle_id]["manufactor"] = manufactor
        my_vehicles[vehicle_id]["model"] = model
        my_vehicles[vehicle_id]["year"] = year
        my_vehicles[vehicle_id]["color"] = color
        return my_vehicles[vehicle_id]

#POST used for creating new vehicle:
@app.post("/create-vehicle", tags=["Vehicle"])
async def create_vehicle(vehicle_id: str, manufactor: str, model: str, year: int, color: str):
        if vehicle_id in my_vehicles:
                return {"Error": "Vehicle ID already exists"}
        my_vehicles[vehicle_id] = {"manufactor": manufactor, "model": model, "year": year, "color": color, "vehicle_id": vehicle_id}
        return my_vehicles[vehicle_id]

@app.get("/vehicles")
async def get_vehicles():
    vehicles = []
    for vehicle in my_vehicles.values():
        vehicles.append(vehicle)
    return {"vehicles": vehicles}

#DELETE used for deleting vehicle:
@app.delete("/delete-vehicle", tags=["Vehicle"])
async def delete_vehicle(vehicle_id: str):
        if vehicle_id not in my_vehicles:
                return {"Error": "Vehicle ID not found"}
        del my_vehicles[vehicle_id]
        return {"Vechicle has been deleted"}
        
#use my customers json file to load customers
#with open("customers.json", "r") as f:
        #customers = json.load(f)


@app.get("/get-customer", tags=["Customers"])
async def customer(customer_id: str):
        if customer_id not in customers:
                return {"Error": "Customer ID not found"}
        return customers[customer_id]

@app.get("/get-all-customers", tags=["Customers"])
async def customer():
        return customers

@app.put("/update-customer", tags=["Customers"])
async def update_customer(customer_id: str, name: str, address: str, phone: str):
        if customer_id not in customers:
                return {"Error": "Customer ID not found"}
        customers[customer_id]["name"] = name
        customers[customer_id]["address"] = address
        customers[customer_id]["phone"] = phone
        return customers[customer_id]

@app.post("/create-customer", tags=["Customers"])
async def create_customer(customer_id: str, name: str, address: str, phone: str):
        if customer_id in customers:
           return {"Error": "Customer ID already exists"}
        customers[customer_id] = {"name": name, "address": address, "phone": phone, "customer_id": customer_id}
        return customers[customer_id]


#Get visa URL and port from environment variables

target_url = "http://lucid_williamson:8000/receive"


@app.post("/order",tags = ["order"])
async def buy_car(customer_id : str, card_number : str, vehicle_id : str, amount : str):
    #selected_car = my_vehicles[vehicle_id]
    data_to_send = { "data" :  {
        "customer_id": customer_id,  
        "card_number" : card_number,
        "vehicle_id" : vehicle_id,
        "amount" : amount   } }

     

    response = requests.post(url=target_url,json=data_to_send)



if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=9001)

 

