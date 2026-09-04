#creating basic route and accessing that to display hello world 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def hello():
    return {'message' : 'Hello world'}

