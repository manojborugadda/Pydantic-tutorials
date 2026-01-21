"""
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

"""


# Data Validation for ML Model Input
from pydantic import BaseModel, field_validator, ValidationError

class MLModelInput(BaseModel):
    """Input data for a machine learning model"""
    feature_1: float
    feature_2: float
    feature_3: float
    
    @field_validator('feature_1', 'feature_2', 'feature_3', mode='wrap')
    @classmethod
    def validate_feature_range(cls, value, handler):
        # BEFORE: Log the raw input (for debugging/monitoring)
        print(f"[LOG] Raw feature value: {value}")
        
        # Call handler: Run Pydantic's standard validation (type coercion)
        validated_value = handler(value)
        
        # AFTER: Check if feature is in expected range (ML domain knowledge)
        if validated_value < -100 or validated_value > 100:
            raise ValueError(f"Feature out of range [-100, 100]: {validated_value}")
        
        print(f"[LOG] Validated feature value: {validated_value}")
        return validated_value

# Usage
try:
    input_data = MLModelInput(feature_1="45.5", feature_2=32.1, feature_3=78.9)
    print("✓ Input valid, ready for model inference")
except ValidationError as e:
    print(f"✗ Validation failed: {e}")