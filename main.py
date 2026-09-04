#creating basic route and accessing that to display hello world 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def hello():
    return {'message' : 'Hello world'}


@app.get("/about")

def about():
    return {'message':'Chatgpt is a ghreat platform for reading about AI'}