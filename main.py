#creating basic route and accessing that to display hello world 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def hello():
    return {'message' : 'Patient Managment System API'}


@app.get("/about")

def about():
    return {'message':'Fully Functionaled API to manage your patients record'}

