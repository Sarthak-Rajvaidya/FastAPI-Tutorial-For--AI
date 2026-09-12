#creating basic route and accessing that to display hello world 

from fastapi import FastAPI,Path,HTTPException,Query 

from fastapi.responses import JSONResponse

from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

import json

class Patient(BaseModel):
    id:Annotated [str,Field(...,description='ID of the patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='Name of the patient')]
    city :Annotated[str,Field(...,description='City where patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of teh patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,decription ='Gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description ='Height of the patient in mtrs')]
    weight : Annotated[float,Field(...,gt=0,description = 'Weight of the patient in kgs')]
    
    #Compuated field - with help of input find cpmuated fields 
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / self.height**2, 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'UnderWeight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    
    
#2nd pydantic model for update

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
    

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        
    return data

#creating utlity fn for converting dict to json

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)      

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
def view_patient(patient_id:str=Path(...,description = 'ID of the patient in DB',example='P001')):
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


@app.post('/create')
def create_patient(patient : Patient):
    #Load existing data
    data = load_data()
    
    #Check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code = 400,detail = 'Patient already exits')
    
    #If new patient :- new patient add 
    #Pydantic object to dictionary - .model_dump()
    
    data[patient.id] = patient.model_dump(exclude = ['id'])
    
    #save new one into json file as it a python dict
    
    save_data(data)
    
    return JSONResponse(status_code = 201,content = {'mesaage':'Patient created succesfuuly'})

#We will see PUT and DELETE

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code = 404,detail ='Patient not found')
    
    existing_patient_info = data[patient_id]
    
    updated_patient_info =patient_update.model_dump(exclude_unset = True)
    
    for key,value in updated_patient_info.items():
        
        existing_patient_info[key] = value
    #Now the problem is that when i will update weight so according to it bmi as well as category will also be updated 
    
    # existing_patient_info-> pydantic object -> updated bmi + verdict -> pydantic object -> dict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    
    patient_pydantic_obj.model_dump(exclude='id')
      #add this dict to data  
    data[patient_id] = existing_patient_info
    
    #save data
    
    save_data(data)
    
    
    return JSONResponse(status_code = 200,content={'message':'patient updated '})
    
    
    