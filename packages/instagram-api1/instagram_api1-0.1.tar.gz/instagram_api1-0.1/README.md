## Usage

### Example

```python
from instagram_api1 import InstagramAPI

# Create an instance of the API class
instagram_api = InstagramAPI()

# Get email input from the user
email = input("Enter the email to reset password: ")

# Send a password reset request
result = instagram_api.send_password_reset(email)

# Handle the response
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print("Password reset request sent successfully!")
```