from typing import Any

from pydantic import BaseModel, field_validator

'''
Plain validators: act similarly to "before" validators but they terminate validation immediately after returning, so no further validators are called and Pydantic does not do any of its internal validation against the field type

'''

class Model(BaseModel):
    number: int

    @field_validator('number', mode='plain')
    @classmethod
    def val_number(cls, value):
        if isinstance(value, int):
            return value * 2
        else:
            return value

class Patient(BaseModel):
    age: int
    name: str

    @field_validator('age', mode='plain')
    @classmethod
    def parse_age_custom(cls, value):
        if isinstance(value, str):
            return int(value.split()[0])  # extract number from string like "30 years"
        return value


print(Model(number=4))
#> number=8
print(Model(number='invalid'))  
#> number='invalid'

p = Patient(age='25 years', name='Alice')
print(p.age)