
# Fields in Pydantic
Pydantic's `Field` function allows you to define additional metadata, validation rules and provides advanced control over field behavior. It is particularly useful for setting constraints on data types, providing default values, and adding descriptions.

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str = Field(...)  # ... means required
    age: int = Field(gt=0, lt=150)  # Greater than 0, less than 150
```

**Common Field Parameters:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `default` | Default value if not provided | `Field(default=False)` |
| `default_factory` | Factory function for mutable defaults | `Field(default_factory=list)` |
| `title` | Display name | `Field(title="Patient Name")` |
| `description` | Field documentation | `Field(description="Patient's full name")` |
| `gt` | Greater than | `Field(gt=0)` |
| `lt` | Less than | `Field(lt=150)` |
| `ge` | Greater than or equal | `Field(ge=0)` |
| `le` | Less than or equal | `Field(le=150)` |
| `min_length` | Minimum string/list length | `Field(min_length=1)` |
| `max_length` | Maximum string/list length | `Field(max_length=100)` |
| `pattern` | Regex pattern | `Field(pattern=r'^\d{3}-\d{3}-\d{4}$')` |
| `alias` | Alternative input name | `Field(alias="patient_name")` |
| `exclude` | Exclude from serialization | `Field(exclude=True)` |


 **Real Example for Your Hospital System:**
```python
from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Optional, List

class Patient(BaseModel):
    # Basic information with constraints
    name: str = Field(
        min_length=1, 
        max_length=100,
        description="Patient's full name"
    )
    
    age: int = Field(
        gt=0, 
        lt=150,
        description="Patient's age in years"
    )
    
    weight: float = Field(
        gt=0,
        description="Patient's weight in kg"
    )
    
    email: EmailStr = Field(
        description="Patient's email address"
    )
    
    # IT-specific fields
    linkedin_url: AnyUrl = Field(
        description="LinkedIn profile URL"
    )
    
    github_url: Optional[AnyUrl] = Field(
        default=None,
        description="GitHub profile URL (optional)"
    )
    
    # Medical information
    allergies: Optional[List[str]] = Field(
        default=None,
        max_length=10,
        description="List of known allergies"
    )
    
    married: bool = Field(
        default=False,
        description="Marital status"
    )
    
    phone: str = Field(
        pattern=r'^\d{3}-\d{3}-\d{4}$',
        description="Phone number in format XXX-XXX-XXXX"
    )
    
    contact_details: dict = Field(
        description="Additional contact information"
    )

# Usage
patient_info = {
    'name': 'Rafael Nadal',
    'age': 32,
    'weight': 85.5,
    'email': 'rafael.nadal@gmail.com',
    'linkedin_url': 'https://www.linkedin.com/in/rafaelnadal/',
    'github_url': 'https://www.github.com/rafaelnadal',
    'allergies': ['pollen', 'nuts'],
    'married': True,
    'phone': '123-456-7890',
    'contact_details': {'company': 'Sports Inc'}
}

patient = Patient(**patient_info)
print(patient.name)  # Works fine
```

# Annotations with Fields in Pydantic
Pydantic supports the use of `Annotated` from the `typing` module to combine type hints with additional metadata, such as validation rules provided by `Field`. This allows for a more structured and clear way to define fields in your models.

Annotated makes your code more readable by keeping the type information upfront while keeping metadata organized with Field. It's the modern Pydantic best practice


```python
from typing import Annotated
from pydantic import Field

# Without Annotated
name: str = Field(max_length=50, description="Patient name")

# With Annotated (cleaner)
name: Annotated[str, Field(max_length=50, description="Patient name")]
```

**Why use Annotated?**

1. Separates type from constraints - Type hint is clear, metadata is separate
2. Better readability - The actual type (str, int, etc.) is prominent
3. IDE support - Better type checking and autocomplete
4. Standards compliant - Works with other tools (**FastAPI**, JSON Schema, etc.)

**Comparison:**

```python
from typing import Annotated
from pydantic import Field, BaseModel

# ❌ Old way (less clear)
class PatientOld(BaseModel):
    name: str = Field(max_length=50, title="Name")
    age: int = Field(gt=0, le=120)

# ✅ New way with Annotated (clearer)
class PatientNew(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name")]
    age: Annotated[int, Field(gt=0, le=120)]
```

# strict Parameter in Pydantic Fields
Pydantic provides a `strict` parameter in the `Field` function that enforces strict type checking for fields. When `strict=True` is set, Pydantic will not perform any type coercion and will raise a validation error if the input data does not exactly match the specified type.

```python
from pydantic import BaseModel, Field, ValidationError
class Patient(BaseModel):
    age: int = Field(strict=True)
# Example usage
try:
    patient = Patient(age='30')  # This will raise a ValidationError
except ValidationError as e:
    print(e)
```
In this example, attempting to create a `Patient` instance with a string for the `age` field will result in a validation error because `strict=True` enforces that the input must be an integer.This is particularly useful in scenarios where data integrity is critical, and you want to avoid unintended type conversions.

# Field Validators in Pydantic
Pydantic provides a powerful way to validate and transform data using field validators. Field validators are methods that you can define in your Pydantic models to perform custom validation or transformation logic on specific fields.

**modes of field validators:**
1. `before`: The validator is called before any type coercion or validation is performed on the field.
2. `after`: The validator is called after the field has been validated and coerced to the correct type.
3. `wrap`: The validator wraps around the standard validation process, allowing you to access both the raw input and the validated value.
4. `plain`: The validator is called with the raw input value, without any type coercion or validation.

Note: By default, if no mode is specified, `mode='after'` is used.

# Wrap Validators in Pydantic
``Wrap validators``: the most flexible validators. They let you run code BEFORE or AFTER Pydantic validates the input. You can also skip validation entirely and return/reject the value immediately.

How they work:
- You define a validator with an extra 'handler' parameter
- The handler is a function that runs Pydantic's standard validation
- You can wrap the handler call in try-except to catch errors
- You can choose to call the handler or skip it completely

Example flow:
1. Your code runs BEFORE handler (pre-validation logic)
2. Call handler(value) to run Pydantic's validation
3. Your code runs AFTER handler (post-validation logic)
4. Return the final value

**Real-world analogy**:
    Think of wrap like a security checkpoint:

    Before handler: Check the person's ID

    Handler: Run standard security scan (metal detector, etc.)

    After handler: Give them a visitor badge

    Skip handler: For VIPs, let them straight through without the scan