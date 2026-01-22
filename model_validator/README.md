
**“If we already have field validators in Pydantic, why do we need model validators? What are model validators?”**

Field validators validate individual fields in isolation, while model validators validate the relationship between multiple fields or the entire request/model as a whole.

1️⃣ What are Model Validators?

Model validators run on the entire **Pydantic model**, not a single field.

They allow you to:

    1. Validate cross-field dependencies

    2. Enforce business logic

    3. Validate configuration consistency

    4. Prevent invalid ML inference or training runs


2️⃣ When to Use Model Validators
Use model validators when:
- You need to validate relationships between multiple fields (e.g., start_date < end_date).
- You want to enforce complex business rules that depend on multiple fields.
- You need to ensure overall model consistency or integrity.
**Comparison:**

```python
from pydantic import BaseModel, model_validator, ValidationError
from datetime import date
# ❌ Field validators alone can't validate cross-field logic
class EventOld(BaseModel):
    name: str
    start_date: date
    end_date: date

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        if v < date.today():
            raise ValueError("start_date must be in the future")
        return v

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v):
        if v < date.today():
            raise ValueError("end_date must be in the future")
        return v

# ✅ Model validator for cross-field validation
class EventNew(BaseModel):
    name: str
    start_date: date
    end_date: date

    @model_validator(mode='after')
    @classmethod
    def validate_dates(cls, model):
        if model.start_date < date.today():
            raise ValueError("start_date must be in the future")
        if model.end_date < date.today():
            raise ValueError("end_date must be in the future")
        if model.start_date >= model.end_date:
            raise ValueError("start_date must be before end_date")
        return model
```

| Mode     | When it runs            | Use case                           |
| -------- | ----------------------- | ---------------------------------- |
| `before` | Before field validation | Normalize payload, inject defaults |
| `after`  | After validation        | Cross-field checks                 |


Most MLOps use mode="after"

Field validators ensure data correctness, while model validators ensure configuration correctness — which is critical in MLOps to prevent bad training or inference runs