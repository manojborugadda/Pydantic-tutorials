from pydantic import AnyUrl, BaseModel,EmailStr, field_validator
from typing import Dict, List,Optional

class Patient(BaseModel):
    # 1 -- creating schema of pydantic class

    # Basic information
    name : str # string type validation
    age: int   # integer type validation
    weight: float  # float type validation
    email: EmailStr # Automatically validates email format

    # IT-specific fields
    linkedin_url: AnyUrl  # Validates URL format
    github_url: Optional[AnyUrl] = None  # Optional GitHub profile

    # Medical information
    allergies: Optional[List[str]] = None  # list of strings with default value
    married: bool = False # boolean type with default value
    contact_details: Dict[str, str]  # dictionary with string keys and string values


    #use case 1 ------ we need to  validate the EMAILs where it should allow only specific domain names
    @field_validator('email', mode = 'before')
    @classmethod
    def email_validator(cls, value):
        #abc@gmail.com
        valid_domain = ['hdfc.com','icici.com']
        #we are extracting the domain names from email
        domain_name  = value.split('@')[-1]

        if domain_name not in valid_domain:
            raise ValueError('not a valid domain')
        return value


    #use case 2 ------------ transform the Name field to Upper case
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    #use case 3 ------------- validate age to be between 0 and 120
    # we used mode as before because we want to validate even before type coercion
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        if value < 0 or value > 120:
            raise ValueError('Age must be between 0 and 120')
        return value
    



patient_info = {'name': 'Rafael Nadal', 'age': '45', 'weight': 85.5,
                'email': 'rafael.nadal@hdfc.com',  # ❌ gmail.com not allowed
                'linkedin_url': 'https://www.linkedin.com/in/rafaelnadal/',
                'contact_details': {'phone': '123-456-7890'}}


#2 --- creating pydantic object from Patient class

#here validation will be done and if any type coercion is needed that will be done also
patient1 = Patient(**patient_info) # here ** means unpacking the dictionary



# 3 --- using the pydantic object to send/use in insert_patient_data method
def update_patient_data(patient1):
    print(patient1.name)
    print(patient1.age)
    print(patient1.weight)
    print(patient1.allergies)
    print(patient1.married)
    print(patient1.email)



update_patient_data(patient1)# calling the function