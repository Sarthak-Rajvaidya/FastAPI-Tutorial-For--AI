#creating basic route and accessing that to display hello world 

from fastapi import FastAPI,Path,HTTPException,Query 
from pydantic import BaseModel,Field
from typing import Annotated,Literal

import json

class Patient(BaseModel):
    id:Annotated [str,Field(...,description='ID of the patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='Name of the patient')]
    city :Annotated[str,Field(...,description='City where patient is living')]
    age:Annotated[str,Field(...,gt=0,lt=120,description='Age of teh patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,'Gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description ='Height of the patient')]
    weight : float
    
    
    
    

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
    
    raise HTTPException(status_code = 404,detail='Patient not found')

#Path() function :- In fastAPIit is used to provide metadata,validation,rules and documnetation hints for path parameteres in your API endpoints 

# Title decription like in patinet_id above it we could write eg like these way ok so accordingly


#Query Parametere :- Optional key value pair appended to end of URL employed for operatiins like filtering,sorting,searching /patiensts?city=Delhi&sort_by=age



@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height ,weight and bmi'),order:str=Query('asc',description='sort in ascending and dexcending order')):
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400,detail =f'Invalid field select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order between asc and desc')
    
    data = load_data()
    
    sort_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse = sort_order)
    
    return sorted_data


