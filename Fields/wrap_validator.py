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


