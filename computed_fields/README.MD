

**What are computed fields in Pydantic, why do we need them, and where are they used in MLOps?**

Computed fields in Pydantic are properties that are automatically computed from other fields in a model. They allow you to define dynamic values based on existing fields, which can be useful for calculations or derived data.

1️⃣ What are Computed Fields?

Computed fields in Pydantic are properties defined using the `@computed_field` decorator. They compute their value based on other fields in the model and can be accessed like regular attributes.

They are not provided by the user and are mainly used for responses, metadata, and observability in MLOps systems.

Introduced officially in Pydantic v2

❌ Not part of input validation

❌ Cannot be set by the client

2️⃣ Why Use Computed Fields?

- **Dynamic Calculations**: Automatically compute derived values (e.g., BMI).
- **Data Consistency**: Ensure derived values stay in sync with base data.
- **Reduced Redundancy**: Avoid storing redundant calculated data.

3️⃣ Where Are Computed Fields Used in MLOps?

In MLOps, computed fields are used for:
- **Feature Engineering**: Derive new features from raw data.
- **Model Validation**: Compute metrics or thresholds for validation.
- **Data Preprocessing**: Normalize or transform data before training.

Example:

```python
from pydantic import BaseModel, computed_field

class Patient(BaseModel):
    name: str
    age: int
    weight: float  # kg
    height: float  # m

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
```

## Why not use a normal @property?

| Feature                      | `@property` | `@computed_field` |
| ---------------------------- | ----------- | ----------------- |
| Appears in API response      | ❌ No        | ✅ Yes             |
| Included in schema (OpenAPI) | ❌ No        | ✅ Yes             |
| Serializable                 | ❌ No        | ✅ Yes             |

FastAPI exposes computed fields in Swagger automatically

Q: Can computed fields be validated?
A: No, computed fields are derived from other fields and are not directly validated. However, you can ensure that the base fields used in the computation are validated properly.
If validation is required, it must happen on the input fields or via a model validator.

Q: Can clients send computed fields in request payload?
A: No, computed fields are read-only and cannot be set by clients. They are derived from other fields in the model and are intended for output purposes only.

```text
Computed fields help expose derived, read-only values in API responses, which is extremely useful in MLOps for metadata, monitoring, and inference insights — without polluting request validation.
```