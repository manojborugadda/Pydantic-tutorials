from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'Mallorca', 'state': 'spain', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'ALCARAZ', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude_unset=True) # Exclude unset fields 
temp1 = patient1.model_dump(exclude={'name', 'age'}) # simple exclusion
temp2 = patient1.model_dump(include={'address'}) # nested inclusion
temp4 = patient1.model_dump(exclude_unset=False) # Exclude unset fields 

print("############### exclude_unset=False  #####################")
print(temp4)
print(type(temp4))

print("############## exclude_unset=True ######################")
print(temp)
print(type(temp))
print("####################################")
print(temp1)
print(type(temp1))

print("####################################")

print(temp2)
print(type(temp2))

print("####################################")

temp3 = patient1.model_dump(exclude={'address': ['pin']}) # nested exclusion
print(temp3)
print(type(temp3))