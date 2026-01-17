# Problems with our current approach in 1_before_pydantic python file:
------------------------------------------------------------------------
1.Repetitive boilerplate code - You're manually checking types in every function (if type(name) == str and type(age) == int). This doesn't scale.

2.No validation beyond type checking - You can only validate types. What if you need to validate:

    Age must be > 0 and < 150
    Name must be non-empty or match a pattern
    Email format validation
    Custom business logic
3.Error handling is manual - You raise generic TypeError without detailed messages about what went wrong or where.

4.Hard to maintain - If you add 10 more functions with similar validation, you're duplicating the same checks everywhere.

5.No documentation - The code doesn't clearly document what valid inputs look like.

# Automatic type coercion in Pydantic

Pydantic automatically converts data types when possible. For example, if you pass a string "32" for an age field expecting an integer, Pydantic will convert it to 32.

This automatic coercion makes Pydantic very flexible for real-world scenarios where data comes from APIs, forms, or databases with inconsistent types


```python
patient_info = {'name': 'Rafael Nadal', 'age': "32"}  # age is a STRING "32"
patient1 = Patient(**patient_info)
print(patient1.age)  # Output: 32 (as INTEGER)

```
Why does Pydantic convert "32" (string) to 32 (int)?

Pydantic automatically coerces values to match the schema when possible. Since "32" can be cleanly converted to an integer without losing information, Pydantic does it automatically.

Key behaviors:

✅ "32" → 32 (works - valid conversion) 

✅ 32.0 → 32 (works - float to int conversion)

✅ True → 1 (works - bool to int)

❌ "hello" → Error (can't convert non-numeric string to int)

# Optional and Default values in Pydantic

With Optional:

```python
from typing import Optional

class Patient(BaseModel):
    allergies: Optional[List[str]] = None

```

Without Optional:

```python
class Patient(BaseModel):
    allergies: List[str]  # REQUIRED - must provide a list

# ❌ This would fail:
p = Patient(name='John', age=25)  # Missing allergies field
```

Default Values: 
Default values make a field optional by providing a fallback value if not supplied.
```python
class Patient(BaseModel):
    married: bool = False  # Default is False
    allergies: Optional[List[str]] = None  # Default is None
```

## **Default Values**

Default values make a field optional by providing a fallback value if not supplied.

```python
class Patient(BaseModel):
    married: bool = False  # Default is False
    allergies: Optional[List[str]] = None  # Default is None
```

**Key differences:**

| Scenario | Code | Required? | Default |
|----------|------|-----------|---------|
| **No default, no Optional** | `name: str` | ✅ Yes | None |
| **Default value** | `married: bool = False` | ❌ No | False |
| **Optional (no default)** | `allergies: Optional[List[str]]` | ✅ Yes | None |
| **Optional + default** | `allergies: Optional[List[str]] = None` | ❌ No | None |


# Email Validation with Pydantic
**EmailStr** is a Pydantic validator that automatically validates email format and ensures the field contains a valid email address

NOTE: You may need to install the email-validator package: pip install email-validator

```python
from pydantic import BaseModel, EmailStr
class Patient(BaseModel):
    name: str
    email: EmailStr  # Validates email format automatically
```
```python
# ✅ Valid email
p1 = Patient(name='John', email='john@example.com')

# ❌ Invalid email - raises ValidationError
p2 = Patient(name='John', email='invalid-email')
p3 = Patient(name='John', email='john@')
p4 = Patient(name='John', email='@example.com')
```

Benefits:

✅ Automatic email validation

✅ Prevents invalid emails from being stored

✅ No need to write regex or custom validation logic

✅ Clear error messages when invalid

# URL Validation with Pydantic
**AnyUrl** is a Pydantic validator that automatically validates URL format and ensures the field contains a valid URL.

```python
from pydantic import BaseModel, AnyUrl
class ITProfile(BaseModel):
    linkedin_url: AnyUrl  # Validates URL format
    github_url: Optional[AnyUrl] = None  # Optional GitHub profile
```
```python
# ✅ Valid URLs
p1 = ITProfile(linkedin_url='https://www.linkedin.com/in/johndoe', github_url='https://www.github.com/johndoe')

# ❌ Invalid URL - raises ValidationError
p2 = ITProfile(linkedin_url='invalid-url')
p3 = ITProfile(linkedin_url='www.linkedin.com/in/johndoe')  # Missing scheme (http/https)
p4 = ITProfile(linkedin_url='https://')
```