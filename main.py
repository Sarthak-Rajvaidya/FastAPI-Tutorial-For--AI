#creating basic route and accessing that to display hello world 

from fastapi import FastAPI
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


