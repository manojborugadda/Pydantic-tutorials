from pydantic import AnyUrl, BaseModel,EmailStr,Field
from typing import Annotated, Dict, List,Optional

class Patient(BaseModel):
    # 1 -- creating schema of pydantic class

    # Basic information
    name : Annotated[str, Field(max_length=50, title="Name of the Patient Name", description=" Give name of the patient in less than 50 characters")]  # string type with max length validation
    age: Annotated[int, Field(gt = 0, le=120, description="Age must be between 1 and 120")]  # integer type with validation
    weight: Annotated[float, Field(gt=0,strict= True, description="Weight must be a positive number")]  # float type with greater than 0 validation
    email: EmailStr # Automatically validates email format

    # IT-specific fields
    linkedin_url: AnyUrl  # Validates URL format
    github_url: Optional[AnyUrl] = None  # Optional GitHub profile

    # Medical information
    allergies: Annotated[Optional[List[str]], Field(default=None, description="List of allergies")]  # list of strings with default value
    married: Annotated[bool, Field(default=False, description="Marital status of the patient")]  # boolean type with default value
    contact_details: Dict[str, str]  # dictionary with string keys and string values

# simulating incoming data as dictionary

# patient_info = {'name': 'Rafael Nadal', 'age': "32", 'weight': 85.5, 
#                 'allergies': ['pollen', 'nuts'], 'married': True,
#                 'contact_details': {'phone': '123-456-7890', 'email': 'rafael.nadal@gmail.com'}}

patient_info = {'name': 'Rafael Nadal', 'age': "32", 'weight': 85.5,
                
                'contact_details': {'phone': '123-456-7890', 'email': 'rafael.nadal@gmail.com'},'email': 'rafael.nadal@gmail.com', 'linkedin_url': 'https://www.linkedin.com/in/rafaelnadal/','github_url': 'https://www.github.com/rafaelnadal'}

#2 --- creating pydantic object from Patient class
patient1 = Patient(**patient_info) # here ** means unpacking the dictionary



# 3 --- using the pydantic object to send/use in insert_patient_data method
def update_patient_data(patient1):
    print(patient1.name)
    print(patient1.age)
    print('weight:', patient1.weight)
    print('allergies:', patient1.allergies)
    print('married:', patient1.married)
    print(patient1.contact_details)
    print(patient1.email)
    print(patient1.linkedin_url)
    print(patient1.github_url)
    # print('updated')



update_patient_data(patient1)# calling the function