#creating basic route and accessing that to display hello world 

from fastapi import FastAPI,Path
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        
    return data
        

@app.get("/")

def hello():
    return {'message' : 'Patient Managment System API'}


@app.get("/about")

def about():
    return {'message':'Fully Functionaled API to manage your patients record'}


# to give all patients data to client following is the API ok  we are using @get API

@app.get('/view')

def view():
    data = load_data()
    return data

#This function can fetch data for a particular fix data entry
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,decription = 'ID of the patient in DB',example='P001')):
    #load all the patients
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    return {'error':'patient not found'}

#Path() function :- In fastAPIit is used to provide metadata,validation,rules and documnetation hints for path parameteres in your API endpoints 

# Title decription like in patinet_id above it we could write eg like these way ok so accordingly





