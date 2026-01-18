
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