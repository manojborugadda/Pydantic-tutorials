
"""
Docstring for nested_models.nested_models

Nested + Validators ( important question )

We can validate inside nested models or across models.

Field validator inside nested model

"""

from pydantic import BaseModel, model_validator,field_validator


class Features(BaseModel):
    age: int

    @field_validator("age")
    @classmethod
    def check_age(cls, v):
        if v < 0:
            raise ValueError("age must be positive")
        return v

#Cross-field validation using model validator

class InferenceRequest(BaseModel):
    model_version: str
    features: Features

    @model_validator(mode="after")
    def check_version(cls,model):
        if model.model_version == 'v2' and model.features.age < 18:
            raise ValueError("model version v2 requires age >= 18")
        return model
    
inference_data = {
    "model_version": "v2",
    "features": {
        "age": 20
    }
}
inference_request = InferenceRequest(**inference_data)
print(inference_request.model_version)
print(inference_request.features.age)
# Raises ValueError: model version v2 requires age >= 18