from pydantic import BaseModel

class Patient(BaseModel):
    # 1 -- creating schema of pydantic class
    name : str # type validation
    age: int   # type validation





patient_info = {'name': 'Rafael Nadal', 'age': "32"}

#2 --- creating pydantic object from Patient class
patient1 = Patient(**patient_info) # here ** means unpacking the dictionary



# 3 --- using the pydantic object to send/use in insert_patient_data method
def insert_patient_data(patient1):
    print(patient1.name)
    print(patient1.age)
    print('inserted')

def update_patient_data(patient1):
    print(patient1.name)
    print(patient1.age)
    print('updated')


insert_patient_data(patient1) # calling the function
update_patient_data(patient1)