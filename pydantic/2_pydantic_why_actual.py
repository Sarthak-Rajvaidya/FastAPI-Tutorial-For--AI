
from pydantic import BaseModel
class Patient(BaseModel):
    name : str
    age : int #Type valiation


def insert_patient_data(name,age):
    print(name)
    print(age)
    print('inserted')