
# What are nested models in Pydantic, why do we need them, and where do they appear in MLOps systems?

Nested models are Pydantic models that are used inside other models as fields.
They help represent 
                    **structured, 
                    hierarchical data and 
                    enforce validation **at multiple levels, which is common in MLOps pipelines.

## What exactly are Nested Models?
A nested model is simply:

A BaseModel used as a field type inside another BaseModel

Each level is validated independently

Example:

```python
from pydantic import BaseModel
class Address(BaseModel):
    street: str
    city: str
    zip_code: str
class Patient(BaseModel):
    name: str
    age: int
    address: Address  # Nested model

patient_info = {
    'name': 'Alexander bublik',
    'age': 30,
    'address': {
        'street': '123 Main St',
        'city': 'Kazakhstan',
        'zip_code': '12345'
    }
}
patient = Patient(**patient_info)
print(patient.address.city)  # Access nested model field
```
## Why Use Nested Models?
- **Structured Data Representation**: Reflects real-world hierarchical data (e.g., patient info with address).
- **Reusability**: Define common structures once (e.g., Address) and reuse
- **Clearer Validation**: Each model validates its own fields, improving data integrity.
- **Improved Readability**: Logical grouping of related fields enhances code clarity.

##### Why NOT just use dict?

Using plain dictionaries for nested data lacks the benefits of Pydantic models:

- No automatic validation of nested structures
- Harder to enforce data types and constraints
- Less readable and maintainable code
- Error-prone
- No auto-docs
- No schema generation

## Where Are Nested Models Used in MLOps?
In MLOps, nested models are commonly used for:
- **Configuration Management**: Complex configurations with multiple sections (e.g., data sources, model parameters).
- **Data Schemas**: Representing structured input/output data for models.
- **Experiment Tracking**: Storing detailed experiment metadata with nested attributes.


**Nested models allow us to model complex ML inputs, configs, and outputs in a structured and validated way, which is critical for reliable MLOps systems**