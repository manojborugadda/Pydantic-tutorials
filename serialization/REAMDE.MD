| Function                | Use                  |
| ----------------------- | -------------------- |
| `model_dump()`          | Convert model → dict |
| `model_dump_json()`     | Convert model → JSON |
| `model_validate()`      | Dict → model         |
| `model_validate_json()` | JSON → model         |

# What is serialization in Pydantic?
Serialization in Pydantic refers to the process of converting Pydantic models into formats suitable for storage or transmission, such as python dictionaries or JSON strings. This is essential for tasks like API responses, data storage, and inter-service communication.

In MLOps, serialization is critical for API responses, logging, model inference outputs, and experiment tracking.

# What exactly happens during serialization?
    Raw JSON → Validation → Pydantic Model → Serialization → JSON/Dict

# Serialization Methods in Pydantic
Pydantic provides built-in methods for serialization:
- `model_dump()`: Converts a Pydantic model instance into a Python dictionary.
- `model_dump_json()`: Converts a Pydantic model instance into a JSON string.
- `model_validate()`: Validates and creates a Pydantic model instance from a Python dictionary.
- `model_validate_json()`: Validates and creates a Pydantic model instance from a JSON string.
These methods ensure that data is correctly formatted and validated during serialization and deserialization processes, which is crucial for maintaining data integrity in MLOps workflows.

# serialize to dict
```python
from pydantic import BaseModel
class Patient(BaseModel):
    name: str
    age: int
    weight: float  # kg
    height: float  # m
patient = Patient(name='John Doe', age=30, weight=70.5, height=1.75)
patient_dict = patient.model_dump()
print(patient_dict)
#> {'name': 'John Doe', 'age': 30, 'weight': 70.5, 'height': 1.75}
```

# serialize to JSON
```python
from pydantic import BaseModel
class Patient(BaseModel):
    name: str
    age: int
    weight: float  # kg
    height: float  # m
patient = Patient(name='John Doe', age=30, weight=70.5, height=1.75)
patient_json = patient.model_dump_json()
print(patient_json)
#> '{"name": "John Doe", "age": 30, "weight": 70.5, "height": 1.75}'
```
# deserialize from dict
```python
from pydantic import BaseModel
class Patient(BaseModel):
    name: str
    age: int
    weight: float  # kg
    height: float  # m
patient_data = {'name': 'Jane Doe', 'age': 28, 'weight': 60.0, 'height': 1.65}
patient = Patient.model_validate(patient_data)
print(patient)
#> name='Jane Doe' age=28 weight=60.0 height=1.65
```

# deserialize from JSON
```python
from pydantic import BaseModel
class Patient(BaseModel):
    name: str
    age: int
    weight: float  # kg
    height: float  # m
patient_json = '{"name": "Jane Doe", "age": 28, "weight": 60.0, "height": 1.65}'
patient = Patient.model_validate_json(patient_json)
print(patient)
#> name='Jane Doe' age=28 weight=60.0 height=1.65
```

# Why serialization is critical in MLOps?

Serialization is used when:

- Returning inference results via FastAPI

- Logging predictions to MLflow

- Sending metrics to Prometheus / Kafka

- Storing metadata in databases

- **Without serialization → model output is unusable outside Python**



# exclude_unset: Exclude fields that were not explicitly set (i.e., fields with default values)
```python
from pydantic import BaseModel
class Address(BaseModel):
    city: str
    state: str
    pin: str
class Patient(BaseModel):
    name: str
    age: int
    address: Address
    gender: str = 'male'  # default value
address_dict = {'city': 'Mallorca', 'state': 'spain', 'pin': '122001'}
patient_dict = {'name': 'ALCARAZ', 'age': 35, 'address': address_dict,'gender':'female'}
patient = Patient(**patient_dict)

patient_dict = patient.model_dump(exclude_unset=True)
print(patient_dict)
#> {'name': 'ALCARAZ', 'age': 35, 'address': {'city': 'Mallorca', 'state': 'spain', 'pin': '122001'}}
```
