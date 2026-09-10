# def insert_patient_data(name:,age):
#     print(name)
#     print(age)
#     print('inserted into database')
    
# insert_patient_data('Sarthak','twenty')

#Here consider  a scenario that there ia senior developer and junior developer ok so considering now we go in deep there ..I have decelread one function passing age and name ok but as a senior developer i know thta the data type of age i int but junior developer dont known so he has written 'Twenty' so to solve this we need pydantic

#Type-valaidation nhi ho raha -python ki in general problem...dynmaikc typing nhi hoti

# def insert_patient_data(name:str,age:int):
#     print(name)
#     print(age)
#     print('inserted into database')
    
# insert_patient_data('Sarthak','twenty') #type hunting - error nhi deta weak hai


def insert_patient_data(name:str,age:int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print('inserted successfully')
    else:
        raise TypeError('Incorrect dara type')
insert_patient_data('Sarthak','30')